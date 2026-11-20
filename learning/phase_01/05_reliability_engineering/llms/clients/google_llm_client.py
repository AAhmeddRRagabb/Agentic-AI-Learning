from .base_llm_client import BaseLLMClient
from pydantic import BaseModel


from google.genai import Client
from google.genai.types import (
    Content,
    EmbedContentConfig,
    EmbedContentResponse,
    GenerateContentConfig,
    GenerateContentResponse,
    HttpOptions,
    Part,
)


class GoogleLLMClient(BaseLLMClient):
    """Using Google as a model provider."""

    def __init__(
        self,
        api_key         : str,
        max_input_tokens: int = 1000,

        connection_time: int = 60
    ) -> None:
        
        super().__init__(
            api_key          = api_key,
            max_input_tokens = max_input_tokens,
            connection_time  = connection_time
        )


    def connect(self, api_key: str) -> Client:
        try:
            return Client(
                api_key      = api_key,
                http_options = HttpOptions(timeout = self.connection_time * 1000),
            )
        
        except Exception as e:
            raise e


    def create_prompt(self, prompt: str, role: str) -> Content:
        return Content(
            role  = role,
            parts = [Part.from_text(text = prompt)],
        )
    

    def generate_text(
        self,
        user_prompt      : str,
        model_name       : str,
        system_prompt    : str
    ) -> str | None:

        """
        Args:
            user_prompt       (str)
            model_name        (str)
            system_prompt     (str)

        Returns:
            on success => str
            on failure => None
        """
        self.client: Client
        response: GenerateContentResponse
        
        user_content = self.create_prompt(
            prompt = self.pre_process_input_prompt(user_prompt),
            role   = 'user',
        )

        try:
            response = self.client.models.generate_content(
                model    = model_name,
                contents = user_content,
                config   = GenerateContentConfig(
                    system_instruction = system_prompt if system_prompt else None,


                    temperature       = 0.1,
                    top_p             = 0.9,
                    max_output_tokens = 512,

                    tools = []
                )
            )

        except Exception as e:
            self.logger.error(f"Error While Generating Answer: {e}")
            return None

        if not self.validate_generation_response(response):
            self.logger.error("Invalid Generation Response")
            return None


        return response.text

    def validate_generation_response(self, response: GenerateContentResponse) -> bool:
        return bool(response and response.text)
