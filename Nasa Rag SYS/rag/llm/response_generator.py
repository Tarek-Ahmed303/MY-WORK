# ============================================================
# RESPONSE GENERATOR
# ============================================================

from .prompt_builder import PromptBuilder
from .llm_client import LLMClient


class ResponseGenerator:

    def __init__(
        self,
        llm_client=None,
        prompt_builder=None
    ):

        self.llm_client = (
            llm_client
            if llm_client is not None
            else LLMClient()
        )

        self.prompt_builder = (
            prompt_builder
            if prompt_builder is not None
            else PromptBuilder()
        )


    # ========================================================
    # GENERATE LLM FALLBACK RESPONSE
    # ========================================================

    def generate(
        self,
        question,
        context,
        ml_prediction=None
    ):
        """
        Generate a structured answer using the LLM.

        This function should only be called when the
        knowledge base cannot answer the question.
        """

        # ----------------------------------------------------
        # BUILD PROMPT
        # ----------------------------------------------------

        prompt = self.prompt_builder.build(
            question=question,
            context=context,
            ml_prediction=ml_prediction
        )


        # ----------------------------------------------------
        # CALL LLM
        # ----------------------------------------------------

        response = self.llm_client.generate(
               prompt=prompt
              )

        print("LLM raw response type:", type(response))
        print("LLM raw response:", repr(response))


        # ----------------------------------------------------
        # FORCE FALLBACK SOURCE
        # ----------------------------------------------------

        response["source"] = (
            "llm_fallback"
        )


        return response