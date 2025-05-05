from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image, ImageOps
import pytesseract
from io import BytesIO

router = APIRouter()

@router.post("/ocr")
async def extract_text(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are supported")

    try:
        image_data = await file.read()
        image = Image.open(BytesIO(image_data))

        # Предобработка
        image = image.convert("L")  # преобразуем в оттенки серого
        image = ImageOps.invert(image)  # инвертируем (тёмный текст на светлом фоне)
        image = image.point(lambda x: 0 if x < 140 else 255, mode='1')  # бинаризация

        # Распознавание с указанием языка
        text = pytesseract.image_to_string(image, lang="rus+eng")

        return JSONResponse(content={"filename": file.filename, "text": text.strip()})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process image: {str(e)}")
