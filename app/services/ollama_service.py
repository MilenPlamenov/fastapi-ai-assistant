from json import JSONDecodeError
from typing import Any

import httpx

from app.core.config import Settings, get_settings


class OllamaConnectionError(Exception):
    pass


class OllamaServiceError(Exception):
    pass


class OllamaService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def generate_response(self, prompt: str) -> str:
        payload = {
            "model": self.settings.ollama_model,
            "prompt": prompt,
            "stream": False,
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    self.settings.ollama_generate_url,
                    json=payload,
                )
                response.raise_for_status()
        except httpx.ConnectError as exc:
            raise OllamaConnectionError("Ollama is unavailable") from exc
        except httpx.TimeoutException as exc:
            raise OllamaConnectionError("Ollama request timed out") from exc
        except httpx.HTTPStatusError as exc:
            raise OllamaServiceError(
                f"Ollama returned an error: {exc.response.status_code}"
            ) from exc
        except httpx.HTTPError as exc:
            raise OllamaServiceError("Unexpected Ollama communication error") from exc

        try:
            data = response.json()
        except JSONDecodeError as exc:
            raise OllamaServiceError("Ollama returned invalid JSON") from exc

        if not isinstance(data, dict):
            raise OllamaServiceError("Ollama returned an unexpected response format")

        return self._parse_response(data)

    @staticmethod
    def _parse_response(data: dict[str, Any]) -> str:
        generated_text = data.get("response")

        if not isinstance(generated_text, str):
            raise OllamaServiceError("Ollama response is missing generated text")

        return generated_text


def get_ollama_service() -> OllamaService:
    return OllamaService(get_settings())
