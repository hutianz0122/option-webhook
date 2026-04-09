def normalize_direction(direction: str) -> str:
    """Normalize direction value to BULLISH or BEARISH."""
    direction = direction.strip().upper()

    if direction in ["BULLISH", "LONG", "BUY"]:
        return "BULLISH"
    if direction in ["BEARISH", "SHORT", "SELL"]:
        return "BEARISH"

    raise ValueError(f"Invalid direction: {direction}")


def parse_signal(data: dict) -> dict:
    """Parse raw webhook payload into the standard indicator signal schema."""
    source = data.get("source")
    event = data.get("event")
    underlying = data.get("underlying")
    raw_direction = data.get("direction")
    trigger_price = data.get("trigger_price")
    timestamp = data.get("timestamp")
    timeframe = data.get("timeframe")
    strategy = data.get("strategy")
    signal_type = data.get("signal_type")
    note = data.get("note")

    if not source:
        raise ValueError("Missing source")
    if not event:
        raise ValueError("Missing event")
    if not underlying:
        raise ValueError("Missing underlying")
    if not raw_direction:
        raise ValueError("Missing direction")
    if trigger_price is None:
        raise ValueError("Missing trigger_price")
    if not timestamp:
        raise ValueError("Missing timestamp")
    if not timeframe:
        raise ValueError("Missing timeframe")
    if not strategy:
        raise ValueError("Missing strategy")

    parsed_signal = {
        "source": str(source).lower(),
        "event": str(event).upper(),
        "underlying": str(underlying).upper(),
        "direction": normalize_direction(raw_direction),
        "trigger_price": float(trigger_price),
        "timestamp": str(timestamp),
        "timeframe": str(timeframe),
        "strategy": str(strategy),
    }

    if signal_type is not None:
        parsed_signal["signal_type"] = str(signal_type).upper()

    if note is not None:
        parsed_signal["note"] = str(note)

    return parsed_signal