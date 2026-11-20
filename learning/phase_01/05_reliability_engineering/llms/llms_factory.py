
import logging


from .clients import GroqLLMClient, GoogleLLMClient

class LLMsFactory:
    """Create an LLM client for the requested provider."""

    def __init__(self):
        self.logger = logging.getLogger("uvicorn")

    def create_agent(
        self, 
        provider: str,
        api_key: str,
        **kwargs
    ) -> GoogleLLMClient | GroqLLMClient | None:
        """
        Creates and returns an LLM client.
        """
        try:
            if provider == 'groq':
                client = GroqLLMClient(
                    api_key = api_key,
                    **kwargs
                )
            elif provider == 'google':
                client = GoogleLLMClient(
                    api_key = api_key,
                    **kwargs
                )

            else:
                self.logger.error(f"Provider {provider} is Not Supported")
                return None

            return client

        except Exception as e:
            self.logger.error(f"Error Initiating LLM Client: {e}")
            return None
