# ============================================================
# OPENROUTER LLM CLIENT
# ============================================================

import json
import os
from pathlib import Path

from openai import OpenAI
from dotenv import load_dotenv


# ============================================================
# LOAD .ENV
# ============================================================

CURRENT_FILE = Path(__file__).resolve()

# llm_client.py
#      ↓
# llm/
#      ↓
# rag/
RAG_DIR = CURRENT_FILE.parent.parent

ENV_FILE = RAG_DIR / ".env"

load_dotenv(
    dotenv_path=ENV_FILE
)


# ============================================================
# STRUCTURED RESPONSE SCHEMA
# ============================================================

# ============================================================
# STRUCTURED RESPONSE SCHEMA
# ============================================================

RESPONSE_SCHEMA = {
    "type": "object",

    "properties": {

        # ====================================================
        # MAIN ANSWER
        # ====================================================

        "answer": {
            "type": "string"
        },

        # ====================================================
        # EXPERIMENTAL EVIDENCE
        # ====================================================

        "experimental_evidence": {
            "type": "array",

            "items": {
                "type": "object",

                "properties": {

                    "experiment_id": {
                        "type": "string"
                    },

                    "oxygen_concentration": {
                        "type": [
                            "number",
                            "null"
                        ]
                    },

                    "flame_temperature": {
                        "type": [
                            "number",
                            "null"
                        ]
                    },

                    "source": {
                        "type": "string"
                    },

                    "finding": {
                        "type": "string"
                    }
                },

                "required": [
                    "experiment_id",
                    "oxygen_concentration",
                    "flame_temperature",
                    "source",
                    "finding"
                ],

                "additionalProperties": False
            }
        },

        # ====================================================
        # ML PREDICTION
        # ====================================================

        "prediction": {
            "type": [
                "object",
                "null"
            ],

            "properties": {

                "target": {
                    "type": "string"
                },

                "value": {
                    "type": "number"
                },

                "unit": {
                    "type": "string"
                },

                "input_conditions": {
                    "type": "object",

                    "properties": {

                        "fuel": {
                            "type": [
                                "string",
                                "null"
                            ]
                        },

                        "oxygen_concentration": {
                            "type": [
                                "number",
                                "null"
                            ]
                        },

                        "pressure": {
                            "type": [
                                "number",
                                "null"
                            ]
                        },

                        "pressure_unit": {
                            "type": [
                                "string",
                                "null"
                            ]
                        },

                        "gravity": {
                            "type": [
                                "string",
                                "null"
                            ]
                        }
                    },

                    "required": [
                        "fuel",
                        "oxygen_concentration",
                        "pressure",
                        "pressure_unit",
                        "gravity"
                    ],

                    "additionalProperties": False
                },

                "is_prediction": {
                    "type": "boolean"
                }
            },

            "required": [
                "target",
                "value",
                "unit",
                "input_conditions",
                "is_prediction"
            ],

            "additionalProperties": False
        },

        # ====================================================
        # OBSERVED TRENDS
        # ====================================================

        "observed_trends": {
            "type": "array",

            "items": {
                "type": "string"
            }
        },

        # ====================================================
        # INTERPRETATION
        # ====================================================

        "interpretation": {
            "type": "string"
        },

        # ====================================================
        # SAFETY INSIGHT
        # ====================================================

        "safety_insight": {
            "type": "string"
        },

        # ====================================================
        # LIMITATIONS
        # ====================================================

        "limitations": {
            "type": "array",

            "items": {
                "type": "string"
            }
        },

        # ====================================================
        # SOURCES
        # ====================================================

        "sources": {
            "type": "array",

            "items": {
                "type": "string"
            }
        }
    },

    "required": [
        "answer",
        "experimental_evidence",
        "prediction",
        "observed_trends",
        "interpretation",
        "safety_insight",
        "limitations",
        "sources"
    ],

    "additionalProperties": False
}
# ============================================================
# LLM CLIENT
# ============================================================

class LLMClient:

    def __init__(
        self,
        model="qwen/qwen-2.5-72b-instruct",
        fallback_model="qwen/qwen3-30b-a3b",
        base_url="https://openrouter.ai/api/v1",
        temperature=0.7,
        timeout=300
    ):

        self.model = model

        self.fallback_model = fallback_model

        self.base_url = base_url

        self.temperature = temperature

        self.timeout = timeout


        # ----------------------------------------------------
        # API KEY
        # ----------------------------------------------------

        api_key = os.getenv(
            "OPENROUTER_API_KEY"
        )


        if not api_key:

            raise ValueError(
                "OPENROUTER_API_KEY was not found.\n"
                f"Expected .env file at:\n{ENV_FILE}"
            )


        # ----------------------------------------------------
        # OPENAI-COMPATIBLE OPENROUTER CLIENT
        # ----------------------------------------------------

        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout
        )


        # ----------------------------------------------------
        # INFORMATION
        # ----------------------------------------------------

        print("=" * 60)
        print("OPENROUTER LLM CLIENT")
        print("=" * 60)

        print(
            f"Environment file: {ENV_FILE}"
        )

        print(
            f"Environment exists: "
            f"{ENV_FILE.exists()}"
        )

        print(
            f"API key loaded: "
            f"{bool(api_key)}"
        )

        print(
            f"Primary model: "
            f"{self.model}"
        )

        print(
            f"Fallback model: "
            f"{self.fallback_model}"
        )

        print(
            f"Temperature: "
            f"{self.temperature}"
        )

        print(
            f"Timeout: "
            f"{self.timeout}s"
        )

        print("=" * 60)


    # ========================================================
    # GENERATE RESPONSE
    # ========================================================

    def generate(
        self,
        prompt,
        system_prompt=None
    ):
        """
        Send a prompt to the primary LLM.

        If the primary model fails,
        automatically try the fallback model.

        Returns:
            dict
        """

        # ----------------------------------------------------
        # BUILD MESSAGES
        # ----------------------------------------------------

        messages = []


        if system_prompt:

            messages.append({
                "role": "system",
                "content": system_prompt
            })


        messages.append({
            "role": "user",
            "content": prompt
        })


        # ----------------------------------------------------
        # PRIMARY MODEL
        # ----------------------------------------------------

        try:

            print("\n" + "=" * 60)
            print("CALLING PRIMARY MODEL")
            print("=" * 60)

            print(
                f"Model: {self.model}"
            )


            response = (
                self.client
                .chat
                .completions
                .create(

                    model=self.model,

                    messages=messages,

                    temperature=self.temperature,

                    response_format={
                        "type": "json_schema",

                        "json_schema": {

                            "name":
                            "flame_in_freefall_answer",

                            "strict":
                            True,

                            "schema":
                            RESPONSE_SCHEMA
                        }
                    }
                )
            )


            # ------------------------------------------------
            # EXTRACT RESPONSE
            # ------------------------------------------------

            content = (
                response
                .choices[0]
                .message
                .content
            )


            if not content:

                raise ValueError(
                    "Primary model returned empty content."
                )


            # ------------------------------------------------
            # PARSE JSON
            # ------------------------------------------------

            result = json.loads(
                content
            )


            # ------------------------------------------------
            # ADD SYSTEM METADATA
            # ------------------------------------------------

            result["model_used"] = (
                self.model
            )


            print(
                "\nPrimary model succeeded."
            )


            return result


        # ====================================================
        # PRIMARY FAILED
        # ====================================================

        except Exception as primary_error:

            print(
                "\nPrimary model failed:"
            )

            print(
                primary_error
            )


            # ------------------------------------------------
            # FALLBACK
            # ------------------------------------------------

            try:

                print("\n" + "=" * 60)
                print("CALLING FALLBACK MODEL")
                print("=" * 60)

                print(
                    f"Model: "
                    f"{self.fallback_model}"
                )


                response = (
                    self.client
                    .chat
                    .completions
                    .create(

                        model=self.fallback_model,

                        messages=messages,

                        temperature=self.temperature,

                        response_format={
                            "type": "json_schema",

                            "json_schema": {

                                "name":
                                "flame_in_freefall_answer",

                                "strict":
                                True,

                                "schema":
                                RESPONSE_SCHEMA
                            }
                        }
                    )
                )


                # ------------------------------------------------
                # EXTRACT
                # ------------------------------------------------

                content = (
                    response
                    .choices[0]
                    .message
                    .content
                )


                if not content:

                    raise ValueError(
                        "Fallback model returned "
                        "empty content."
                    )


                # ------------------------------------------------
                # PARSE
                # ------------------------------------------------

                result = json.loads(
                    content
                )


                # ------------------------------------------------
                # ADD SYSTEM METADATA
                # ------------------------------------------------

                result["model_used"] = (
                    self.fallback_model
                )


                print(
                    "\nFallback model succeeded."
                )


                return result


            except Exception as fallback_error:

                raise RuntimeError(
                    "\nBoth LLM models failed.\n\n"

                    f"Primary error:\n"
                    f"{primary_error}\n\n"

                    f"Fallback error:\n"
                    f"{fallback_error}"
                )