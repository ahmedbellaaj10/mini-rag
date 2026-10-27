from enum import Enum


class LLMEnums(Enum):
    OPENAI = "OPENAI"
    COHERE = "COHERE"


class OpenAIRolesEnums(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
