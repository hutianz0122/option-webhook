from signal_model import build_signal


def normalize_tradingview_signal(payload: dict) -> dict:
    """Normalize TradingView-like payload into internal signal structure."""
    return build_signal(
        source="tradingview",
        symbol=payload.get("symbol") or payload.get("ticker"),
        timestamp=payload.get("timestamp") or payload.get("time"),
        price=payload.get("price") or payload.get("close") or payload.get("trigger_price"),
        direction=payload.get("direction"),
        signal_type=payload.get("signal_type"),
        indicator=payload.get("indicator"),
        timeframe=payload.get("timeframe") or payload.get("interval"),
        raw_payload=payload,
    )


def normalize_unknown_signal(payload: dict) -> dict:
    """Normalize unknown payload into a fallback internal signal structure."""
    return build_signal(
        source=payload.get("source", "unknown"),
        symbol=payload.get("symbol") or payload.get("ticker"),
        timestamp=payload.get("timestamp") or payload.get("time"),
        price=payload.get("price") or payload.get("close") or payload.get("trigger_price"),
        direction=payload.get("direction"),
        signal_type=payload.get("signal_type"),
        indicator=payload.get("indicator"),
        timeframe=payload.get("timeframe") or payload.get("interval"),
        raw_payload=payload,
    )


def normalize_raw_signal(payload: dict) -> dict:
    """Route payload to the appropriate normalizer."""
    source = str(payload.get("source", "")).lower()

    if source == "tradingview":
        return normalize_tradingview_signal(payload)

    return normalize_unknown_signal(payload)