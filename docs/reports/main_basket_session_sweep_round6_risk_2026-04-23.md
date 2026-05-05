# Main Basket Session Sweep Round 6 Risk Sizing Review, 2026-04-23

## Goal

Define a simple branch-level risk sizing scheme for the current basket that reflects:
- branch quality differences
- sample-size confidence differences
- ORB's role as the main flow engine without letting it dominate risk the same way it dominates count

## Starting point

Current core execution assumptions already support fixed risk-per-trade sizing.
So the practical next step is not a complex optimizer, but a clean tiered risk model.

## Branch quality context

### Cleaner / higher-confidence branches
- EURUSD sweep: PF 4.98, DD ~1.00%
- EURUSD continuation: PF 3.94, DD ~1.00%, but tiny sample
- XAUUSD continuation: PF 3.88, DD ~1.00%, but tiny sample

### Medium-confidence branch
- GBPUSD adapted sweep: PF 1.37, DD ~1.00%

### Flow engine / lower-quality branch
- EURUSD ORB r2_b: PF 1.31, DD ~9.03%, high flow

### Low-confidence branch
- GBPUSD continuation: only 1 trade so far

## Proposed risk sizing tiers

### Tier A: 1.00% risk per trade
Use for the cleanest highest-PF branch.
- EURUSD sweep: **1.00%**

### Tier B: 0.75% risk per trade
Use for good continuation branches with strong early profile but smaller samples.
- EURUSD continuation: **0.75%**
- XAUUSD continuation: **0.75%**

### Tier C: 0.60% risk per trade
Use for acceptable but clearly weaker branch quality.
- GBPUSD adapted sweep: **0.60%**

### Tier D: 0.50% risk per trade
Use for the main frequency engine with lower PF and materially higher DD.
- EURUSD ORB r2_b: **0.50%**

### Tier E: 0.25% risk per trade
Use for tiny-sample exploratory branch.
- GBPUSD continuation: **0.25%**

## Why ORB should be smaller

ORB is central for productivity, but it is not the cleanest branch.
If it receives the same per-trade risk as EURUSD sweep, portfolio behavior becomes too dependent on the noisiest branch.

That means:
- keep ORB in the basket
- let ORB provide flow
- cap ORB per-trade risk below the cleaner branches

## Simple portfolio-level guardrails

Recommended initial guardrails:
- one position per symbol
- branch priority as defined in the priority review
- allow cross-symbol overlap
- optional soft cap: no more than **1.5% total live risk per symbol**
- optional soft cap: no more than **2.0% total live ORB-origin risk** across the book
- optional daily/session guard: stop new entries after **2 consecutive losses in the same symbol/session window**

## Nominal weekly risk view under proposed sizing

Using accepted trades under the current one-position-per-symbol + priority model:
- accepted trades: 60
- average nominal weekly risk flow: **2.63%**
- max nominal weekly risk flow: **3.85%**
- min nominal weekly risk flow: **1.50%**

### Weekly nominal risk examples
- 2026-W06: 3.70%
- 2026-W07: 3.85%
- 2026-W12: 3.00%
- 2026-W13: 3.00%

This looks manageable and much more balanced than flat 1% sizing across all branches.

## Current recommendation

Use this as the first practical sizing model:
- EURUSD sweep: 1.00%
- EURUSD continuation: 0.75%
- XAUUSD continuation: 0.75%
- GBPUSD adapted sweep: 0.60%
- EURUSD ORB r2_b: 0.50%
- GBPUSD continuation: 0.25%

## Bottom line

The basket is now strong enough that sizing matters more than finding more branches.
A tiered model is the right next step because it:
- protects the portfolio from ORB over-dominance
- still keeps the frequency advantage
- respects the current evidence quality of each branch

## Review file

- `data/main_basket_session_sweep_round6_risk/summary.json`
