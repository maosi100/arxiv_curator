import os
import json
import re
from loguru import logger
from google import genai
from google.genai import types


class AiAdapter:
    def __init__(self) -> None:
        self.client = self._connect()

    def generate_completion(
        self, system_prompt: str, user_prompt: str, temperature: float
    ) -> list[dict]:
        response = self._generate_response(system_prompt, user_prompt, temperature)
        return self._parse_response(response.text)

    def _connect(self) -> genai.Client:
        try:
            client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
            return client
        except Exception as e:
            logger.exception(f"Could not connect to AI Service: {e}")
            raise

    def _generate_response(
        self, system_prompt: str, user_prompt: str, temperature: float
    ) -> types.GenerateContentResponse:
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    temperature=temperature,
                    system_instruction=system_prompt,
                ),
            )

            if not response or not response.text:
                error = "Invalid AI Response Structure"
                logger.error(error)
                raise ValueError(error)

            logger.debug(f"Response generated {response.text[200]}")
            return response

        except Exception as e:
            logger.exception(f"Could not generate AI response: {e}")
            raise

    def _parse_response(self, response: str) -> list[dict]:
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            match = re.search(r"```(?:json)?\s*(\[.*\])\s*```", response, re.DOTALL)
            if match:
                return json.loads(match.group(1))
            raise
