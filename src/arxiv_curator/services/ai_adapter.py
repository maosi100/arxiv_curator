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
        self.tools = [{"url_context": {}}]

    def generate_completion(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
        tool_use: bool | None = None,
    ) -> list[dict]:
        response = None
        parsed_response = None

        tools = None
        if tool_use:
            tools = self.tools

        for _ in range(3):
            try:
                response = self._generate_response(
                    system_prompt, user_prompt, temperature, tools
                )
                parsed_response = self._parse_response(response)
                logger.debug("Response Generated")
                break
            except Exception as e:
                logger.warning(f"No valid LLM response: {e}. Retrying")
                time.sleep(10)
                continue

        if not response or not parsed_response:
            raise ValueError("Couldn't retrieve or parse LLM response")

        if response.candidates[0].url_context_metadata:
            metadata = response.candidates[0].url_context_metadata
            for url_meta in metadata.url_metadata:
                logger.debug(f"URL Retrieved: {url_meta.retrieved_url}")
                logger.debug(f"Status: {url_meta.url_retrieval_status}")

        return parsed_response

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
        response = self.client.models.generate_content(
            model="gemini-2.5-pro",
            contents=user_prompt,
            config=types.GenerateContentConfig(
                temperature=temperature,
                system_instruction=system_prompt,
                tools=tools,
            ),
        )

        if not response or not response.text:
            raise ValueError("Invalid AI Response Structure")

        return response

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
