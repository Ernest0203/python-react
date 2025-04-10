from fastapi import FastAPI
from routes import todos
from database import db

app = FastAPI()

app.include_router(todos.router)

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI"}
