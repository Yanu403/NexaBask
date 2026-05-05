from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from xauusd_trading.models.trading import ExecutedTrade


def _serialize_trade(trade: ExecutedTrade) -> dict[str, Any]:
    payload = asdict(trade)
    payload["entry_time"] = trade.entry_time.isoformat()
    payload["exit_time"] = trade.exit_time.isoformat()
    return payload


def export_trade_ledger(trades: list[ExecutedTrade], path: str | Path) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.suffix.lower() == ".json":
        output_path.write_text(json.dumps([_serialize_trade(trade) for trade in trades], indent=2))
        return output_path

    if output_path.suffix.lower() == ".csv":
        rows = [_serialize_trade(trade) for trade in trades]
        if not rows:
            output_path.write_text("")
            return output_path

        headers = list(rows[0].keys())
        with output_path.open("w", encoding="utf-8") as handle:
            handle.write(",".join(headers) + "\n")
            for row in rows:
                values = [json.dumps(row.get(header, "")) if isinstance(row.get(header), (dict, list)) else str(row.get(header, "")) for header in headers]
                handle.write(",".join(values) + "\n")
        return output_path

    raise ValueError(f"Unsupported ledger format: {output_path.suffix}")
