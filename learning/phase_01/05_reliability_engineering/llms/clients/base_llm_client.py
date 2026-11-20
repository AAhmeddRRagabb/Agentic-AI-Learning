from abc import ABC, abstractmethod
import logging


class BaseLLMClient(ABC):
    """
    Base class shared by all LLM provider clients.
    """

    def __init__(
        self,
        api_key         : str,
        max_input_tokens: int = 1000,

        connection_time: int = 60,
    ) -> None:
        
        self.max_input_tokens = max_input_tokens
        self.connection_time  = connection_time

        self.logger = logging.getLogger("uvicorn")
        self.client = self.connect(api_key = api_key)


    @abstractmethod
    def connect(self, api_key: str):
        pass

    def disconnect(self) -> None:
        if self.client is None:
            return

        try:
            self.client.close()
        except Exception:
            self.client = None


    # pre-processing
    def pre_process_input_prompt(self, prompt: str) -> str:
        """Ensure that the input length is within the configured range."""
        if len(prompt) > self.max_input_tokens:
            self.logger.info(
                "Prompt has exceeded the max input tokens\n"
                f"- Prompt: {prompt[:50]}...\n"
                f"- Prompt Length: {len(prompt)}\n"
                f"- Max Allowed Input Length: {self.max_input_tokens}\n"
                ">>> Prompt will be truncated <<<\n\n"
            )
            return prompt[: self.max_input_tokens]

        return prompt

    
    @abstractmethod
    def generate_text(
        self,
        user_prompt      : str,
        model_name       : str,
        system_prompt    : str
    ):
        pass

    @abstractmethod
    def validate_generation_response(self, response) -> bool:
        pass

    @abstractmethod
    def create_prompt(self, prompt: str, role: str):
        pass
