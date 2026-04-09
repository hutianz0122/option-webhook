"""
Generic option chain fetcher.

This module provides a provider-agnostic structure for:
1. validating provider configs
2. building request configs
3. fetching raw provider data
4. fetching option expirations
5. fetching option chains
6. running a full pipeline: symbol -> expirations -> option chain
"""

from typing import Any, Dict, Optional
import requests

from providers import PROVIDERS


def validate_provider_config(provider_config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Validate provider configuration before sending request.

    Args:
        provider_config: Provider-specific configuration dictionary

    Returns:
        None if valid, otherwise an error dictionary
    """
    required_fields = ["name", "base_url", "method", "timeout"]
    for field in required_fields:
        if not provider_config.get(field):
            return {
                "status": "error",
                "error_type": "config_error",
                "message": f"Missing required provider config field: {field}"
            }

    auth_type = provider_config.get("auth_type")
    api_key = provider_config.get("api_key", "")

    if auth_type in ["query", "header"] and not api_key:
        return {
            "status": "error",
            "error_type": "config_error",
            "message": f"Missing API key for provider: {provider_config.get('name', 'unknown')}"
        }

    return None


def build_request_config(
    symbol: str,
    expiration: str,
    provider_config: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Build request configuration for option chain endpoint.

    Args:
        symbol: Underlying symbol, e.g. "AAPL"
        expiration: Option expiration date, e.g. "2026-04-17"
        provider_config: Provider-specific configuration dictionary

    Returns:
        A dictionary containing method, url, headers, params, timeout
    """
    base_url = provider_config.get("base_url", "")
    endpoint = provider_config.get("endpoint", "")
    method = provider_config.get("method", "GET").upper()
    timeout = provider_config.get("timeout", 10)

    auth_type = provider_config.get("auth_type")
    api_key = provider_config.get("api_key")

    headers = provider_config.get("headers", {}).copy()
    params = provider_config.get("default_params", {}).copy()

    symbol_param = provider_config.get("symbol_param", "symbol")
    expiration_param = provider_config.get("expiration_param", "expiration")

    params[symbol_param] = symbol
    params[expiration_param] = expiration

    if auth_type == "query" and api_key:
        key_name = provider_config.get("api_key_param", "apikey")
        params[key_name] = api_key

    elif auth_type == "header" and api_key:
        header_name = provider_config.get("api_key_header", "Authorization")
        header_prefix = provider_config.get("api_key_prefix", "")
        headers[header_name] = f"{header_prefix}{api_key}"

    url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"

    return {
        "method": method,
        "url": url,
        "headers": headers,
        "params": params,
        "timeout": timeout
    }


def build_expirations_request_config(
    symbol: str,
    provider_config: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Build request configuration for option expirations endpoint.

    Args:
        symbol: Underlying symbol
        provider_config: Provider-specific configuration dictionary

    Returns:
        A dictionary containing method, url, headers, params, timeout
    """
    base_url = provider_config.get("base_url", "")
    endpoint = provider_config.get("expirations_endpoint", "")
    method = provider_config.get("method", "GET").upper()
    timeout = provider_config.get("timeout", 10)

    auth_type = provider_config.get("auth_type")
    api_key = provider_config.get("api_key")

    headers = provider_config.get("headers", {}).copy()
    params = provider_config.get("default_params", {}).copy()

    symbol_param = provider_config.get("symbol_param", "symbol")
    params[symbol_param] = symbol

    if auth_type == "query" and api_key:
        key_name = provider_config.get("api_key_param", "apikey")
        params[key_name] = api_key

    elif auth_type == "header" and api_key:
        header_name = provider_config.get("api_key_header", "Authorization")
        header_prefix = provider_config.get("api_key_prefix", "")
        headers[header_name] = f"{header_prefix}{api_key}"

    url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"

    return {
        "method": method,
        "url": url,
        "headers": headers,
        "params": params,
        "timeout": timeout
    }


def fetch_raw_data(request_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Send HTTP request and return raw response.

    Args:
        request_config: Output from request config builder

    Returns:
        A dictionary containing raw response or error info
    """
    method = request_config["method"]
    url = request_config["url"]
    headers = request_config.get("headers", {})
    params = request_config.get("params", {})
    timeout = request_config.get("timeout", 10)

    try:
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            timeout=timeout
        )

        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "")
        if "application/json" in content_type:
            data = response.json()
        else:
            data = response.text

        return {
            "status": "success",
            "http_status": response.status_code,
            "raw_data": data
        }

    except requests.exceptions.Timeout:
        return {
            "status": "error",
            "error_type": "timeout",
            "message": "Request timed out"
        }

    except requests.exceptions.HTTPError as e:
        return {
            "status": "error",
            "error_type": "http_error",
            "message": str(e),
            "http_status": getattr(e.response, "status_code", None),
            "response_text": getattr(e.response, "text", None)
        }

    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error_type": "request_error",
            "message": str(e)
        }


def normalize_option_chain(
    raw_result: Dict[str, Any],
    provider_config: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Normalize provider response into project-level standard structure.

    Args:
        raw_result: Output from fetch_raw_data()
        provider_config: Provider-specific configuration dictionary

    Returns:
        A normalized dictionary
    """
    if raw_result["status"] != "success":
        return raw_result

    raw_data = raw_result["raw_data"]

    return {
        "status": "success",
        "provider": provider_config.get("name", "unknown"),
        "normalized": False,
        "option_chain": raw_data,
        "meta": {
            "note": "Raw provider response returned. Deep normalization not implemented yet."
        }
    }


def get_option_chain(
    symbol: str,
    expiration: str,
    provider_config: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Main entry point for fetching option chain data.

    Args:
        symbol: Underlying symbol
        expiration: Option expiration date
        provider_config: Provider-specific configuration

    Returns:
        Standardized fetch result
    """
    config_error = validate_provider_config(provider_config)
    if config_error:
        return config_error

    endpoint = provider_config.get("endpoint")
    if not endpoint:
        return {
            "status": "error",
            "error_type": "config_error",
            "message": f"Missing endpoint for provider: {provider_config.get('name', 'unknown')}"
        }

    request_config = build_request_config(
        symbol=symbol,
        expiration=expiration,
        provider_config=provider_config
    )

    raw_result = fetch_raw_data(request_config)
    normalized_result = normalize_option_chain(raw_result, provider_config)

    return normalized_result


def get_option_expirations(
    symbol: str,
    provider_config: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Fetch option expiration dates for a symbol.

    Args:
        symbol: Underlying symbol
        provider_config: Provider-specific configuration

    Returns:
        Standardized fetch result
    """
    config_error = validate_provider_config(provider_config)
    if config_error:
        return config_error

    expirations_endpoint = provider_config.get("expirations_endpoint")
    if not expirations_endpoint:
        return {
            "status": "error",
            "error_type": "config_error",
            "message": f"Missing expirations_endpoint for provider: {provider_config.get('name', 'unknown')}"
        }

    request_config = build_expirations_request_config(
        symbol=symbol,
        provider_config=provider_config
    )

    raw_result = fetch_raw_data(request_config)

    if raw_result["status"] != "success":
        return raw_result

    return {
        "status": "success",
        "provider": provider_config.get("name", "unknown"),
        "normalized": False,
        "expirations": raw_result["raw_data"],
        "meta": {
            "note": "Raw provider response returned. Expiration parsing not implemented yet."
        }
    }


def parse_tradier_expirations(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse Tradier expiration response.

    Args:
        raw_data: Raw API response

    Returns:
        Parsed expiration list
    """
    try:
        expirations = raw_data["expirations"]["date"]

        if isinstance(expirations, str):
            expirations = [expirations]

        return {
            "status": "success",
            "expirations": expirations
        }

    except Exception:
        return {
            "status": "error",
            "error_type": "parse_error",
            "message": "Failed to parse expiration response"
        }


def get_first_expiration(symbol: str, provider_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Fetch expirations and return the first available date.
    """
    result = get_option_expirations(symbol, provider_config)

    if result["status"] != "success":
        return result

    provider_name = provider_config.get("name", "")

    if provider_name == "tradier":
        parsed = parse_tradier_expirations(result["expirations"])
    else:
        return {
            "status": "error",
            "error_type": "parse_error",
            "message": f"No expiration parser implemented for provider: {provider_name}"
        }

    if parsed["status"] != "success":
        return parsed

    expirations = parsed["expirations"]

    if not expirations:
        return {
            "status": "error",
            "error_type": "no_expirations",
            "message": "No expirations found"
        }

    return {
        "status": "success",
        "expiration": expirations[0]
    }


def fetch_option_chain_auto(symbol: str, provider_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Full pipeline:
    symbol -> expirations -> option chain
    """
    expiration_result = get_first_expiration(symbol, provider_config)

    if expiration_result["status"] != "success":
        return expiration_result

    expiration = expiration_result["expiration"]

    return get_option_chain(symbol, expiration, provider_config)


if __name__ == "__main__":
    result = fetch_option_chain_auto(
        symbol="AAPL",
        provider_config=PROVIDERS["tradier"]
    )

    print(result)