import os
import json
import re
import time
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
        logger.debug("Response Generated")
        return self._parse_response(response)

    def generate_completion_with_url(
        self, system_prompt: str, user_prompt: str, temperature: float
    ) -> str:
        tools = [{"url_context": {}}]

        for _ in range(3):
            try:
                response = self._generate_response(
                    system_prompt, user_prompt, temperature, tools
                )
                break
            except ValueError:
                time.sleep(10)
                continue

        if response.candidates[0].url_context_metadata:
            metadata = response.candidates[0].url_context_metadata
            for url_meta in metadata.url_metadata:
                logger.debug(f"URL Retrieved: {url_meta.retrieved_url}")
                logger.debug(f"Status: {url_meta.url_retrieval_status}")

        return response.text

    def _connect(self) -> genai.Client:
        try:
            client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
            return client
        except Exception as e:
            logger.exception(f"Could not connect to AI Service: {e}")
            raise

    def _generate_response(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
        tools: list[dict] | None = None,
    ) -> types.GenerateContentResponse:
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    temperature=temperature,
                    system_instruction=system_prompt,
                    tools=tools,
                ),
            )

            if not response or not response.text:
                error = "Invalid AI Response Structure"
                logger.error(error)
                raise ValueError(error)

            return response

        except Exception as e:
            logger.exception(f"Could not generate AI response: {e}")
            raise

    def _parse_response(self, response: types.GenerateContentResponse) -> list[dict]:
        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
            match = re.search(
                r"```(?:json)?\s*(\[.*\])\s*```", response.text, re.DOTALL
            )
            if match:
                return json.loads(match.group(1))
            raise
