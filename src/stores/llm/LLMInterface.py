from abc import ABC, abstractmethod
from typing import Optional


class LLMInterface(ABC):
    @abstractmethod
    def set_llm(self, llm_id: str) -> None:
        pass

    @abstractmethod
    def set_embedding_model(self, embedding_model_id: str, embedding_size: int) -> None:
        pass

    @abstractmethod
    def generate(
        self,
        prompt: str,
        chat_history: list = [],
        max_out_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
    ) -> Optional[str]:
        pass

    @abstractmethod
    def embed(self, text: str, document_type: Optional[str] = None) -> Optional[list]:
        pass

    @abstractmethod
    def construct_prompt(self, prompt_template: str, role: str) -> dict:
        pass
