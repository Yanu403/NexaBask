from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_execution_state(path: str | Path) -> dict[str, Any]:
    state_path = Path(path)
    if not state_path.exists():
        return {'generated_at': _utc_now(), 'positions': {}}
    try:
        payload = json.loads(state_path.read_text())
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning('Corrupted state file %s (%s); resetting to empty state', state_path, exc)
        return {'generated_at': _utc_now(), 'positions': {}}
    if not isinstance(payload, dict):
        logger.warning('State file %s does not contain a dict; resetting to empty state', state_path)
        return {'generated_at': _utc_now(), 'positions': {}}
    payload.setdefault('generated_at', _utc_now())
    payload.setdefault('positions', {})
    return payload


def save_execution_state(state: dict[str, Any], path: str | Path) -> Path:
    state_path = Path(path)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state['generated_at'] = _utc_now()
    tmp_path = state_path.with_suffix('.tmp')
    tmp_path.write_text(json.dumps(state, indent=2))
    os.replace(str(tmp_path), str(state_path))
    return state_path


def prune_execution_state(state: dict[str, Any], active_tickets: list[int]) -> dict[str, Any]:
    active_keys = {str(ticket) for ticket in active_tickets}
    state['positions'] = {
        ticket: payload
        for ticket, payload in state.get('positions', {}).items()
        if ticket in active_keys
    }
    return state
