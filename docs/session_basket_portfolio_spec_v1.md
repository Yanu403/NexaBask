# Session Basket Portfolio Spec v1

## Status

Candidate portfolio spec for demo-market implementation.
This is the first basket version that has passed:
- branch research
- overlap review
- simple execution realism review
- branch priority review
- branch-level risk sizing review

## Goal

Run a multi-branch intraday session basket in demo market conditions with deterministic conflict handling and branch-aware risk sizing.

## Portfolio branches

### EURUSD
1. **Sweep reversal**
   - branch id: `eurusd_sweep`
   - strategy family: session sweep + MSS + FVG
   - role: highest-quality EURUSD branch

2. **Continuation after displacement**
   - branch id: `eurusd_continuation`
   - strategy family: continuation + FVG retrace
   - role: cleaner secondary EURUSD branch

3. **ORB breakout retest**
   - branch id: `eurusd_orb`
   - variant: `r2_b_cleaner_retest`
   - role: main EURUSD flow engine

### GBPUSD
4. **Adapted sweep**
   - branch id: `gbpusd_sweep`
   - role: moderate-confidence non-EURUSD contributor

5. **Continuation**
   - branch id: `gbpusd_continuation`
   - role: low-confidence exploratory branch, kept at reduced risk only

### XAUUSD
6. **Continuation**
   - branch id: `xauusd_continuation`
   - role: higher-quality diversification branch

## Approved branch priority

Priority is only used when conflicts occur on the same symbol.

1. `eurusd_sweep`
2. `eurusd_continuation`
3. `xauusd_continuation`
4. `gbpusd_sweep`
5. `eurusd_orb`
6. `gbpusd_continuation`

## Conflict rules

### Rule 1: one position per symbol
Only one live position per symbol may exist at a time.

### Rule 2: same-symbol conflicts use branch priority
If a new signal appears while another branch on the same symbol is already active:
- reject the lower-priority candidate
- keep the already-active higher-priority branch position

### Rule 3: cross-symbol overlap is allowed
EURUSD, GBPUSD, and XAUUSD may be open simultaneously.

### Rule 4: ORB is the flow engine, not the conflict winner
ORB is allowed to contribute most of the basket frequency, but if it directly conflicts with a cleaner same-symbol branch, the cleaner branch wins.

## Branch-level risk sizing

### Tier allocation
- `eurusd_sweep`: **1.00%** risk per trade
- `eurusd_continuation`: **0.75%** risk per trade
- `xauusd_continuation`: **0.75%** risk per trade
- `gbpusd_sweep`: **0.60%** risk per trade
- `eurusd_orb`: **0.50%** risk per trade
- `gbpusd_continuation`: **0.25%** risk per trade

## Portfolio guardrails

### Live exposure caps
- max **1 position per symbol**
- soft cap: max **1.5% live risk per symbol**
- soft cap: max **2.0% live ORB-origin risk** across the book

### Session hygiene
- no new entries outside each strategy's defined London / New York windows
- strategy-generated expiry and timeout rules remain active
- optional safety rule for demo runner: stop new entries for that symbol/session after **2 consecutive losses** in the same session window

### Account-level protection
Initial recommended demo defaults:
- max portfolio drawdown halt: **12%**
- max consecutive portfolio losses halt: **8**
- min balance guard remains active

## Execution model for demo runner

### Inputs
- MT5 market data for EURUSD, GBPUSD, XAUUSD
- execution timeframe by branch remains M3 for current basket research set
- per-symbol latest bars loaded independently

### Signal collection
At each loop iteration:
1. load latest data per symbol
2. run each approved branch on its assigned symbol dataset
3. collect zero or one candidate signal per branch
4. attach branch id, priority, and configured risk tier to each candidate

### Conflict resolution
Apply in this order:
1. discard candidates outside trade window
2. discard candidates blocked by open same-symbol position
3. among same-symbol simultaneous candidates, keep highest-priority branch only
4. allow cross-symbol signals to coexist

### Position sizing
For each accepted signal:
- compute risk amount from branch-specific risk tier
- size using stop distance
- enforce symbol live-risk cap before sending / opening

### Exit handling
Keep current branch-native exits:
- stop loss
- take profit
- timeout
- optional branch-native trailing / partial rules if present in signal metadata

## Current evidence level

### Strong enough to include now
- `eurusd_sweep`
- `eurusd_continuation`
- `eurusd_orb` r2_b
- `gbpusd_sweep`
- `xauusd_continuation`

### Include at reduced confidence only
- `gbpusd_continuation`

## What this spec does NOT claim yet

- it is not a final live-money portfolio
- it is not yet a broker-validated production runtime
- it has not yet been run as a full multi-symbol demo basket in MT5

## Immediate next implementation target

Build a demo basket runner that:
1. loads this branch list
2. enforces one-position-per-symbol
3. applies branch priority rules
4. applies branch-level risk tiers
5. records accepted vs rejected signals and reasons
6. emits journal + Telegram alerts for demo monitoring

## Success criteria for demo phase

The basket demo runner is considered ready when it can:
- run on MT5 demo without manual chart babysitting
- produce deterministic conflict decisions
- persist open positions and rejected-signal reasons
- show that real-time flow roughly resembles the research expectations
- survive multiple session days without state drift or signal spam
