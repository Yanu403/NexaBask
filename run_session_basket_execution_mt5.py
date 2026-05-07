#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_CONFIG_PATH = PROJECT_ROOT / 'runtime' / 'session_basket_execution_config.json'
sys.path.insert(0, str(PROJECT_ROOT / 'src'))

from run_session_basket_demo_mt5 import (
    build_branch_specs,
    build_mt5_configs,
    collect_candidates,
    load_runtime_config,
    resolve_conflicts,
    resolve_telegram,
)
from xauusd_trading.data.mt5 import fetch_ohlcv_from_mt5
from xauusd_trading.execution.alerts import TelegramAlertConfig, dispatch_telegram_alerts
from xauusd_trading.execution.mt5_execution import MT5ExecutionAdapter, MT5ExecutionConfig
from xauusd_trading.execution.portfolio import compact_debug_summary
from xauusd_trading.execution.runtime_state import load_execution_state, prune_execution_state, save_execution_state
from xauusd_trading.models.live import ExecutionDecision
from xauusd_trading.risk.manager import RiskConfig


def build_parser(*, add_help: bool = True) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='MT5 execution runner for session basket portfolio', add_help=add_help)
    parser.add_argument('--config', default=str(DEFAULT_CONFIG_PATH))
    parser.add_argument('--execution-state-dir', default=str(PROJECT_ROOT / 'runtime' / 'session_basket_execution_states'))
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--send-telegram-alerts', action='store_true')
    parser.add_argument('--telegram-bot-token')
    parser.add_argument('--telegram-chat-id')
    parser.add_argument('--allow-live-send', action='store_true', help='Actually send requests to MT5. Default is dry-run.')
    parser.add_argument('--account-balance', type=float, default=10_000.0, help='Fallback sizing balance')
    parser.add_argument('--max-live-positions-total', type=int, default=3)
    parser.add_argument('--max-live-positions-per-symbol', type=int, default=1)
    parser.add_argument('--max-new-orders-per-run', type=int, default=1)
    return parser


def build_execution_config(runtime_config: dict, *, symbol: str, allow_live_send: bool) -> MT5ExecutionConfig:
    execution_cfg = runtime_config.get('execution', {})
    return MT5ExecutionConfig(
        symbol=symbol,
        lot_step=float(execution_cfg.get('lot_step', 0.01)),
        min_lot=float(execution_cfg.get('min_lot', 0.01)),
        max_lot=float(execution_cfg.get('max_lot', 100.0)),
        deviation=int(execution_cfg.get('deviation', 20)),
        magic=int(execution_cfg.get('magic', 35052026)),
        comment=str(execution_cfg.get('comment', 'session_basket_bot')),
        allow_live_send=allow_live_send,
        close_opposite_first=bool(execution_cfg.get('close_opposite_first', True)),
        sltp_tolerance_points=float(execution_cfg.get('sltp_tolerance_points', 0.05)),
    )


def decision_to_event(symbol: str, decision: ExecutionDecision, *, send_result: dict | None = None, close_results: list[dict] | None = None, sync_result: dict | None = None, management_result: dict | None = None) -> dict:
    payload = {
        'type': 'EXECUTION_DECISION',
        'symbol': symbol,
        'action': decision.action,
        'reason': decision.reason,
        'intent': decision.intent.to_dict() if decision.intent else None,
        'sync_plan': decision.sync_plan.to_dict() if decision.sync_plan else None,
        'management_plan': decision.management_plan.to_dict() if decision.management_plan else None,
        'broker_positions': [position.to_dict() for position in decision.broker_positions],
        'metadata': decision.metadata,
    }
    if send_result is not None:
        payload['send_result'] = send_result
    if close_results is not None:
        payload['close_results'] = close_results
    if sync_result is not None:
        payload['sync_result'] = sync_result
    if management_result is not None:
        payload['management_result'] = management_result
    return payload


def _suppress_repeated_management(decision: ExecutionDecision, execution_state: dict) -> ExecutionDecision:
    if decision.management_plan is None:
        return decision

    ticket_key = str(decision.management_plan.ticket)
    position_state = execution_state.get('positions', {}).get(ticket_key, {})
    partial_done = bool(position_state.get('partial_close_done', False))

    if partial_done:
        decision.management_plan.partial_close_volume = 0.0
        decision.management_plan.partial_close_reason = None
        if decision.management_plan.sync_plan is None:
            decision.action = 'HOLD'
            decision.reason = 'PARTIAL_ALREADY_DONE_NO_FURTHER_MANAGEMENT'
            decision.management_plan = None
            decision.sync_plan = None
    return decision


def _update_execution_state(execution_state: dict, decision: ExecutionDecision, *, allow_live_send: bool, management_result: dict | None, broker_positions: list) -> dict:
    execution_state = prune_execution_state(execution_state, [position.ticket for position in broker_positions])
    if not allow_live_send or decision.management_plan is None:
        return execution_state

    ticket_key = str(decision.management_plan.ticket)
    ticket_state = execution_state.setdefault('positions', {}).setdefault(ticket_key, {})
    partial_result = management_result.get('partial_result') if management_result else None
    sync_result = management_result.get('sync_result') if management_result else None
    if partial_result and partial_result.get('sent'):
        ticket_state['partial_close_done'] = True
        ticket_state['partial_close_reason'] = decision.management_plan.partial_close_reason
    if sync_result and sync_result.get('sent') and decision.management_plan.sync_plan is not None:
        ticket_state['last_synced_stop_loss'] = decision.management_plan.sync_plan.target_stop_loss
        ticket_state['last_synced_take_profit'] = decision.management_plan.sync_plan.target_take_profit
    return execution_state


def run_once(args: argparse.Namespace) -> dict:
    runtime_config = load_runtime_config(args.config)
    resolve_telegram(args, runtime_config)

    risk_cfg = runtime_config.get('risk', {})
    risk_config = RiskConfig(
        risk_per_trade=float(risk_cfg.get('risk_per_trade', 0.01)),
        max_drawdown_pct=float(risk_cfg.get('max_drawdown_pct', 12.0)),
        max_consecutive_losses=int(risk_cfg.get('max_consecutive_losses', 8)),
        min_balance=float(risk_cfg.get('min_balance', 1000.0)),
    )

    mt5_configs = build_mt5_configs(runtime_config)
    df_by_symbol = {symbol: fetch_ohlcv_from_mt5(cfg) for symbol, cfg in mt5_configs.items()}

    branch_specs = build_branch_specs(runtime_config, mt5_configs)
    candidates, branch_debugs = collect_candidates(df_by_symbol, branch_specs)
    accepted_signals, rejected_signals = resolve_conflicts(candidates)
    accepted_by_symbol = {str(signal.metadata.get('symbol')): signal for signal in accepted_signals}
    debug_summary = compact_debug_summary(branch_debugs, limit=4)

    state_dir = Path(args.execution_state_dir)
    state_dir.mkdir(parents=True, exist_ok=True)

    per_symbol_payload: dict[str, dict] = {}
    all_events: list[dict] = []
    open_positions_total = 0
    opened_orders_count = 0

    for symbol, cfg in mt5_configs.items():
        execution_config = build_execution_config(runtime_config, symbol=cfg.symbol, allow_live_send=bool(args.allow_live_send))
        adapter = MT5ExecutionAdapter(mt5_config=cfg, execution_config=execution_config)
        broker_positions = adapter.fetch_positions()
        open_positions_total += len(broker_positions)

        state_path = state_dir / f'{symbol.lower()}.json'
        execution_state = load_execution_state(state_path)

        signal = accepted_by_symbol.get(symbol)
        decision = adapter.decide(signal=signal, broker_positions=broker_positions, account_balance=args.account_balance, risk_config=risk_config)
        decision.metadata['branch_debugs'] = [d for d in branch_debugs if d.get('symbol') == symbol]
        decision.metadata['debug_summary'] = debug_summary
        decision = _suppress_repeated_management(decision, execution_state)

        if decision.action == 'OPEN':
            if len(broker_positions) >= max(args.max_live_positions_per_symbol, 0):
                decision.action = 'HOLD'
                decision.reason = 'GUARD_MAX_POSITIONS_PER_SYMBOL'
            elif open_positions_total >= max(args.max_live_positions_total, 0):
                decision.action = 'HOLD'
                decision.reason = 'GUARD_MAX_POSITIONS_TOTAL'
            elif opened_orders_count >= max(args.max_new_orders_per_run, 0):
                decision.action = 'HOLD'
                decision.reason = 'GUARD_MAX_NEW_ORDERS_PER_RUN'

        close_results = None
        send_result = None
        sync_result = None
        management_result = None
        if decision.action == 'REVERSE':
            close_results = adapter.close_positions(decision.metadata.get('close_tickets_first', []))
            if decision.intent is not None:
                send_result = adapter.send_market_order(decision.intent)
                if send_result.get('sent'):
                    opened_orders_count += 1
        elif decision.action == 'OPEN' and decision.intent is not None:
            send_result = adapter.send_market_order(decision.intent)
            if send_result.get('sent'):
                opened_orders_count += 1
                open_positions_total += 1
        elif decision.action == 'SYNC_SLTP' and decision.sync_plan is not None:
            sync_result = adapter.modify_position_sltp(decision.sync_plan)
        elif decision.action == 'MANAGE_POSITION' and decision.management_plan is not None:
            management_result = adapter.execute_management_plan(decision.management_plan)

        execution_state = _update_execution_state(
            execution_state,
            decision,
            allow_live_send=execution_config.allow_live_send,
            management_result=management_result,
            broker_positions=broker_positions,
        )
        save_execution_state(execution_state, state_path)

        event = decision_to_event(symbol, decision, send_result=send_result, close_results=close_results, sync_result=sync_result, management_result=management_result)
        all_events.append(event)

        per_symbol_payload[symbol] = {
            'execution_state_path': str(state_path),
            'latest_bar_time': df_by_symbol[symbol].index[-1].isoformat(),
            'broker_positions': [position.to_dict() for position in broker_positions],
            'decision': event,
        }

    telegram_sent = 0
    if args.send_telegram_alerts and args.telegram_bot_token and args.telegram_chat_id and all_events:
        filtered_events = [event for event in all_events if event.get('action') != 'HOLD']
        if filtered_events:
            telegram_sent = dispatch_telegram_alerts(
                TelegramAlertConfig(
                    bot_token=args.telegram_bot_token,
                    chat_id=args.telegram_chat_id,
                    insecure_ssl=args.telegram_insecure_ssl,
                ),
                filtered_events,
            )

    return {
        'mode': 'LIVE' if args.allow_live_send else 'DRY_RUN',
        'config_path': args.config,
        'execution_state_dir': str(state_dir),
        'risk': {
            'risk_per_trade_default': risk_config.risk_per_trade,
            'max_drawdown_pct': risk_config.max_drawdown_pct,
            'max_consecutive_losses': risk_config.max_consecutive_losses,
            'min_balance': risk_config.min_balance,
        },
        'guards': {
            'max_live_positions_total': args.max_live_positions_total,
            'max_live_positions_per_symbol': args.max_live_positions_per_symbol,
            'max_new_orders_per_run': args.max_new_orders_per_run,
        },
        'candidates': [
            {
                'branch_id': signal.metadata.get('branch_id'),
                'symbol': signal.metadata.get('symbol'),
                'priority': signal.metadata.get('branch_priority'),
                'risk_per_trade': signal.metadata.get('risk_per_trade'),
                'side': signal.side,
                'entry_time': signal.timestamp.isoformat(),
                'entry_price': signal.entry_price,
                'stop_loss': signal.stop_loss,
                'take_profit': signal.take_profit,
            }
            for signal in candidates
        ],
        'accepted_signals': [
            {
                'branch_id': signal.metadata.get('branch_id'),
                'symbol': signal.metadata.get('symbol'),
                'priority': signal.metadata.get('branch_priority'),
                'risk_per_trade': signal.metadata.get('risk_per_trade'),
                'side': signal.side,
                'entry_time': signal.timestamp.isoformat(),
                'entry_price': signal.entry_price,
                'stop_loss': signal.stop_loss,
                'take_profit': signal.take_profit,
            }
            for signal in accepted_signals
        ],
        'branch_debugs': branch_debugs,
        'debug_summary': debug_summary,
        'rejected_signals': rejected_signals,
        'per_symbol': per_symbol_payload,
        'telegram_alerts_sent': telegram_sent,
    }


def main() -> int:
    args = build_parser().parse_args()
    payload = run_once(args)
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        from xauusd_trading.execution.terminal_ui import format_execution_summary
        print(format_execution_summary(payload))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
