from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import todos, analysis, predict, analyze_img, blur_faces, ocr, crypto, crypto_lstm
from auth.routes import router as auth_router
from database import db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(todos.router)
app.include_router(analysis.router)
app.include_router(predict.router)
app.include_router(analyze_img.router)
app.include_router(blur_faces.router)
app.include_router(ocr.router)
app.include_router(crypto.router)
app.include_router(crypto_lstm.router)
app.include_router(auth_router, prefix="/auth")

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI"}
