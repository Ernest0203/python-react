from fastapi import FastAPI
from routes import todos
from auth.routes import router as auth_router
from database import db

app = FastAPI()

app.include_router(todos.router)
app.include_router(auth_router, prefix="/auth")

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI"}
