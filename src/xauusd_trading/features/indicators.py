from __future__ import annotations

import numpy as np
import pandas as pd


def add_ema_columns(df: pd.DataFrame, spans: tuple[int, ...] = (20, 50, 200)) -> pd.DataFrame:
    result = df.copy()
    for span in spans:
        result[f"ema{span}"] = result["close"].ewm(span=span, adjust=False).mean()
    return result


def add_atr_column(df: pd.DataFrame, period: int = 14, column_name: str = "atr14") -> pd.DataFrame:
    result = df.copy()
    prev_close = result["close"].shift(1)
    tr1 = result["high"] - result["low"]
    tr2 = (result["high"] - prev_close).abs()
    tr3 = (result["low"] - prev_close).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    # Wilder's smoothing: first ATR = SMA of first `period` TRs, then exponential
    atr = pd.Series(np.nan, index=result.index, dtype=float)
    first_valid = tr.iloc[period - 1] if len(tr) >= period else np.nan
    if not np.isnan(first_valid):
        atr.iloc[period - 1] = tr.iloc[:period].mean()
        for i in range(period, len(atr)):
            atr.iloc[i] = (atr.iloc[i - 1] * (period - 1) + tr.iloc[i]) / period
    result[column_name] = atr
    return result


def add_rsi_column(df: pd.DataFrame, period: int = 14, column_name: str = "rsi14") -> pd.DataFrame:
    result = df.copy()
    delta = result["close"].diff()
    gain_raw = delta.clip(lower=0)
    loss_raw = (-delta.clip(upper=0))
    # Wilder's smoothing: first avg = SMA of first `period` values, then exponential
    avg_gain = pd.Series(np.nan, index=result.index, dtype=float)
    avg_loss = pd.Series(np.nan, index=result.index, dtype=float)
    if len(gain_raw) >= period:
        avg_gain.iloc[period] = gain_raw.iloc[1:period + 1].mean()
        avg_loss.iloc[period] = loss_raw.iloc[1:period + 1].mean()
        for i in range(period + 1, len(avg_gain)):
            avg_gain.iloc[i] = (avg_gain.iloc[i - 1] * (period - 1) + gain_raw.iloc[i]) / period
            avg_loss.iloc[i] = (avg_loss.iloc[i - 1] * (period - 1) + loss_raw.iloc[i]) / period
    # RSI: if avg_loss is zero, RSI = 100 (all gains, no losses)
    rs = avg_gain / avg_loss.replace(0, np.nan)
    result[column_name] = 100 - (100 / (1 + rs))
    result[column_name] = result[column_name].where(avg_loss != 0, 100.0)
    return result


def add_session_columns(df: pd.DataFrame, *, timezone_offset_hours: int = 7) -> pd.DataFrame:
    result = df.copy()
    result["hour_utc"] = result.index.hour
    result["hour_local"] = (result["hour_utc"] + timezone_offset_hours) % 24
    result["is_london_ny"] = result["hour_local"].isin([14, 15, 16, 17, 18, 19, 20, 21]).astype(int)
    return result


def build_tf001_feature_frame(df: pd.DataFrame) -> pd.DataFrame:
    result = add_ema_columns(df)
    result = add_atr_column(result)
    result = add_rsi_column(result)
    result = add_session_columns(result)
    result["bullish_candle"] = (result["close"] > result["open"]).astype(int)
    result["price_vs_ema20_atr"] = (result["close"] - result["ema20"]).abs() / result["atr14"].clip(lower=0.01)
    return result
