from typing import Optional
import json

from google import genai
from google.genai import types
from tenacity import retry, stop_after_attempt, wait_exponential

from config.settings import GEMINI_API_KEY


class LLMService:
    """
    Wrapper around Google's Gemini API.

    Every agent in the project should use this service instead of calling
    Gemini directly.
    """

    DEFAULT_MODEL = "gemini-2.5-flash"

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
    ):
        self.api_key = api_key or GEMINI_API_KEY

        if not self.api_key:
            raise ValueError(
                "Gemini API Key not found. Please add GEMINI_API_KEY to your .env file."
            )

        self.client = genai.Client(api_key=self.api_key)
        self.model = model or self.DEFAULT_MODEL

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=2, min=2, max=10),
        reraise=True,
    )
    def generate_completion(
        self,
        system_prompt: str,
        user_prompt: str,
        json_mode: bool = False,
    ):
        """
        Generates a response from Gemini.

        Parameters
        ----------
        system_prompt : str
            System instructions.

        user_prompt : str
            User query.

        json_mode : bool
            If True, Gemini is instructed to return JSON only.

        Returns
        -------
        str | dict
        """

        config = types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.2,
        )

        if json_mode:
            config.response_mime_type = "application/json"

        response = self.client.models.generate_content(
            model=self.model,
            contents=user_prompt,
            config=config,
        )

        text = response.text

        if json_mode:
            return json.loads(text)

        return text