from __future__ import annotations

import pandas as pd

from xauusd_trading.models.trading import TradeSignal


def simulate_long_with_optional_trailing(
    df: pd.DataFrame,
    signal: TradeSignal,
    *,
    trailing_atr_multiple: float | None = None,
    partial_tp_rr: float | None = None,
    partial_close_fraction: float = 0.5,
    move_stop_to_breakeven_on_partial: bool = True,
    default_exit_index: int,
) -> tuple[float, str, int, dict]:
    take_profit_half = signal.entry_price + (signal.take_profit - signal.entry_price) * 0.5
    trailing_stop = signal.stop_loss
    trailing_active = False
    partial_taken = False
    partial_exit_price = None
    partial_exit_index = None
    stop_distance = abs(signal.entry_price - signal.stop_loss)
    partial_tp_price = signal.entry_price + stop_distance * partial_tp_rr if partial_tp_rr is not None else None

    # FIX 4: Use previous bar's close for trailing update; start with signal bar's close
    prev_close = float(df.iloc[signal.index]["close"])

    for index in range(signal.index + 1, min(signal.index + signal.max_hold_bars + 1, len(df))):
        future_row = df.iloc[index]
        high = float(future_row["high"])
        low = float(future_row["low"])
        current_close = float(future_row["close"])

        # FIX 4: Use previous bar's close to update trailing stop (before checking current bar)
        if trailing_active and trailing_atr_multiple is not None:
            atr_value = float(future_row.get("atr14", 0.0))
            if atr_value > 0:
                trailing_stop = max(trailing_stop, prev_close - atr_value * trailing_atr_multiple)

        # FIX 3: Conservative — check SL first; if both TP and SL trigger in same bar, assume SL hits first
        sl_hit = low <= trailing_stop
        tp_would_hit = high >= signal.take_profit

        if sl_hit:
            if partial_taken and partial_exit_price is not None:
                effective_exit = partial_close_fraction * partial_exit_price + (1 - partial_close_fraction) * trailing_stop
                final_reason = "TRAIL" if trailing_stop > signal.stop_loss else "SL_HIT"
                return effective_exit, f"PARTIAL_TP+{final_reason}", index, {
                    "partial_taken": True,
                    "partial_exit_price": partial_exit_price,
                    "partial_exit_index": partial_exit_index,
                    "final_exit_price": trailing_stop,
                    "final_exit_reason": final_reason,
                }
            if trailing_active and trailing_stop > signal.stop_loss:
                return trailing_stop, "TRAIL", index, {"partial_taken": False}
            return trailing_stop, "SL_HIT", index, {"partial_taken": False}

        # Partial TP (only checked if SL not hit)
        if not partial_taken and partial_tp_price is not None and high >= partial_tp_price:
            partial_taken = True
            partial_exit_price = partial_tp_price
            partial_exit_index = index
            if move_stop_to_breakeven_on_partial:
                trailing_stop = max(trailing_stop, signal.entry_price)
            trailing_active = True

        # Full TP (only checked if SL not hit — FIX 3)
        if tp_would_hit:
            if partial_taken and partial_exit_price is not None:
                effective_exit = partial_close_fraction * partial_exit_price + (1 - partial_close_fraction) * signal.take_profit
                return effective_exit, "PARTIAL_TP+TP", index, {
                    "partial_taken": True,
                    "partial_exit_price": partial_exit_price,
                    "partial_exit_index": partial_exit_index,
                    "final_exit_price": signal.take_profit,
                    "final_exit_reason": "TP_HIT",
                }
            return signal.take_profit, "TP_HIT", index, {"partial_taken": False}

        # Trailing activation (for future bars)
        if trailing_atr_multiple is not None and high >= take_profit_half:
            trailing_active = True

        # FIX 4: Store current close for next iteration's trailing update
        prev_close = current_close

    timeout_price = float(df.iloc[default_exit_index]["close"])
    if partial_taken and partial_exit_price is not None:
        effective_exit = partial_close_fraction * partial_exit_price + (1 - partial_close_fraction) * timeout_price
        return effective_exit, "PARTIAL_TP+TIMEOUT", default_exit_index, {
            "partial_taken": True,
            "partial_exit_price": partial_exit_price,
            "partial_exit_index": partial_exit_index,
            "final_exit_price": timeout_price,
            "final_exit_reason": "TIMEOUT",
        }
    return timeout_price, "TIMEOUT", default_exit_index, {"partial_taken": False}


def simulate_short_with_optional_trailing(
    df: pd.DataFrame,
    signal: TradeSignal,
    *,
    trailing_atr_multiple: float | None = None,
    partial_tp_rr: float | None = None,
    partial_close_fraction: float = 0.5,
    move_stop_to_breakeven_on_partial: bool = True,
    default_exit_index: int,
) -> tuple[float, str, int, dict]:
    take_profit_half = signal.entry_price - (signal.entry_price - signal.take_profit) * 0.5
    trailing_stop = signal.stop_loss
    trailing_active = False
    partial_taken = False
    partial_exit_price = None
    partial_exit_index = None
    stop_distance = abs(signal.entry_price - signal.stop_loss)
    partial_tp_price = signal.entry_price - stop_distance * partial_tp_rr if partial_tp_rr is not None else None

    # FIX 4: Use previous bar's close for trailing update; start with signal bar's close
    prev_close = float(df.iloc[signal.index]["close"])

    for index in range(signal.index + 1, min(signal.index + signal.max_hold_bars + 1, len(df))):
        future_row = df.iloc[index]
        high = float(future_row["high"])
        low = float(future_row["low"])
        current_close = float(future_row["close"])

        # FIX 4: Use previous bar's close to update trailing stop (before checking current bar)
        if trailing_active and trailing_atr_multiple is not None:
            atr_value = float(future_row.get("atr14", 0.0))
            if atr_value > 0:
                trailing_stop = min(trailing_stop, prev_close + atr_value * trailing_atr_multiple)

        # FIX 3: Conservative — check SL first; if both TP and SL trigger in same bar, assume SL hits first
        sl_hit = high >= trailing_stop
        tp_would_hit = low <= signal.take_profit

        if sl_hit:
            if partial_taken and partial_exit_price is not None:
                effective_exit = partial_close_fraction * partial_exit_price + (1 - partial_close_fraction) * trailing_stop
                final_reason = "TRAIL" if trailing_stop < signal.stop_loss else "SL_HIT"
                return effective_exit, f"PARTIAL_TP+{final_reason}", index, {
                    "partial_taken": True,
                    "partial_exit_price": partial_exit_price,
                    "partial_exit_index": partial_exit_index,
                    "final_exit_price": trailing_stop,
                    "final_exit_reason": final_reason,
                }
            if trailing_active and trailing_stop < signal.stop_loss:
                return trailing_stop, "TRAIL", index, {"partial_taken": False}
            return trailing_stop, "SL_HIT", index, {"partial_taken": False}

        # Partial TP (only checked if SL not hit)
        if not partial_taken and partial_tp_price is not None and low <= partial_tp_price:
            partial_taken = True
            partial_exit_price = partial_tp_price
            partial_exit_index = index
            if move_stop_to_breakeven_on_partial:
                trailing_stop = min(trailing_stop, signal.entry_price)
            trailing_active = True

        # Full TP (only checked if SL not hit — FIX 3)
        if tp_would_hit:
            if partial_taken and partial_exit_price is not None:
                effective_exit = partial_close_fraction * partial_exit_price + (1 - partial_close_fraction) * signal.take_profit
                return effective_exit, "PARTIAL_TP+TP", index, {
                    "partial_taken": True,
                    "partial_exit_price": partial_exit_price,
                    "partial_exit_index": partial_exit_index,
                    "final_exit_price": signal.take_profit,
                    "final_exit_reason": "TP_HIT",
                }
            return signal.take_profit, "TP_HIT", index, {"partial_taken": False}

        # Trailing activation (for future bars)
        if trailing_atr_multiple is not None and low <= take_profit_half:
            trailing_active = True

        # FIX 4: Store current close for next iteration's trailing update
        prev_close = current_close

    timeout_price = float(df.iloc[default_exit_index]["close"])
    if partial_taken and partial_exit_price is not None:
        effective_exit = partial_close_fraction * partial_exit_price + (1 - partial_close_fraction) * timeout_price
        return effective_exit, "PARTIAL_TP+TIMEOUT", default_exit_index, {
            "partial_taken": True,
            "partial_exit_price": partial_exit_price,
            "partial_exit_index": partial_exit_index,
            "final_exit_price": timeout_price,
            "final_exit_reason": "TIMEOUT",
        }
    return timeout_price, "TIMEOUT", default_exit_index, {"partial_taken": False}
