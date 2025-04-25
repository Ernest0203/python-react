from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from io import StringIO
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

router = APIRouter()

@router.post("/predict")
async def predict_from_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")

    try:
        contents = await file.read()
        decoded = contents.decode("utf-8")
        df = pd.read_csv(StringIO(decoded))

        if "salary" not in df.columns:
            raise HTTPException(status_code=400, detail="Column 'salary' is required for prediction")

        # Только числовые признаки (исключаем salary)
        feature_cols = df.select_dtypes(include=np.number).drop(columns=["salary"], errors="ignore").columns.tolist()
        if not feature_cols:
            raise HTTPException(status_code=400, detail="No valid numeric features found")

        X = df[feature_cols]
        y = df["salary"]

        # Обучение модели
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = LinearRegression()
        model.fit(X_train, y_train)
        predictions = model.predict(X)

        result = {
            "features": feature_cols,
            "actual": y.tolist(),
            "predicted": predictions.tolist()
        }

        return JSONResponse(content=jsonable_encoder(result))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
