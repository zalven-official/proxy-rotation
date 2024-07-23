from __future__ import annotations

import re

import requests  # type: ignore
from rea_beta_backend_toolsets.services.proxies import constants


def is_valid_request(proxy: str) -> bool:
    try:
        res = requests.get(
            constants.PROXY_PROXY_CHECKER_URL,
            proxies={'http': proxy, 'https': proxy},
            timeout=constants.PROXY_TIME_OUT_VALIDATION,
        )
        if res.status_code == 200:
            return True
    except requests.RequestException:
        return False
    return False


def is_valid_format(proxy: str) -> bool:
    if not isinstance(proxy, str) or not proxy.strip():
        return False
    proxy_pattern = re.compile(
        r'^'
        r'(?:(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.){3}'
        r'(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])'
        r':'
        r'(?:6553[0-5]|655[0-2][0-9]|65[0-4][0-9]{2}|6[0-4][0-9]{3}|'
        r'[1-5][0-9]{4}|[1-9][0-9]{0,3})'
        r'$',
    )
    return proxy_pattern.match(proxy) is not None


def is_valid(proxy: str) -> bool:
    return is_valid_format(proxy) and is_valid_request(proxy)
