from __future__ import annotations

from collections.abc import Sequence

from xauusd_trading.models.trading import ExecutedTrade


def summarize_trades(trades: Sequence[ExecutedTrade], *, initial_balance: float = 10_000.0) -> dict[str, float]:
    total_trades = len(trades)
    wins = [trade for trade in trades if trade.pnl_currency > 0]
    losses = [trade for trade in trades if trade.pnl_currency <= 0]

    win_rate = (len(wins) / total_trades * 100) if total_trades else 0.0
    avg_win = (sum(trade.pnl_pct for trade in wins) / len(wins)) if wins else 0.0
    avg_loss = (sum(trade.pnl_pct for trade in losses) / len(losses)) if losses else 0.0
    gross_profit = sum(trade.pnl_currency for trade in wins)
    gross_loss = abs(sum(trade.pnl_currency for trade in losses))
    profit_factor = (gross_profit / gross_loss) if gross_loss else 0.0
    ending_balance = trades[-1].equity_after if trades else initial_balance
    total_return_pct = ((ending_balance / initial_balance) - 1) * 100 if initial_balance else 0.0

    peak_balance = initial_balance
    max_drawdown_pct = 0.0
    for trade in trades:
        peak_balance = max(peak_balance, trade.equity_after)
        if peak_balance > 0:
            drawdown_pct = ((peak_balance - trade.equity_after) / peak_balance) * 100
            max_drawdown_pct = max(max_drawdown_pct, drawdown_pct)

    return {
        "trades": float(total_trades),
        "win_rate_pct": win_rate,
        "avg_win_pct": avg_win,
        "avg_loss_pct": avg_loss,
        "profit_factor": profit_factor,
        "ending_balance": ending_balance,
        "total_return_pct": total_return_pct,
        "max_drawdown_pct": max_drawdown_pct,
    }
