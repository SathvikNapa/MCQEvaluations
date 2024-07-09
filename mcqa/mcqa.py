import logging

import tqdm

from mcqa.application.postprocessor import PostProcessor
from mcqa.application.prompt_crafter import PromptCrafter
from mcqa.application.question_formation import QuestionFormation
from mcqa.config import McqaConfig
from mcqa.domain.mcqa import McqaInterface
from mcqa.domain.response_generator import ResponseGeneratorRequest, ResponsesGeneratorResponse
from mcqa.llm_router import LLMRouter

logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.DEBUG)


class Mcqa(McqaInterface):
    """Class to handle MCQA (Multiple Choice Question Answering) operations."""

    def __init__(self, request: ResponseGeneratorRequest):
        """Initializes the Mcqa instance with the given request.

        Args:
            request (ResponseGeneratorRequest): The generator request containing query, options, and context.
        """
        self.mcqa_config = McqaConfig()
        self.request = request
        self.postprocessor = PostProcessor(model=self.mcqa_config.text_model)
        self.question_formulator = QuestionFormation(request=self.request)
        self.prompt_crafter = PromptCrafter(
            query=self.request.query,
            options=self.request.options,
            context=self.request.context,
            answer=self.request.answer,
            question_format=self.request.question_format
        )

    def generate_query_response(self):
        """Generates a response for the given query based on the context type.

        Returns:
            str: The generated response from the LLM.
        """
        if self.request.context.context_type == "pdf" or self.request.context.context_type == "text":
            llm_router = LLMRouter(text_model=self.mcqa_config.text_model)

            if self.request.question_format == "raw":
                user_prompt, system_prompt = self.question_formulator.use_raw_question(
                    question=self.request.query
                )
                llm_router.start_model()
                response = llm_router.generate_llm_response(
                    system_prompt=system_prompt,
                    user_prompt=user_prompt
                )
                return self.postprocessor.postprocess(generated_response=response, actual_answer=self.request.answer)

    def generate_modified_query_response(self):
        if self.request.context.context_type == "pdf" or self.request.context.context_type == "text":
            llm_router = LLMRouter(text_model=self.mcqa_config.text_model)
            if self.request.question_format == "synthetic":
                user_prompt, system_prompt = self.question_formulator.create_synthetic_questions(
                    question=self.request.query,
                    answer=self.request.answer,
                    context=self.request.context.link_or_text)
                llm_router.start_model()
                response = llm_router.generate_llm_response(
                    system_prompt=system_prompt,
                    user_prompt=user_prompt
                )
                rephrased_questions = self.postprocessor.postprocess_synthetic(generated_response=response)

                responses = []
                for question, options, answer in tqdm.tqdm(rephrased_questions):
                    responses.append(Mcqa(request=ResponseGeneratorRequest(
                        query=question,
                        options=options,
                        context=self.request.context,
                        answer=answer,
                        question_format="raw"
                    )).generate_query_response())

                evaluation = sum(response.evaluation for response in responses) / len(responses)

                return ResponsesGeneratorResponse(list_of_responses=responses, evaluation=evaluation)

            if self.request.question_format == "rephrase":
                user_prompt, system_prompt = self.question_formulator.rephrase_question(
                    question=self.request.query, options=self.request.options, answer=self.request.answer
                )
                llm_router.start_model()
                response = llm_router.generate_llm_response(
                    system_prompt=system_prompt,
                    user_prompt=user_prompt
                )
                rephrased_questions = self.postprocessor.postprocess_rephrase(generated_response=response)

                logger.debug("Rephrased questions: %s", rephrased_questions)

                responses = []
                for question, options, answer in tqdm.tqdm(rephrased_questions):
                    responses.append(Mcqa(request=ResponseGeneratorRequest(
                        query=question,
                        options=options,
                        context=self.request.context,
                        answer=answer,
                        question_format="raw"
                    )).generate_query_response())

                evaluation = sum(response.evaluation for response in responses) / len(responses)

                return ResponsesGeneratorResponse(list_of_responses=responses, evaluation=evaluation)
