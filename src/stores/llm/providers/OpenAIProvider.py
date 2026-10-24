from typing import Optional
import logging
from openai import OpenAI
from ..LLMInterface import LLMInterface
from ..LLMEnums import OpenAIEnums


class OpenAIProvider(LLMInterface):
    def __init__(
        self,
        api_key: str,
        api_url: Optional[str] = None,
        default_input_max_characters: int = 1000,
        default_output_max_tokens: int = 1000,
        default_temperature: float = 0.1,
    ) -> None:
        self.api_key = api_key
        self.api_url = api_url
        self.default_input_max_characters = default_input_max_characters
        self.default_output_max_tokens = default_output_max_tokens
        self.default_temperature = default_temperature
        self.llm_id: Optional[str] = None
        self.embedding_model_id: Optional[str] = None
        self.embedding_size: Optional[int] = None
        self.client = OpenAI(api_key=self.api_key, base_url=self.api_url)
        self.logger = logging.getLogger(__name__)

    def set_llm(self, llm_id: str) -> None:
        self.llm_id = llm_id

    def set_embedding_model(self, embedding_model_id: str, embedding_size: int) -> None:
        self.embedding_model_id = embedding_model_id
        self.embedding_size = embedding_size

    def process_text(self, text: str) -> str:
        return text[: self.default_input_max_characters]

    def generate(
        self,
        prompt: str,
        chat_history: list = [],
        max_out_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
    ) -> Optional[str]:
        if not self.client:
            self.logger.error("OpenAI client is not set")
            return None
        if not self.llm_id:
            self.logger.error("LLM ID is not set")
            return None

        max_out_tokens = (
            max_out_tokens
            if max_out_tokens is not None
            else self.default_output_max_tokens
        )
        temperature = (
            temperature if temperature is not None else self.default_temperature
        )

        chat_history.append(self.construct_prompt(prompt, OpenAIEnums.USER.value))

        response = self.client.chat.completions.create(
            model=self.llm_id,
            messages=chat_history,
            max_tokens=max_out_tokens,
            temperature=temperature,
        )
        if (
            not response
            or not response.choices
            or len(response.choices) == 0
            or not response.choices[0].message
            or not response.choices[0].message.content
        ):
            self.logger.error(
                "Error while generating text: No content returned from OpenAI API"
            )
            return None
        return response.choices[0].message.content

    def embed(self, text: str, document_type: Optional[str] = None) -> Optional[list]:
        if not self.client:
            self.logger.error("OpenAI client is not set")
            return None
        if not self.embedding_model_id:
            self.logger.error("Embedding model ID is not set")
            return None

        response = self.client.embeddings.create(
            model=self.embedding_model_id,
            input=text,
        )
        if (
            not response
            or not response.data
            or len(response.data) == 0
            or response.data[0].embedding is None
        ):
            self.logger.error(
                "Error while embedding text: No embedding returned from OpenAI API"
            )
            return None
        return response.data[0].embedding

    def construct_prompt(self, prompt_template: str, role: str) -> dict:
        return {"role": role, "content": self.process_text(prompt_template)}
