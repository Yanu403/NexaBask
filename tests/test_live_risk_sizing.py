from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace

import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from run_session_basket_demo_mt5 import build_branch_specs
from xauusd_trading.data import mt5 as mt5_data
from xauusd_trading.data.mt5 import MT5Config
from xauusd_trading.execution.mt5_execution import MT5ExecutionAdapter, MT5ExecutionConfig
from xauusd_trading.models.trading import TradeSignal
from xauusd_trading.risk.manager import RiskConfig
from xauusd_trading.strategies.session_orb_retest import SessionORBRetestStrategy


def _gbpusd_long_signal(metadata: dict) -> TradeSignal:
    return TradeSignal(
        index=1,
        timestamp=pd.Timestamp("2026-05-11T06:30:00Z"),
        side="LONG",
        entry_price=1.35902,
        stop_loss=1.35825,
        take_profit=1.36056,
        metadata=metadata,
    )


def test_gbpusd_orb_strategy_uses_forex_lot_size_metadata() -> None:
    strategy = SessionORBRetestStrategy(pip_size=0.0001, lot_size=100_000.0)
    signal = strategy._build_signal(  # noqa: SLF001 - regression test for strategy metadata
        pd.DataFrame(
            {
                "low": [1.35825],
                "high": [1.35910],
            },
            index=[pd.Timestamp("2026-05-11T06:30:00Z")],
        ),
        index=0,
        breakout_index=0,
        side="LONG",
        entry_price=1.35902,
        level=1.35900,
    )

    assert signal is not None
    assert signal.metadata["lot_size"] == 100_000.0


def test_live_build_intent_defaults_forex_to_100k_lot_size() -> None:
    adapter = MT5ExecutionAdapter(
        mt5_config=MT5Config(symbol="GBPUSD"),
        execution_config=MT5ExecutionConfig(symbol="GBPUSD"),
    )
    signal = _gbpusd_long_signal(
        {
            "symbol": "GBPUSD",
            "strategy": "gbpusd_orb",
            "risk_per_trade": 0.003,
            "pip_size": 0.0001,
            # Deliberately omit lot_size to verify safe forex fallback.
        }
    )

    intent = adapter.build_intent(
        signal,
        account_balance=10_000.0,
        risk_config=RiskConfig(risk_per_trade=0.01),
    )

    assert intent is not None
    assert intent.metadata["lot_size"] == 100_000.0
    assert 0.37 <= intent.volume <= 0.40
    assert intent.metadata["estimated_risk_currency"] <= intent.metadata["risk_budget"] * 1.05


def test_live_mode_uses_mt5_equity_and_order_calc_profit_not_cli_balance(monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeMT5:
        ORDER_TYPE_BUY = 0
        ORDER_TYPE_SELL = 1

        def initialize(self, **kwargs) -> bool:  # noqa: ARG002
            return True

        def login(self, *args, **kwargs) -> bool:  # noqa: ARG002
            return True

        def shutdown(self) -> None:
            return None

        def last_error(self):
            return (0, "ok")

        def account_info(self):
            return SimpleNamespace(equity=1_000.0, balance=1_200.0)

        def symbol_info(self, symbol):  # noqa: ARG002
            return SimpleNamespace(visible=True, trade_contract_size=100_000.0)

        def symbol_select(self, symbol, visible):  # noqa: ARG002
            return True

        def order_calc_profit(self, order_type, symbol, volume, entry, stop):  # noqa: ARG002
            assert volume == 1.0
            # GBPUSD 7.7 pip risk at 1 lot is about $77.
            return -77.0

    monkeypatch.setattr(mt5_data, "_import_mt5", lambda: FakeMT5())
    adapter = MT5ExecutionAdapter(
        mt5_config=MT5Config(symbol="GBPUSD"),
        execution_config=MT5ExecutionConfig(symbol="GBPUSD", allow_live_send=True),
    )
    signal = _gbpusd_long_signal({"symbol": "GBPUSD", "risk_per_trade": 0.003, "pip_size": 0.0001})

    intent = adapter.build_intent(signal, account_balance=10_000.0, risk_config=RiskConfig(risk_per_trade=0.01))

    assert intent is not None
    assert intent.metadata["risk_budget_source"] == "mt5_equity"
    assert intent.metadata["sizing_balance"] == 1_000.0
    assert intent.metadata["risk_budget"] == 3.0
    assert intent.metadata["risk_per_lot"] == 77.0
    assert intent.volume == 0.03


def test_risk_override_is_clamped_to_five_percent() -> None:
    adapter = MT5ExecutionAdapter(
        mt5_config=MT5Config(symbol="GBPUSD"),
        execution_config=MT5ExecutionConfig(symbol="GBPUSD"),
    )
    signal = _gbpusd_long_signal({"symbol": "GBPUSD", "risk_per_trade": 0.99, "pip_size": 0.0001, "lot_size": 100_000.0})

    intent = adapter.build_intent(signal, account_balance=10_000.0, risk_config=RiskConfig(risk_per_trade=0.01))

    assert intent is not None
    assert intent.metadata["effective_risk_per_trade"] == 0.05
    assert intent.metadata["risk_budget"] == 500.0


def test_buggy_ten_lot_gbpusd_trade_would_exceed_risk_budget() -> None:
    entry = 1.35902
    stop = 1.35825
    estimated_risk = 10.0 * 100_000.0 * abs(entry - stop)

    assert estimated_risk > 700.0
    assert estimated_risk > 30.0 * 20.0


def test_build_intent_does_not_round_sub_min_volume_up_to_min_lot() -> None:
    adapter = MT5ExecutionAdapter(
        mt5_config=MT5Config(symbol="GBPUSD"),
        execution_config=MT5ExecutionConfig(symbol="GBPUSD", min_lot=0.01, lot_step=0.01),
    )
    signal = _gbpusd_long_signal({"symbol": "GBPUSD", "risk_per_trade": 0.000001, "pip_size": 0.0001, "lot_size": 100_000.0})

    intent = adapter.build_intent(
        signal,
        account_balance=1_000.0,
        risk_config=RiskConfig(risk_per_trade=0.000001),
    )

    assert intent is None
    assert adapter._last_build_intent_reject_reason is not None
    assert "BELOW_MIN_LOT" in adapter._last_build_intent_reject_reason


def test_unknown_active_branch_fails_fast_instead_of_silent_ignore() -> None:
    mt5_configs = {
        "EURUSD": MT5Config(symbol="EURUSD"),
        "GBPUSD": MT5Config(symbol="GBPUSD"),
        "XAUUSD": MT5Config(symbol="XAUUSD"),
    }

    with pytest.raises(ValueError, match="Unsupported active_branches"):
        build_branch_specs({"active_branches": ["eurusd_sweep", "gbpusd_orb"]}, mt5_configs)
