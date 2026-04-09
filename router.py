def route_signal(signal: dict) -> dict:
    """Determine where the signal should be routed."""
    
    source = signal.get("source")

    if source == "tradingview":
        destination = "manual_review"
    else:
        destination = "unknown_queue"

    routed_signal = {
        "destination": destination,
        "signal": signal
    }

    return routed_signal