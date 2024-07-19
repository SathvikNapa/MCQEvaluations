from __future__ import annotations

from itertools import chain

import tqdm

from mcqa.commons import logger
from mcqa.commons.regex import extract_regex
from mcqa.dataloaders.csv_loader import CsvLoader
from mcqa.application.postprocessor import PostProcessor
from mcqa.application.prompt_crafter import PromptCrafter
from mcqa.config import McqaConfig
from mcqa.domain.mcqa import McqaInterface
from mcqa.domain.response_generator import (
    Question,
    ResponsesGeneratorResponse,
)
from mcqa.llm_router import LLMRouter
from mcqa.domain.patterns import Patterns
logger = logger.setup_logger()
from mcqa.application.question_formation import QuestionFormation

class Mcqa(McqaInterface):
    """Class to handle MCQA (Multiple Choice Question Answering) operations."""

    def __init__(self, request: Question | ResponsesGeneratorResponse):
        """Initializes the Mcqa instance with the given request."""
        self.mcqa_config = McqaConfig()
        self.request = request
        self.postprocessor = PostProcessor(model=self.mcqa_config.text_model)
        self.question_formulator = QuestionFormation()
        self.prompt_crafter = PromptCrafter()

        if self.request.long_context.file_type in ["text", "pdf"]:
            self.llm_router = LLMRouter(text_model=self.mcqa_config.text_model)
        if self.request.long_context.file_type in ["image"]:
            self.llm_router = LLMRouter(multimodal_model=self.mcqa_config.multimodal_model)

    def generate_query_response(self):
        """Generates a response for the given query based on the context type."""
        question_format = self.request.question_format

        if question_format == "raw":
            return self._generate_raw_response(self.llm_router)
        elif question_format in ["synthetic", "rephrase"]:
            return self.generate_modified_query_response()

    def generate_modified_query_response(self):
        """Generates a modified query response based on the context type."""
        if self.request.long_context.file_type in ["text", "pdf"]:
            llm_router = LLMRouter(text_model=self.mcqa_config.text_model)
            question_format = self.request.question_format
            prompt_object, options_text, answer = self._get_prompts(question_format)

            user_prompt, system_prompt = prompt_object
            llm_router.start_model()
            response = llm_router.generate_llm_response(
                system_prompt=system_prompt, user_prompt=user_prompt
            )
            rephrased_questions = self._postprocess_response(response, question_format)

            responses = []
            for question, options, answer in tqdm.tqdm(rephrased_questions):
                try:
                    responses.append(
                        Mcqa(
                            request=Question(
                                query=question,
                                options=extract_regex(options, pattern=Patterns.question_options_pattern),
                                long_context=self.request.long_context,
                                answer=answer,
                                question_format="raw",
                                short_context=self.request.short_context,
                            )
                        ).generate_query_response())
                except Exception as e:
                    logger.error("Exception at Generating Query Response", e)
                    continue

            evaluation = sum(response.evaluation for response in responses) / len(
                responses
            )
            return ResponsesGeneratorResponse(
                list_of_responses=responses, evaluation=evaluation
            )

        if self.request.long_context.file_type in ["image"]:
            llm_router = LLMRouter(multimodal_model=self.mcqa_config.multimodal_model)
            question_format = self.request.question_format
            prompt_object, options_text, answer = self._get_prompts(question_format)
            user_prompt, system_prompt, parsed_multimodal_object = prompt_object
            llm_router.start_model()
            response = llm_router.generate_llm_response(
                system_prompt=system_prompt, user_prompt=user_prompt, multimodal_object=parsed_multimodal_object
            )
            rephrased_questions = self._postprocess_response(response, question_format)

            responses = [
                Mcqa(
                    request=Question(
                        query=question,
                        options=extract_regex(options, pattern=Patterns.question_options_pattern),
                        long_context=self.request.long_context,
                        answer=answer,
                        question_format="raw",
                        short_context=self.request.short_context,
                    )
                ).generate_query_response()
                for question, options, answer in tqdm.tqdm(rephrased_questions)
            ]

            evaluation = sum(response.evaluation for response in responses) / len(
                responses
            )
            return ResponsesGeneratorResponse(
                list_of_responses=responses, evaluation=evaluation
            )

    def _generate_raw_response(self, llm_router):
        """Generates a raw response using the LLM router."""
        if self.request.long_context.file_type in ["text", "pdf"]:
            prompt_object, options_text, answer = self.question_formulator.use_raw_question(
                query=self.request.query,
                options=self.request.options,
                context=self.request.long_context,
                answer=self.request.answer,
                question_format=self.request.question_format,
                short_context=self.request.short_context,
            )
            user_prompt, system_prompt = prompt_object
            llm_router.start_model()
            response = llm_router.generate_llm_response(
                system_prompt=system_prompt, user_prompt=user_prompt
            )

        if self.request.long_context.file_type in ["image"]:
            prompt_object, options_text, answer = self.question_formulator.use_raw_question(
                query=self.request.query,
                options=self.request.options,
                context=self.request.long_context,
                answer=self.request.answer,
                question_format=self.request.question_format,
                short_context=self.request.short_context,
            )
            user_prompt, system_prompt, parsed_multimodal_object = prompt_object
            llm_router.start_model()
            response = llm_router.generate_llm_response(
                system_prompt=system_prompt, user_prompt=user_prompt, multimodal_object=parsed_multimodal_object
            )

        return self.postprocessor.postprocess(
            generated_response=response,
            actual_answer=answer,
            question=self.request.query,
            options=options_text,
        )

    def _get_prompts(self, question_format):
        """Returns the appropriate prompts based on the question format."""
        if question_format == "synthetic":
            return self.question_formulator.create_synthetic_questions(
                query=self.request.query,
                options= self.request.options,
                context=self.request.long_context,
                answer=self.request.answer,
                short_context=self.request.short_context,
            )
        elif question_format == "rephrase":
            return self.question_formulator.rephrase_question(
                query=self.request.query,
                options=self.request.options,
                context=self.request.long_context,
                answer=self.request.answer,
                short_context=self.request.short_context,
            )

    def _postprocess_response(self, response, question_format):
        """Postprocesses the response based on the question format."""
        if question_format == "synthetic":
            return self.postprocessor.postprocess_synthetic(generated_response=response)
        elif question_format == "rephrase":
            rephrased_questions = self.postprocessor.postprocess_rephrase(
                generated_response=response
            )
            logger.debug("Rephrased questions: %s", rephrased_questions)
            return rephrased_questions

    def generate_response_from_files(
            self, file_path: str, file_type: str, question_format: str
    ):
        """Generates responses for queries from a file.

        Args:
            file_path (str): The path to the file containing the queries.
            file_type (str): The type of the file (e.g., csv).
            question_format (str): The format of the questions (e.g., raw, synthetic, rephrase).

        Returns:
            ResponsesGeneratorResponse: The response generated by the MCQA system.
        """
        if file_type == "csv":
            extracted_requests = CsvLoader().handle_csv(file_path=file_path)

            final_responses = []
            for _n, (query, option, answer, context, short_context) in tqdm.tqdm(enumerate(extracted_requests)):
                try:
                    request_obj = Mcqa(
                        request=Question(
                            query=query,
                            options=option,
                            answer=answer,
                            question_format=question_format,
                            long_context=context,
                            short_context=short_context,
                        )
                    )
                    response = request_obj.generate_query_response()

                    final_responses.append(response)

                except Exception as e:
                    logger.error(e)
                    continue

            if question_format in ["synthetic", "rephrase"]:
                final_responses = list(
                    chain(
                        *[response_.list_of_responses for response_ in final_responses]
                    )
                )

            evaluation = sum(
                response_.evaluation for response_ in final_responses
            ) / len(final_responses)

            serialized_response = ResponsesGeneratorResponse(
                list_of_responses=final_responses, evaluation=evaluation
            )

            logger.debug(
                "ResponsesGeneratorResponse: %s", serialized_response
            )
            return serialized_response
