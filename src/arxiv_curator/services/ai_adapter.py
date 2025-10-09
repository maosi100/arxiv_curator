import os
import json
import re
import time
from loguru import logger
from google import genai
from google.genai import types, errors


class AiAdapter:
    def __init__(self) -> None:
        self.client = self._connect()
        self.tools = [{"url_context": {}}]

    def generate_completion(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
        model: str,
        tool_use: bool | None = None,
    ) -> list[dict]:
        response = None
        parsed_response = None

        tools = None
        if tool_use:
            tools = self.tools

        for retry in range(3):
            try:
                response = self.client.models.generate_content(
                    model=model,
                    contents=user_prompt,
                    config=types.GenerateContentConfig(
                        temperature=temperature,
                        system_instruction=system_prompt,
                        tools=tools,
                    ),
                )

                if not response:
                    logger.warning("No valid LLM response. Retrying")
                    continue

                parsed_response = self._parse_response(response)

                if not parsed_response:
                    logger.warning("Couldn't properly parse LLM response. Retrying")
                    continue

                logger.debug("Valid LLM response generated & parsed.")
                break

            except errors.APIError as e:
                logger.warning(
                    f"An APIError occured during LLM operation: {e}. Retrying"
                )

                sleep_time = retry * 20 + 20
                time.sleep(sleep_time)
                continue

            except TimeoutError as e:
                logger.warning(f"Connection issues during LLM call: {e}. Retrying.")
                continue

            except json.JSONDecodeError as e:
                logger.warning(f"Couldn't properly parse LLM repose: {e}. Retrying")
                continue

            except Exception as e:
                logger.critical(f"Un unexpected exception occured: {e}. Aborting")
                raise

        if not response or not parsed_response:
            raise ValueError(
                "Couldn't retrieve or parse LLM response, stopped retrying."
            )

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
            logger.critical(f"Could not connect to AI Service: {e}")
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
