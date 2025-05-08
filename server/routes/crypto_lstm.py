from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from pybit.unified_trading import HTTP
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import joblib
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
from pathlib import Path
import os

from ta.momentum import RSIIndicator, ROCIndicator, StochasticOscillator
from ta.trend import MACD, EMAIndicator
from ta.volume import OnBalanceVolumeIndicator
from ta.volatility import BollingerBands

router = APIRouter()
session = HTTP(testnet=False)

@router.get("/crypto/lstm")
def predict_lstm(
    symbol: str = Query(...),
    interval: str = Query("60"),
    days: int = Query(100)
):
    try:
        # Пути
        model_dir = Path("models")
        model_dir.mkdir(exist_ok=True)
        model_path = model_dir / f"lstm_{symbol}_{interval}.h5"
        scaler_path = model_dir / f"lstm_scaler_{symbol}_{interval}.pkl"

        seq_length = 10
        forecast_horizon = 5
        retrain_model = True

        # Проверка актуальности модели
        if model_path.exists():
            modified_time = datetime.fromtimestamp(model_path.stat().st_mtime)
            if datetime.utcnow() - modified_time < timedelta(hours=24):
                retrain_model = False

        # Получение данных
        interval_minutes = int(interval)
        end_time_dt = datetime.utcnow() - timedelta(minutes=interval_minutes)
        end_time = int(end_time_dt.timestamp() * 1000)
        start_time = int((end_time_dt - timedelta(days=days)).timestamp() * 1000)

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
            raise ValueError("No candles returned")

        df = pd.DataFrame([{
            "timestamp": int(c[0]),
            "open": float(c[1]),
            "high": float(c[2]),
            "low": float(c[3]),
            "close": float(c[4]),
            "volume": float(c[5]),
        } for c in reversed(candles)])

        # Индикаторы
        df["rsi"] = RSIIndicator(df["close"]).rsi()
        df["macd"] = MACD(df["close"]).macd()
        df["ema"] = EMAIndicator(df["close"]).ema_indicator()
        df["hl_range"] = df["high"] - df["low"]
        df["rsi_diff"] = df["rsi"].diff()
        df["roc"] = ROCIndicator(df["close"]).roc()
        df["stoch"] = StochasticOscillator(df["high"], df["low"], df["close"]).stoch()
        df["obv"] = OnBalanceVolumeIndicator(df["close"], df["volume"]).on_balance_volume()
        bb = BollingerBands(close=df["close"])
        df["bb_width"] = bb.bollinger_hband() - bb.bollinger_lband()
        df.dropna(inplace=True)

        features = ["close", "rsi", "macd", "ema", "volume", "hl_range", "rsi_diff", "roc", "stoch", "obv", "bb_width"]

        if retrain_model:
            scaler = MinMaxScaler()
            scaled = scaler.fit_transform(df[features])
            joblib.dump(scaler, scaler_path)

            X, y = [], []
            for i in range(len(scaled) - seq_length - forecast_horizon):
                X.append(scaled[i:i + seq_length])
                y.append(scaled[i + seq_length:i + seq_length + forecast_horizon, 0])
            X, y = np.array(X), np.array(y)

            model = Sequential()
            model.add(LSTM(64, input_shape=(X.shape[1], X.shape[2])))
            model.add(Dense(forecast_horizon))
            model.compile(loss="mse", optimizer="adam")
            model.fit(X, y, epochs=30, batch_size=16, shuffle=False, verbose=0)
            model.save(model_path)
        else:
            model = load_model(model_path, compile=False)
            model.compile(loss="mse", optimizer="adam")
            scaler = joblib.load(scaler_path)

        # Прогноз
        last_sequence = df[features].iloc[-seq_length:].values
        last_scaled = scaler.transform(last_sequence)
        input_seq = np.expand_dims(last_scaled, axis=0)

        pred_scaled = model.predict(input_seq, verbose=0)[0]
        pred_full = np.hstack([
            pred_scaled.reshape(-1, 1),
            np.zeros((len(pred_scaled), len(features) - 1))
        ])
        pred_close = scaler.inverse_transform(pred_full)[:, 0]
        last_close = df["close"].iloc[-1]

        return JSONResponse(content={
            "symbol": symbol,
            "interval": interval,
            "last_close": float(last_close),
            "lstm_prediction": [float(p) for p in pred_close],
            "model_retrained": retrain_model
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LSTM prediction failed: {str(e)}")
