
from llms import LLMsFactory
from llms.clients import GroqLLMClient, GoogleLLMClient

from helpers.settings import get_settings

class Agent:
    """
    Define the agent class the controls the whole workfolw [user request -> process -> response]
    
    Args:
        required_provider (str): the main provider required.

        connection_time (int): the max time allowed to wait for the client to be initiated in seconds.
        read_time       (int): the max time allowed to wait for the client to return response.
        request_time    (int): the max time allowed to wait for whole generation request.
    """
    def __init__(
        self,
        required_provider: str,

        connection_time: int,
        read_time      : int,
        request_time   : int
    ):
        self.llm_factory = LLMsFactory()

        self.client = self.init_client(required_provider)


    def init_client(provider: str) -> GroqLLMClient | GoogleLLMClient:
        
        
        