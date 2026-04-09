def build_signal(
    source: str,
    symbol: str = None,
    timestamp: str = None,
    price: float = None,
    direction: str = None,
    signal_type: str = None,
    indicator: str = None,
    timeframe: str = None,
    raw_payload: dict = None,
) -> dict:
    """Build a standard internal signal object."""
    return {
        "source": source,
        "symbol": symbol,
        "timestamp": timestamp,
        "price": price,
        "direction": direction,
        "signal_type": signal_type,
        "indicator": indicator,
        "timeframe": timeframe,
        "raw_payload": raw_payload,
    }