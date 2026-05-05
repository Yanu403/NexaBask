from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_execution_state(path: str | Path) -> dict[str, Any]:
    state_path = Path(path)
    if not state_path.exists():
        return {'generated_at': _utc_now(), 'positions': {}}
    payload = json.loads(state_path.read_text())
    payload.setdefault('generated_at', _utc_now())
    payload.setdefault('positions', {})
    return payload


def save_execution_state(state: dict[str, Any], path: str | Path) -> Path:
    state_path = Path(path)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state['generated_at'] = _utc_now()
    state_path.write_text(json.dumps(state, indent=2))
    return state_path


def prune_execution_state(state: dict[str, Any], active_tickets: list[int]) -> dict[str, Any]:
    active_keys = {str(ticket) for ticket in active_tickets}
    state['positions'] = {
        ticket: payload
        for ticket, payload in state.get('positions', {}).items()
        if ticket in active_keys
    }
    return state
