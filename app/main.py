from fastapi import FastAPI

app = FastAPI(
    title="AI Assistant API",
    version="1.0.0"
)


@app.get("/")
async def root():
    return {
        "message": "AI Assistant API is running"
    }