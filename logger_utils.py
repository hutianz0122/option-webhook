import json
from datetime import datetime
from pathlib import Path


RAW_LOG_FILE = Path("/home/ubuntu/projects/logs/raw_signals.log")
NORMALIZED_LOG_FILE = Path("/home/ubuntu/projects/logs/normalized_signals.log")
REJECTED_LOG_FILE = Path("/home/ubuntu/projects/logs/rejected_signals.log")
ROUTED_LOG_FILE = Path("/home/ubuntu/projects/logs/routed_signals.log")

def append_raw_signal_log(payload: dict, status: str = "received") -> None:
    """Append one raw webhook payload record to the raw signal log file."""
    record = {
        "received_at": datetime.now().isoformat(),
        "raw_payload": payload,
        "status": status,
    }

    RAW_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    with RAW_LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def append_normalized_signal_log(signal: dict, status: str = "normalized") -> None:
    """Append one normalized signal record to the normalized signal log file."""
    record = {
        "processed_at": datetime.now().isoformat(),
        "normalized_signal": signal,
        "status": status,
    }

    NORMALIZED_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    with NORMALIZED_LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def append_rejected_signal_log(payload: dict, errors: list, status: str = "rejected") -> None:
    """Append one rejected signal record to the rejected signal log file."""
    record = {
        "processed_at": datetime.now().isoformat(),
        "raw_payload": payload,
        "errors": errors,
        "status": status,
    }

    REJECTED_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    with REJECTED_LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def append_routed_signal_log(routed_signal: dict, status: str = "routed") -> None:
    """Append one routed signal record to the routed signal log file."""
    record = {
        "routed_at": datetime.now().isoformat(),
        "routed_signal": routed_signal,
        "status": status,
    }

    ROUTED_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    with ROUTED_LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")