from __future__ import annotations

import random
import re
import time
from concurrent.futures import ThreadPoolExecutor

import requests  # type: ignore

from .constants import PROXY_PROXY_CHECKER_URL
from .constants import PROXY_TIME_OUT_VALIDATION
from .types import Proxy

# Regular expression pattern for validating proxy format
proxy_pattern = re.compile(
    r'^'
    r'(?:(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.){3}'
    r'(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])'
    r':'
    r'(?:6553[0-5]|655[0-2][0-9]|65[0-4][0-9]{2}|6[0-4][0-9]{3}|'
    r'[1-5][0-9]{4}|[1-9][0-9]{0,3})'
    r'$',
)


def is_valid_request(proxy: str) -> Proxy | None:
    try:
        start_time = time.time()
        response = requests.get(
            PROXY_PROXY_CHECKER_URL,
            proxies={'http': proxy, 'https': proxy},
            timeout=PROXY_TIME_OUT_VALIDATION,
        )
        if response.status_code == 200:
            duration = time.time() - start_time
            data = response.json()
            data['duration'] = duration
            data['proxy'] = proxy
            return data
    except requests.RequestException:
        pass
    return None


def is_valid_format(proxy: str) -> bool:
    return bool(proxy.strip()) and proxy_pattern.match(proxy) is not None


def is_valid(proxy: str) -> Proxy | None:
    return is_valid_request(proxy) if is_valid_format(proxy) else None


def valid_proxies(proxies: list[str], randomize=False) -> list[Proxy]:
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(is_valid, proxies))

    valid_results = [result for result in results if result is not None]

    if randomize:
        random.shuffle(valid_results)
    else:
        valid_results.sort(key=lambda d: d.duration)

    return valid_results
