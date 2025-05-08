from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from pybit.unified_trading import HTTP
from datetime import datetime, timedelta
import time
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from xgboost import XGBRegressor, XGBClassifier
from sklearn.preprocessing import LabelEncoder
from ta.momentum import RSIIndicator
from ta.trend import MACD, EMAIndicator

router = APIRouter()
session = HTTP(testnet=False)

@router.get("/crypto/history")
def predict_crypto_price(
    symbol: str = Query(..., example="BTCUSDT"),
    interval: str = Query("60"),
    days: int = Query(100)
):
    try:
        end_time = int(time.time() * 1000)
        start_time = int((datetime.utcnow() - timedelta(days=days)).timestamp() * 1000)

        response = session.get_kline(
            category="linear",
            symbol=symbol,
            interval=interval,
            start=start_time,
            end=end_time,
            limit=1000
        )

        candles = response.get("result", {}).get("list", [])
        if not candles:
            raise ValueError("No data returned from Bybit")

        df = pd.DataFrame([{
            "timestamp": int(c[0]),
            "open": float(c[1]),
            "high": float(c[2]),
            "low": float(c[3]),
            "close": float(c[4]),
            "volume": float(c[5]),
        } for c in reversed(candles)])

        # Технические индикаторы
        df["rsi"] = RSIIndicator(df["close"]).rsi()
        df["macd"] = MACD(df["close"]).macd()
        df["ema"] = EMAIndicator(df["close"]).ema_indicator()

        df.dropna(inplace=True)

        features = ["close", "rsi", "macd", "ema"]
        forecast_horizon = 5

        # ---------- Регрессия: прогноз цен ----------
        X_reg, y_reg = [], []
        for i in range(len(df) - forecast_horizon):
            X_reg.append(df[features].iloc[i].values)
            y_reg.append(df["close"].iloc[i + 1:i + 1 + forecast_horizon].values)

        X_reg = np.array(X_reg)
        y_reg = np.array(y_reg)

        # Random Forest Regressor
        rf = RandomForestRegressor(n_estimators=100, random_state=42)
        rf.fit(X_reg, y_reg)
        rf_pred = rf.predict([df[features].iloc[-1].values])[0].tolist()

        # XGBoost Regressor
        xgb = XGBRegressor(n_estimators=100, random_state=42)
        xgb.fit(X_reg, y_reg)
        xgb_pred = xgb.predict([df[features].iloc[-1].values])[0].tolist()

        # ---------- Классификация: "up", "down", "stable" ----------
        df["pct_change"] = df["close"].pct_change().shift(-1)

        def classify(change, threshold=0.01):
            if change > threshold:
                return "up"
            elif change < -threshold:
                return "down"
            else:
                return "stable"

        df["label"] = df["pct_change"].apply(classify)
        df.dropna(inplace=True)

        X_cls = df[features][:-1]
        y_cls = df["label"][:-1]

        # Label Encoding
        encoder = LabelEncoder()
        y_cls_encoded = encoder.fit_transform(y_cls)

        # Random Forest Classifier
        rf_clf = RandomForestClassifier(n_estimators=100, random_state=42)
        rf_clf.fit(X_cls, y_cls_encoded)
        rf_class_encoded = rf_clf.predict([df[features].iloc[-1].values])[0]
        rf_class = encoder.inverse_transform([rf_class_encoded])[0]

        # XGBoost Classifier
        xgb_clf = XGBClassifier(n_estimators=100, use_label_encoder=False, eval_metric="mlogloss", random_state=42)
        xgb_clf.fit(X_cls, y_cls_encoded)
        xgb_class_encoded = xgb_clf.predict([df[features].iloc[-1].values])[0]
        xgb_class = encoder.inverse_transform([xgb_class_encoded])[0]

        result = {
            "symbol": symbol,
            "interval": interval,
            "last_close": float(df["close"].iloc[-1]),
            "random_forest": [float(p) for p in rf_pred],
            "xgboost": [float(p) for p in xgb_pred],
            "classification": {
                "random_forest": rf_class,
                "xgboost": xgb_class
            }
        }

        return JSONResponse(content=result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
