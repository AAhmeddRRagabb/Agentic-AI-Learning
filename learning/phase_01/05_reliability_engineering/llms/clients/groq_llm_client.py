
from pydantic import BaseModel
from .base_llm_client import BaseLLMClient
from groq import Groq
from groq.types.chat import ChatCompletion


class GroqLLMClient(BaseLLMClient):
    """Using Groq as a model provider."""

    def __init__(
        self,
        api_key         : str,
        max_input_tokens: int = 1000,

        connection_time: int = 60,

    ) -> None:
        super().__init__(
            api_key          = api_key,
            max_input_tokens = max_input_tokens,
            connection_time  = connection_time
        )

    def connect(self, api_key: str) -> Groq:
        try:
            return Groq(
                api_key = api_key,
                timeout = self.connection_time,
            )
        except Exception as e:
            raise e

    
    def create_prompt(self, prompt: str, role  : str) -> dict[str, str]:
        return {
            "content": prompt,
            "role": role,
        }


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
        self.client: Groq
        response: ChatCompletion
        

        user_message = self.create_prompt(
            prompt = self.pre_process_input_prompt(user_prompt),
            role   = "user"
        )

        if system_prompt:
            system_message = self.create_prompt(
                prompt = system_prompt,
                role = 'system'
            )

            messages = [system_message, user_message]

        else:
            messages [user_message]

        try:
            response = self.client.chat.completions.create(
                messages = messages,
                model    = model_name,
                stream   = False,


                temperature       = 0.1,
                top_p             = 0.9,
                max_output_tokens = 512,
            )
            
        except Exception as e:
            self.logger.error(f"Error While Generating Answer: {e}")
            return None
    
        if not self.validate_generation_response(response):
            self.logger.error("Invalid Generation Response")
            return None

        
        return response.choices[0].message.content

    

    def validate_generation_response(
        self,
        response: ChatCompletion,
    ) -> bool:
        return bool(
            response
            and response.choices
            and response.choices[0]
            and response.choices[0].message
            and response.choices[0].message.content
        )
