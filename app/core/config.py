import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseModel, Field


class Settings(BaseModel):
    ollama_url: str = Field(default="http://localhost:11434")
    ollama_model: str = Field(default="llama3")

    @property
    def ollama_generate_url(self) -> str:
        return f"{self.ollama_url.rstrip('/')}/api/generate"


@lru_cache
def get_settings() -> Settings:
    load_dotenv()

    return Settings(
        ollama_url=os.getenv("OLLAMA_URL", "http://localhost:11434"),
        ollama_model=os.getenv("OLLAMA_MODEL", "llama3"),
    )
