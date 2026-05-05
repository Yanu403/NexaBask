from __future__ import annotations

import json
import ssl
import sys
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class TelegramAlertConfig:
    bot_token: str
    chat_id: str
    parse_mode: str = "HTML"
    disable_web_preview: bool = True
    insecure_ssl: bool = False


def format_paper_trade_event(event: dict[str, Any]) -> str:
    event_type = event.get("type", "EVENT")
    if event_type == "RAW_MESSAGE":
        return str(event.get("text", ""))

    if event_type == "OPEN":
        position = event.get("position", {})
        return (
            "<b>Paper Trade OPEN</b>\n"
            f"Strategy: <code>{position.get('strategy')}</code>\n"
            f"Side: <b>{position.get('side')}</b>\n"
            f"Entry: <code>{position.get('entry_price')}</code>\n"
            f"SL: <code>{position.get('stop_loss')}</code>\n"
            f"TP: <code>{position.get('take_profit')}</code>\n"
            f"Time: <code>{position.get('entry_time')}</code>"
        )

    if event_type == "CLOSE":
        pnl_currency = float(event.get("pnl_currency", 0.0))
        emoji = "🟢" if pnl_currency > 0 else "🔴"
        return (
            f"<b>{emoji} Paper Trade CLOSE</b>\n"
            f"Strategy: <code>{event.get('strategy')}</code>\n"
            f"Side: <b>{event.get('side')}</b>\n"
            f"Exit reason: <code>{event.get('exit_reason')}</code>\n"
            f"PnL: <code>{pnl_currency:.2f}</code>\n"
            f"PnL %: <code>{float(event.get('pnl_pct', 0.0)):.2f}%</code>\n"
            f"Equity: <code>{float(event.get('equity_after', 0.0)):.2f}</code>\n"
            f"Exit time: <code>{event.get('exit_time')}</code>"
        )

    if event_type == "EXECUTION_DECISION":
        return "<b>MT5 Execution Decision</b>\n<pre>" + json.dumps(event, indent=2, default=str) + "</pre>"

    return f"<b>Paper Trade Event</b>\n<pre>{json.dumps(event, indent=2, default=str)}</pre>"


def send_telegram_message(config: TelegramAlertConfig, text: str) -> None:
    payload = urllib.parse.urlencode(
        {
            "chat_id": config.chat_id,
            "text": text,
            "parse_mode": config.parse_mode,
            "disable_web_page_preview": "true" if config.disable_web_preview else "false",
        }
    ).encode("utf-8")
    url = f"https://api.telegram.org/bot{config.bot_token}/sendMessage"
    request = urllib.request.Request(url, data=payload, method="POST")
    context = None
    if config.insecure_ssl:
        context = ssl._create_unverified_context()
    with urllib.request.urlopen(request, timeout=20, context=context) as response:
        response.read()


def dispatch_telegram_alerts(config: TelegramAlertConfig, events: list[dict[str, Any]]) -> int:
    sent = 0
    for event in events:
        try:
            send_telegram_message(config, format_paper_trade_event(event))
            sent += 1
        except Exception as exc:
            print(f"[WARN] Telegram alert failed: {exc}", file=sys.stderr)
    return sent
