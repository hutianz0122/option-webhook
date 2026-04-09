"""
Provider configuration registry.
"""

import os

PROVIDERS = {
    "httpbin_test": {
        "name": "httpbin_test",
        "base_url": "https://httpbin.org",
        "endpoint": "/get",
        "method": "GET",
        "timeout": 10,
        "auth_type": "query",
        "api_key": os.getenv("OPTION_DATA_API_KEY", ""),
        "api_key_param": "apikey",
        "symbol_param": "symbol",
        "expiration_param": "expiration",
        "headers": {},
        "default_params": {
            "greeks": "true"
        }
    },

    "real_provider_template": {
        "name": "real_provider_template",
        "base_url": "",
        "endpoint": "",
        "expirations_endpoint": "",
        "method": "GET",
        "timeout": 10,
        "auth_type": "query",
        "api_key": os.getenv("OPTION_DATA_API_KEY", ""),
        "api_key_param": "apikey",
        "symbol_param": "symbol",
        "expiration_param": "expiration",
        "headers": {},
        "default_params": {}
    },

    "tradier": {
        "name": "tradier",
        "base_url": "https://api.tradier.com",
        "endpoint": "/v1/markets/options/chains",
        "expirations_endpoint": "/v1/markets/options/expirations",
        "method": "GET",
        "timeout": 10,
        "auth_type": "header",
        "api_key": os.getenv("TRADIER_API_KEY", ""),
        "api_key_header": "Authorization",
        "api_key_prefix": "Bearer ",
        "symbol_param": "symbol",
        "expiration_param": "expiration",
        "headers": {
            "Accept": "application/json"
        },
        "default_params": {}
    },

    "longport_template": {
        "name": "longport_template",
        "base_url": "",
        "endpoint": "",
        "expirations_endpoint": "",
        "method": "GET",
        "timeout": 10,
        "auth_type": "header",
        "api_key": os.getenv("LONGPORT_API_KEY", ""),
        "api_key_header": "Authorization",
        "api_key_prefix": "Bearer ",
        "symbol_param": "symbol",
        "expiration_param": "expiration",
        "headers": {},
        "default_params": {}
    }
}