from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.routers.chat import router as chat_router
from app.services.ollama_service import OllamaConnectionError, OllamaServiceError

app = FastAPI(
    title="AI Assistant API",
    version="1.0.0",
    description="A FastAPI backend for an AI assistant powered by a local Ollama model.",
)


@app.exception_handler(OllamaConnectionError)
async def ollama_connection_exception_handler(
    request: Request,
    exc: OllamaConnectionError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"detail": str(exc)},
    )


@app.exception_handler(OllamaServiceError)
async def ollama_service_exception_handler(
    request: Request,
    exc: OllamaServiceError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": str(exc)},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.errors()},
    )


@app.get(
    "/",
    summary="Health check",
    description="Returns a simple message confirming that the API is running.",
)
async def root():
    return {
        "message": "AI Assistant API is running"
    }


app.include_router(chat_router)
