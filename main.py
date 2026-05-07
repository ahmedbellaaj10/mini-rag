from fastapi import FastAPI

app: FastAPI = FastAPI()


@app.get("/welcome")
async def read_root() -> dict[str, str]:
    return {"message": "Welcome to mini-RAG!"}
