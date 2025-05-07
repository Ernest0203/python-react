# routes/crypto_predict.py
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from pybit.unified_trading import HTTP
from datetime import datetime, timedelta
import time
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
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

        X, y = [], []
        for i in range(len(df) - forecast_horizon):
            X.append(df[features].iloc[i].values)
            y.append(df["close"].iloc[i + 1:i + 1 + forecast_horizon].values)

        X = np.array(X)
        y = np.array(y)

        # Random Forest
        rf = RandomForestRegressor(n_estimators=100, random_state=42)
        rf.fit(X, y)
        rf_pred = rf.predict([df[features].iloc[-1].values])[0].tolist()

        # XGBoost
        xgb = XGBRegressor(n_estimators=100, random_state=42)
        xgb.fit(X, y)
        xgb_pred = xgb.predict([df[features].iloc[-1].values])[0].tolist()

        result = {
            "symbol": symbol,
            "interval": interval,
            "last_close": float(df["close"].iloc[-1]),
            "random_forest": [float(p) for p in rf_pred],
            "xgboost": [float(p) for p in xgb_pred]
        }

        return JSONResponse(content=result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
