# Session Basket Demo Runtime

This runtime is the first implementation bridge from the session basket research portfolio spec to a real MT5 demo loop.

## Scope

Runner:
- `run_session_basket_demo_mt5.py` (one-shot)
- `run_session_basket_demo_mt5_loop.py` (periodic loop)

Config sample:
- `runtime/session_basket_demo_config.windows.sample.json`

Windows launcher:
- `windows_run_session_basket_demo_loop.bat`

## What this runner enforces

- basket branch set from `session_basket_portfolio_spec_v1.md`
- one position per symbol
- branch priority for same-symbol conflicts
- branch-level risk overrides via signal metadata
- cross-symbol overlap allowed

## Branch priority in runtime

1. `eurusd_sweep`
2. `eurusd_continuation`
3. `xauusd_continuation`
4. `gbpusd_sweep`
5. `eurusd_orb`
6. `gbpusd_continuation`

## Risk tiers in runtime

- `eurusd_sweep`: 1.00%
- `eurusd_continuation`: 0.75%
- `xauusd_continuation`: 0.75%
- `gbpusd_sweep`: 0.60%
- `eurusd_orb`: 0.50%
- `gbpusd_continuation`: 0.25%

## Setup on Windows RDP

1. Copy sample config:

```text
runtime\session_basket_demo_config.windows.sample.json
```

to:

```text
runtime\session_basket_demo_config.json
```

2. Fill MT5 and Telegram credentials.
3. Set broker symbols correctly (e.g. `EURUSDm`, `GBPUSDm`, `XAUUSDm`).
4. Run:

```bat
windows_run_session_basket_demo_loop.bat
```

## Outputs

- per-symbol state JSON:
  - `runtime/session_basket_states/eurusd.json`
  - `runtime/session_basket_states/gbpusd.json`
  - `runtime/session_basket_states/xauusd.json`
- per-symbol journals:
  - `runtime/session_basket_journals/*.jsonl`
- loop heartbeat:
  - `runtime/session_basket_demo_loop.jsonl`

## Notes

- This is a demo-paper runtime, not broker order execution yet.
- It is designed to validate multi-branch signal flow and conflict logic under live MT5 data.
- After this runner is stable on demo, the next phase is broker execution bridge for the basket.
