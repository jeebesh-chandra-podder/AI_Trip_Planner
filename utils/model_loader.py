import os
from dotenv import load_dotenv
from typing import Literal, Optional, Any
from pydantic import BaseModel, Field
from utils.config_loader import load_config
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI


# This class wraps the configuration dictionary so you can access values like a dictionary.
class ConfigLoader:
    def __init__(self):
        print(f"Loaded config.....")
        self.config = load_config()  # Loads settings from a config file
    
    def __getitem__(self, key):
        return self.config[key] # Allows dict-style access (e.g., config["llm"])

class ModelLoader(BaseModel):
    
    ## It's a Pydantic data model, which means it’s validated on creation.
    ## You can specify whether to use "groq" or "openai".
    model_provider: Literal["groq", "openai"] = "groq"
    config: Optional[ConfigLoader] = Field(default=None, exclude=True)

    
    ## This function is called after the model is initialized.
    ## It ensures the configuration is available for the model provider.
    def model_post_init(self, __context: Any) -> None:
        self.config = ConfigLoader()
    
    class Config:
        arbitrary_types_allowed = True
    
    def load_llm(self):
        """
        Load and return the LLM model.

        It checks which provider to use.
        Then fetches the API key from .env.
        Then fetches the model name from the config.
        Finally, it creates and returns the right LLM object (ChatGroq or ChatOpenAI).
        """
        print("LLM loading...")
        print(f"Loading model from provider: {self.model_provider}")
        if self.model_provider == "groq":
            print("Loading LLM from Groq..............")
            groq_api_key = os.getenv("GROQ_API_KEY")
            model_name = self.config["llm"]["groq"]["model_name"]
            llm=ChatGroq(model=model_name, api_key=groq_api_key)
        elif self.model_provider == "openai":
            print("Loading LLM from OpenAI..............")
            openai_api_key = os.getenv("OPENAI_API_KEY")
            model_name = self.config["llm"]["openai"]["model_name"]
            llm = ChatOpenAI(model_name="o4-mini", api_key=openai_api_key)
        
        return llm
    