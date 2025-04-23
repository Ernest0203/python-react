from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import pandas as pd
from io import StringIO
import numpy as np

router = APIRouter()


@router.post("/analyze")
async def analyze_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")

    try:
        # Чтение байтов и декодировка
        contents = await file.read()
        decoded = contents.decode("utf-8")

        # Преобразуем в DataFrame
        df = pd.read_csv(StringIO(decoded))

        # Заменяем NaN и Inf на None (Python null → JSON null)
        df_clean = df.replace([np.nan, float('inf'), -float('inf')], None)

        # Анализ — можно заменить на свою метрику
        summary = df_clean.describe(include='all').to_dict()

        # Преобразуем summary, чтобы избавиться от неприемлемых типов
        def clean_summary(value):
            # Проверяем на NaN, Inf и заменяем на None
            if isinstance(value, (float, int)) and (np.isnan(value) or value == float('inf') or value == -float('inf')):
                return None
            return value

        # Обрабатываем каждый элемент в summary
        summary_clean = {
            key: {k: clean_summary(v) for k, v in value.items()} 
            for key, value in summary.items()
        }

        # Возврат безопасного JSON
        response = {
            "filename": file.filename,
            "columns": df_clean.columns.tolist(),
            "summary": summary_clean
        }

        return JSONResponse(content=jsonable_encoder(response))

    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="Failed to decode file. Please upload UTF-8 CSV.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
