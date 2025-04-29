from fastapi import APIRouter, UploadFile, File, HTTPException
import face_recognition
import numpy as np
from io import BytesIO
from PIL import Image

router = APIRouter()

@router.post("/analyze_img")
async def detect_faces(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".png", ".jpg", ".jpeg")):
        raise HTTPException(status_code=400, detail="Only PNG/JPG images are supported.")

    try:
        contents = await file.read()
        image = np.array(Image.open(BytesIO(contents)))

        # Находим все лица
        face_locations = face_recognition.face_locations(image)

        return {
            "filename": file.filename,
            "num_faces": len(face_locations),
            "faces": face_locations  # можно передавать координаты лиц, если хочешь
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
