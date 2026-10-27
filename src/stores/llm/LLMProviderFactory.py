from .LLMInterface import LLMInterface
from .LLMEnums import LLMEnums


class LLMProviderFactory:
    def __init__(self, config: dict):
        self.config = config

    def create_provider(self, provider: str) -> LLMInterface:
        if provider == LLMEnums.OPENAI.value:
            from .providers import OpenAIProvider

            return OpenAIProvider(
                api_key=self.config["OPENAI_API_KEY"],
                api_url=self.config.get("OPENAI_API_BASE_URL"),
                default_input_max_characters=self.config["DEFAULT_MAX_INPUT_CARACTERS"],
                default_output_max_tokens=self.config["DEFAULT_OUTPUT_MAX_TOKENS"],
                default_temperature=self.config["DEFAULT_TEMPERATURE"],
            )
        elif provider == LLMEnums.COHERE.value:
            from .providers import CoHereProvider

            return CoHereProvider(
                api_key=self.config["COHERE_API_KEY"],
                default_input_max_characters=self.config["DEFAULT_MAX_INPUT_CARACTERS"],
                default_output_max_tokens=self.config["DEFAULT_OUTPUT_MAX_TOKENS"],
                default_temperature=self.config["DEFAULT_TEMPERATURE"],
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
