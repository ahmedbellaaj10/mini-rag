from enum import Enum


class LLMEnums(Enum):
    OPENAI = "OPENAI"
    COHERE = "COHERE"


class OpenAIRolesEnums(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class CoHereRolesEnums(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    DOCUMENT = "search_document"
    QUERY = "search_query"


class DocumentTypesEnums(Enum):
    DOCUMENT = "document"
    QUERY = "query"
