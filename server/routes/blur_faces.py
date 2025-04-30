from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
import face_recognition
from PIL import Image
import numpy as np
from io import BytesIO

router = APIRouter()

@router.post("/blur_faces")
async def blur_faces(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    image_bytes = await file.read()

    # Загружаем изображение и распознаем лица
    image_np = face_recognition.load_image_file(BytesIO(image_bytes))
    face_locations = face_recognition.face_locations(image_np)

    pil_image = Image.fromarray(image_np)
    for top, right, bottom, left in face_locations:
        face_region = pil_image.crop((left, top, right, bottom)).resize((10, 10), Image.Resampling.BILINEAR)
        face_region = face_region.resize((right - left, bottom - top), Image.Resampling.NEAREST)
        pil_image.paste(face_region, (left, top))

    # Сохраняем в память
    output_buffer = BytesIO()
    pil_image.save(output_buffer, format="PNG")
    output_buffer.seek(0)

    return StreamingResponse(output_buffer, media_type="image/png")
