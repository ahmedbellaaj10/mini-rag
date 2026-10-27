from typing import Optional
import logging

import cohere

from ..LLMInterface import LLMInterface
from ..LLMEnums import CoHereRolesEnums, DocumentTypesEnums


class CoHereProvider(LLMInterface):
    def __init__(
        self,
        api_key: str,
        default_input_max_characters: int = 1000,
        default_output_max_tokens: int = 1000,
        default_temperature: float = 0.1,
    ) -> None:
        self.api_key = api_key
        self.default_input_max_characters = default_input_max_characters
        self.default_output_max_tokens = default_output_max_tokens
        self.default_temperature = default_temperature
        self.llm_id: Optional[str] = None
        self.embedding_model_id: Optional[str] = None
        self.embedding_size: Optional[int] = None

        self.client = cohere.ClientV2(api_key=self.api_key)

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
            self.logger.error("Cohere client is not set")
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

        chat_history.append(self.construct_prompt(prompt, CoHereRolesEnums.USER.value))

        response = self.client.chat(
            model=self.llm_id,
            messages=chat_history,
            max_tokens=max_out_tokens,
            temperature=temperature,
        )

        content = getattr(getattr(response, "message", None), "content", None) or []
        text = next(
            (c.text for c in content if getattr(c, "type", None) == "text" and c.text),
            None,
        )

        if not text:
            self.logger.error(
                f"Empty response from Cohere (finish_reason={getattr(response, 'finish_reason', None)})"
            )
            return None

        return text.strip()

    def embed(self, text: str, document_type: Optional[str] = None) -> Optional[list]:
        if not self.client:
            self.logger.error("Cohere client is not set")
            return None
        if not self.embedding_model_id:
            self.logger.error("Embedding model ID is not set")
            return None

        input_type = CoHereRolesEnums.DOCUMENT.value
        if document_type == DocumentTypesEnums.QUERY.value:
            input_type = CoHereRolesEnums.QUERY.value

        response = self.client.embed(
            model=self.embedding_model_id,
            inputs=self.construct_embed_input(text),
            input_type=input_type,
            embedding_types=["float"],
        )

        embeddings = getattr(response, "embeddings", None) or []
        embedding = next(
            (e.float for e in embeddings if getattr(e, "float", None)), None
        )

        if not embedding:
            self.logger.error("Empty embedding response from Cohere")
            return None

        return embedding

    def construct_prompt(self, prompt: str, role: str) -> dict:
        return {"role": role, "content": prompt}

    def construct_embed_input(self, text: str) -> list:
        return [{"content": [{"type": "text", "text": text}]}]
