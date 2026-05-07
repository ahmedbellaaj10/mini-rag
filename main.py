from fastapi import FastAPI

app = FastAPI()


@app.get("/welcome")
async def read_root() -> dict[str, str]:
    return {"message": "Welcome to mini-RAG!"}
