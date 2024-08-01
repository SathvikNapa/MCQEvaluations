from __future__ import annotations

import json
import os
import re
import time
from itertools import chain

import tqdm

from mcqa.base.input_parser.parser import Parser
from mcqa.base.postprocessor import PostProcessor
from mcqa.base.prompt_crafter import PromptCrafter
from mcqa.commons import logger
from mcqa.commons.regex import extract_regex
from mcqa.config import McqaConfig
from mcqa.dataloaders.csv_loader import CsvLoader
from mcqa.domain.mcqa import McqaInterface
from mcqa.domain.patterns import Patterns
from mcqa.domain.response_generator import (ExceptionLog, Question,
                                            RequestResponseLog,
                                            ResponsesFromSources)
from mcqa.llm_router import LLMRouter

logger = logger.setup_logger()
from mcqa.base.question_formation import QuestionFormation


class Mcqa(McqaInterface):
    """Class to handle MCQA (Multiple Choice Question Answering) operations."""

    def __init__(self, request: Question | ResponsesFromSources):
        """Initializes the Mcqa instance with the given request."""
        self.mcqa_config = McqaConfig()
        self.request = request
        self.postprocessor = PostProcessor()
        self.question_formulator = QuestionFormation()
        self.prompt_crafter = PromptCrafter()
        self.input_parser = Parser()

    def _start_llm(self):
        if ".txt" in self.request.full_context_path:
            self.model = self.mcqa_config.text_model
            self.llm_router = LLMRouter(text_model=self.model)
        if self.request.full_context_path.endswith(("pdf", "png", "jpeg", "jpg")):
            self.model = self.mcqa_config.multimodal_model
            self.llm_router = LLMRouter(multimodal_model=self.model)
        self.llm_router.start_model()

    def generate_query_response(self):
        """Generates a response for the given query based on the context type."""
        question_format = self.request.question_format
        self.request.options.extend(
            ["Y. Not enough information to answer", "Z. Answer not listed"]
        )

        if question_format in ["raw", "naive"]:
            return self._generate_raw_response()
        elif question_format in ["synthetic", "rephrase"]:
            return self.generate_modified_query_response()

    def generate_modified_query_response(self):
        """Generates a modified query response based on the context type."""
        if self.request.full_context_path.endswith(".txt"):
            self.llm_router = LLMRouter(text_model=self.mcqa_config.text_model)
            question_format = self.request.question_format
            prompt_object, options_text, answer = self._get_prompts(question_format)

            user_prompt, system_prompt = prompt_object
            self._start_llm()
            response = self.llm_router.generate_llm_response(
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
                                options=extract_regex(
                                    options, pattern=Patterns.question_options_pattern
                                ),
                                long_context=self.request.full_context_path,
                                options_randomizer=self.request.options_randomizer,
                                answer=answer,
                                question_format="raw",
                                short_context=self.request.question_context,
                            )
                        ).generate_query_response()
                    )
                except Exception as e:
                    logger.error("Exception at Generating Query Response", e)
                    continue

            evaluation = sum(response.evaluation for response in responses) / len(
                responses
            )
            return ResponsesFromSources(
                list_of_responses=responses, evaluation=evaluation
            )

        if self.request.full_context_path.endswith((".pdf", ".png", ".jpeg", ".jpg")):
            self._start_llm()
            question_format = self.request.question_format
            prompt_object, options_text, answer = self._get_prompts(question_format)
            user_prompt, system_prompt = prompt_object

            self.request.attachments.append(self.request.full_context_path)
            parsed_multimodal_objects = [
                self.input_parser.parse(file_path=path)
                for path in self.request.attachments
            ]

            response = self.llm_router.generate_llm_response(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                multimodal_object=parsed_multimodal_objects,
            )
            rephrased_questions = self._postprocess_response(response, question_format)

            responses = [
                Mcqa(
                    request=Question(
                        question=question,
                        options=extract_regex(
                            options, pattern=Patterns.question_options_pattern
                        ),
                        full_context_path=self.request.full_context_path,
                        options_randomizer=self.request.options_randomizer,
                        answer=answer,
                        question_format="raw",
                        question_context=self.request.question_context,
                    )
                ).generate_query_response()
                for question, options, answer in tqdm.tqdm(rephrased_questions)
            ]

            evaluation = sum(response.evaluation for response in responses) / len(
                responses
            )
            return ResponsesFromSources(
                list_of_responses=responses, evaluation=evaluation
            )

    def _generate_raw_response(self):
        """Generates a raw response using the LLM router."""
        if "txt" in self.request.full_context_path:
            prompt_object, options_text, answer = (
                self.question_formulator.use_raw_question(
                    query=self.request.question,
                    options=self.request.options,
                    attachments=self.request.attachments,
                    full_context_path=self.request.full_context_path,
                    answer=self.request.answer,
                    options_randomizer=self.request.options_randomizer,
                    question_format=self.request.question_format,
                    short_context=self.request.question_context,
                )
            )
            user_prompt, system_prompt = prompt_object
            self._start_llm()
            response = self.llm_router.generate_llm_response(
                system_prompt=system_prompt, user_prompt=user_prompt
            )

        if re.search(
                "|".join(["pdf", "png", "jpeg", "jpg"]), self.request.full_context_path
        ):
            self._start_llm()
            prompt_object, options_text, answer = (
                self.question_formulator.use_raw_question(
                    query=self.request.question,
                    options=self.request.options,
                    full_context_path=self.request.full_context_path,
                    options_randomizer=self.request.options_randomizer,
                    answer=self.request.answer,
                    question_format=self.request.question_format,
                    short_context=self.request.question_context,
                )
            )
            self.request.attachments.append(self.request.full_context_path)
            parsed_multimodal_objects = [
                self.input_parser.parse(file_path=path)
                for path in self.request.attachments
            ]
            (
                user_prompt,
                system_prompt,
            ) = prompt_object

            response = self.llm_router.generate_llm_response(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                multimodal_object=parsed_multimodal_objects,
            )
            if self.request.question_format in ["naive"]:
                return self.postprocessor.naive_postprocess(
                    generated_response=response,
                    actual_answer=answer,
                    question=self.request.question,
                    options=options_text,
                    model=self.model,
                )

        return self.postprocessor.postprocess(
            generated_response=response,
            actual_answer=answer,
            question=self.request.question,
            options=options_text,
            model=self.model,
        )

    def _get_prompts(self, question_format):
        """Returns the appropriate prompts based on the question format."""
        if question_format == "synthetic":
            return self.question_formulator.create_synthetic_questions(
                query=self.request.question,
                options=self.request.options,
                full_context_path=self.request.full_context_path,
                answer=self.request.answer,
                short_context=self.request.question_context,
            )
        elif question_format == "rephrase":
            return self.question_formulator.rephrase_question(
                query=self.request.question,
                options=self.request.options,
                full_context_path=self.request.full_context_path,
                answer=self.request.answer,
                short_context=self.request.question_context,
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
            self,
            file_path: str,
            file_type: str,
            question_format: str,
            output_path: str,
            options_randomizer: bool = False,
    ):
        """Generates responses for queries from a file.

        Args:
            file_path (str): The path to the file containing the queries.
            file_type (str): The type of the file (e.g., csv).
            question_format (str): The format of the questions (e.g., raw, synthetic, rephrase).

        Returns:
            ResponsesFromSources: The response generated by the MCQA system.
        """
        if file_type == "csv":
            extracted_requests = CsvLoader(
                options_randomizer=options_randomizer
            ).handle_csv(file_path=file_path)

            final_responses = []
            for _n, (
                    query,
                    option,
                    answer,
                    context,
                    short_context,
                    options_randomizer,
            ) in tqdm.tqdm(enumerate(extracted_requests)):
                # if _n < 5:
                #     continue
                request_payload = Question(
                    query=query,
                    options=option,
                    answer=answer,
                    options_randomizer=options_randomizer,
                    question_format=question_format,
                    long_context=context,
                    short_context=short_context,
                )
                try:
                    request_obj = Mcqa(request=request_payload)
                    time.sleep(5)
                    response = request_obj.generate_query_response()
                    final_responses.append(response)

                    request_response_log = RequestResponseLog(
                        request=request_obj.request, response=response
                    )

                    # Extracting the output
                    os.makedirs(output_path, exist_ok=True)
                    with open(
                            f"{output_path}/request_responseLog_geminiPro_{_n}.json", "w"
                    ) as f:
                        request_res_dict = request_response_log.dict()
                        pretty_request_res_dict = json.dumps(request_res_dict, indent=4)
                        f.write(pretty_request_res_dict)

                except Exception as e:
                    os.makedirs(output_path, exist_ok=True)
                    logger.error(f"Exception Occured: {e}")
                    pretty_request_dict = json.dumps(request_payload.dict(), indent=4)
                    exception_log = ExceptionLog(
                        request=pretty_request_dict, exception=str(e)
                    )
                    with open(
                            f"{output_path}/exception_log_geminiPro_{_n}.json", "w"
                    ) as f:
                        exception_dict = exception_log.dict()
                        pretty_exception_dict = json.dumps(exception_dict, indent=4)
                        f.write(pretty_exception_dict)
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

            serialized_response = ResponsesFromSources(
                list_of_responses=final_responses, evaluation=evaluation
            )

            logger.debug("ResponsesGeneratorResponse: %s", serialized_response)
            return serialized_response
