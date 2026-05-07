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


def _fmt_side(side: str) -> str:
    if side == "LONG":
        return "🟢 LONG"
    if side == "SHORT":
        return "🔴 SHORT"
    return side


def _fmt_pips(price_diff: float, pip_size: float) -> str:
    if pip_size <= 0:
        return "?"
    return f"{abs(price_diff) / pip_size:.1f} pips"


def _fmt_branch(branch_id: str) -> str:
    icons = {
        "eurusd_sweep": "⚡",
        "gbpusd_orb": "📊",
        "eurusd_orb": "📊",
        "xauusd_continuation": "🥇",
    }
    return f"{icons.get(branch_id, '📈')} {branch_id}"


def format_paper_trade_event(event: dict[str, Any]) -> str:
    event_type = event.get("type", "EVENT")
    if event_type == "RAW_MESSAGE":
        return str(event.get("text", ""))

    if event_type == "OPEN":
        position = event.get("position", {})
        side = position.get("side", "?")
        entry = float(position.get("entry_price", 0))
        sl = float(position.get("stop_loss", 0))
        tp = float(position.get("take_profit", 0))
        pip_size = float(position.get("pip_size", 0.0001))
        branch = position.get("strategy", "?")
        symbol = position.get("symbol", "?")
        risk_pips = _fmt_pips(entry - sl, pip_size) if side == "LONG" else _fmt_pips(sl - entry, pip_size)
        rr = abs(entry - tp) / abs(entry - sl) if abs(entry - sl) > 0 else 0

        return (
            f"{'━' * 28}\n"
            f"📥 <b>TRADE OPENED</b>\n"
            f"{'━' * 28}\n"
            f"{_fmt_side(side)}  <b>{symbol}</b>\n"
            f"{_fmt_branch(branch)}\n"
            f"\n"
            f"💰 Entry: <code>{entry:.5f}</code>\n"
            f"🛑 SL: <code>{sl:.5f}</code> ({risk_pips})\n"
            f"🎯 TP: <code>{tp:.5f}</code> (R:R {rr:.1f})\n"
            f"🕐 Time: <code>{position.get('entry_time', '?')}</code>"
        )

    if event_type == "CLOSE":
        pnl_currency = float(event.get("pnl_currency", 0.0))
        pnl_pct = float(event.get("pnl_pct", 0.0))
        emoji = "🟢" if pnl_currency > 0 else "🔴" if pnl_currency < 0 else "⚪"
        side = event.get("side", "?")
        symbol = event.get("symbol", "?")
        equity = float(event.get("equity_after", 0.0))

        return (
            f"{'━' * 28}\n"
            f"{emoji} <b>TRADE CLOSED</b>\n"
            f"{'━' * 28}\n"
            f"{_fmt_side(side)}  <b>{symbol}</b>\n"
            f"{_fmt_branch(event.get('strategy', '?'))}\n"
            f"\n"
            f"💵 PnL: <b>{pnl_currency:+.2f}</b> ({pnl_pct:+.2f}%)\n"
            f"📊 Exit: <code>{event.get('exit_reason', '?')}</code>\n"
            f"💰 Equity: <code>{equity:.2f}</code>\n"
            f"🕐 Time: <code>{event.get('exit_time', '?')}</code>"
        )

    if event_type == "EXECUTION_DECISION":
        action = event.get("action", "?")
        reason = event.get("reason", "?")
        symbol = event.get("symbol", "?")
        intent = event.get("intent", {})
        send_result = event.get("send_result", {})
        broker_positions = event.get("broker_positions", [])
        metadata = event.get("metadata", {})
        branch_debugs = metadata.get("branch_debugs", [])

        # ── Decision header ──
        if action == "OPEN":
            side = intent.get("side", "?")
            entry = float(intent.get("entry_price", 0))
            sl = float(intent.get("stop_loss", 0))
            tp = float(intent.get("take_profit", 0))
            volume = float(intent.get("volume", 0))
            intent_meta = intent.get("metadata", {})
            pip_size = float(intent_meta.get("pip_size", 0.0001))
            branch_id = intent_meta.get("branch_id", "?")
            risk_pct = float(intent_meta.get("risk_per_trade", 0))
            rr = abs(entry - tp) / abs(entry - sl) if abs(entry - sl) > 0 else 0
            risk_pips = _fmt_pips(abs(entry - sl), pip_size)
            sent = send_result.get("sent", False)
            retcode = send_result.get("retcode", -1)
            mode = send_result.get("mode", "?")

            status_emoji = "✅" if sent else "❌"
            status_text = f"{status_emoji} ORDER {'FILLED' if sent else 'REJECTED'}"
            if not sent:
                status_text += f" (retcode {retcode})"

            return (
                f"{'━' * 28}\n"
                f"📥 <b>LIVE ORDER</b>\n"
                f"{'━' * 28}\n"
                f"{_fmt_side(side)}  <b>{symbol}</b>  ×{volume:.2f} lot\n"
                f"{_fmt_branch(branch_id)}  (risk {risk_pct*100:.1f}%)\n"
                f"\n"
                f"💰 Entry: <code>{entry:.5f}</code>\n"
                f"🛑 SL: <code>{sl:.5f}</code> ({risk_pips})\n"
                f"🎯 TP: <code>{tp:.5f}</code> (R:R {rr:.1f})\n"
                f"\n"
                f"{status_text} [{mode}]\n"
                f"🕐 Time: <code>{intent_meta.get('timestamp', '?')}</code>"
            )

        if action in ("HOLD", "MANAGE_POSITION", "SYNC_SLTP", "REVERSE"):
            pos_text = ""
            if broker_positions:
                for pos in broker_positions:
                    p_side = pos.get("side", "?")
                    p_vol = float(pos.get("volume", 0))
                    p_pnl = float(pos.get("profit", 0))
                    pnl_emoji = "🟢" if p_pnl >= 0 else "🔴"
                    pos_text += f"\n  {pnl_emoji} {_fmt_side(p_side)} ×{p_vol:.2f} lot (PnL: {p_pnl:+.2f})"

            # Branch debug summary
            debug_text = ""
            for bd in branch_debugs:
                bid = bd.get("branch_id", "?")
                rc = bd.get("reason_code", "?")
                icon = "✅" if bd.get("has_signal") else "⏳"
                debug_text += f"\n  {icon} {_fmt_branch(bid)}: {rc}"

            return (
                f"{'━' * 28}\n"
                f"⏸ <b>{action}</b> — {reason}\n"
                f"{'━' * 28}\n"
                f"📊 <b>{symbol}</b>\n"
                f"\n"
                f"<b>Positions:</b>{pos_text or ' None'}\n"
                f"\n"
                f"<b>Branches:</b>{debug_text or ' None'}"
            )

        # Fallback for unknown action
        return (
            f"{'━' * 28}\n"
            f"⚙️ <b>{action}</b>\n"
            f"{'━' * 28}\n"
            f"Symbol: <b>{symbol}</b>\n"
            f"Reason: <code>{reason}</code>"
        )

    # Fallback for unknown event type
    return f"<b>Event</b>\n<pre>{json.dumps(event, indent=2, default=str)[:800]}</pre>"


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
