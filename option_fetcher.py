def build_request_config(
    symbol: str,
    expiration: str | None,
    provider_config: dict
) -> dict:
    """Build request config from a generic provider configuration."""
    base_url = provider_config.get("base_url")
    headers = provider_config.get("headers", {}).copy()
    params_map = provider_config.get("params_map", {})

    params = {}

    symbol_param = params_map.get("symbol")
    if symbol_param:
        params[symbol_param] = symbol.upper()

    expiration_param = params_map.get("expiration")
    if expiration_param and expiration is not None:
        params[expiration_param] = expiration

    static_params = provider_config.get("static_params", {})
    params.update(static_params)

    return {
        "base_url": base_url,
        "headers": headers,
        "params": params,
    }


def get_option_chain(
    symbol: str,
    expiration: str | None = None,
    provider_config: dict | None = None
) -> dict:
    """Build a generic option chain request from provider config."""
    if provider_config is None:
        raise ValueError("provider_config is required")

    provider_name = provider_config.get("name", "unknown")

    request_config = build_request_config(
        symbol=symbol,
        expiration=expiration,
        provider_config=provider_config,
    )

    return {
        "provider": provider_name,
        "symbol": symbol.upper(),
        "expiration": expiration,
        "request_config": request_config,
        "status": "not_implemented",
        "message": "Request config built successfully. Real API call not implemented yet.",
    }


if __name__ == "__main__":
    demo_provider_config = {
        "name": "custom_provider",
        "base_url": "https://api.example.com/options",
        "headers": {
            "Authorization": "Bearer YOUR_API_KEY"
        },
        "params_map": {
            "symbol": "symbol",
            "expiration": "expiration"
        },
        "static_params": {
            "greeks": "true"
        }
    }

    result = get_option_chain(
        symbol="AAPL",
        expiration="2026-04-17",
        provider_config=demo_provider_config
    )

    print(result)