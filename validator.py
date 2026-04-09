def validate_signal(signal: dict) -> tuple[bool, list]:
    """Validate a normalized signal object."""
    errors = []

    if not signal.get("source"):
        errors.append("Missing source")

    if not signal.get("symbol"):
        errors.append("Missing symbol")

    if not signal.get("timestamp"):
        errors.append("Missing timestamp")

    price = signal.get("price")
    if price is None:
        errors.append("Missing price")
    else:
        try:
            if float(price) <= 0:
                errors.append("Price must be greater than 0")
        except (TypeError, ValueError):
            errors.append("Price must be a number")

    direction = signal.get("direction")
    if direction is not None and direction not in ["BULLISH", "BEARISH"]:
        errors.append("Direction must be BULLISH or BEARISH")

    return len(errors) == 0, errors