# from fastapi import APIRouter, UploadFile, File, HTTPException
# from fastapi.responses import JSONResponse
# from fastapi.encoders import jsonable_encoder
# import pandas as pd
# from io import StringIO
# import numpy as np

# router = APIRouter()

# @router.post("/analyze")
# async def analyze_csv(file: UploadFile = File(...)):
#     if not file.filename.endswith(".csv"):
#         raise HTTPException(status_code=400, detail="Only CSV files are supported")

#     try:
#         contents = await file.read()
#         decoded = contents.decode("utf-8")
#         df = pd.read_csv(StringIO(decoded))

#         df_clean = df.replace([np.nan, float('inf'), -float('inf')], None)

#         # Статистика describe()
#         summary = df_clean.describe(include='all').to_dict()

#         def clean_summary(value):
#             if isinstance(value, (float, int)) and (np.isnan(value) or value in [float('inf'), -float('inf')]):
#                 return None
#             return value

#         summary_clean = {
#             key: {k: clean_summary(v) for k, v in value.items()}
#             for key, value in summary.items()
#         }

#         salary_by_department = {}
#         if 'salary' in df.columns and 'department' in df.columns:
#             salary_grouped = df.groupby("department")["salary"].mean().round(2)
#             salary_by_department = salary_grouped.to_dict()

#         response = {
#             "filename": file.filename,
#             "columns": df_clean.columns.tolist(),
#             "summary": summary_clean,
#             "salaryByDepartment": salary_by_department  # 👈 добавлено
#         }

#         return JSONResponse(content=jsonable_encoder(response))

#     except UnicodeDecodeError:
#         raise HTTPException(status_code=400, detail="Failed to decode file. Please upload UTF-8 CSV.")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


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

        # Сводная статистика
        summary = df_clean.describe(include='all').to_dict()

        # Подготовка данных для визуализации: salary vs years_experience и age vs salary
        chart_data = {
            "salary_vs_experience": df_clean[["salary", "years_experience"]].dropna().to_dict(orient="records"),
            "salary_vs_age": df_clean[["salary", "age"]].dropna().to_dict(orient="records")
        }

        # Обработка summary для JSON
        def clean_summary(value):
            if isinstance(value, (float, int)) and (np.isnan(value) or value == float('inf') or value == -float('inf')):
                return None
            return value

        summary_clean = {
            key: {k: clean_summary(v) for k, v in value.items()} 
            for key, value in summary.items()
        }

        response = {
            "filename": file.filename,
            "columns": df_clean.columns.tolist(),
            "summary": summary_clean,
            "charts": chart_data
        }

        return JSONResponse(content=jsonable_encoder(response))

    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="Failed to decode file. Please upload UTF-8 CSV.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
