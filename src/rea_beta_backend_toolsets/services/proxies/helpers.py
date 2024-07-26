from __future__ import annotations

import random
from concurrent.futures import ThreadPoolExecutor

import requests  # type: ignore

from .constants import MAX_THREAD_WORKER_VALIDATION
from .constants import PROXY_LIST_URL
from .types import Proxy
from .validation import is_valid
from .validation import is_valid_format


def valid_proxies(proxies: list[str], randomize=False) -> list[Proxy]:
    with ThreadPoolExecutor(
        max_workers=MAX_THREAD_WORKER_VALIDATION,
    ) as executor:
        results = list(executor.map(is_valid, proxies))

    valid_results = [result for result in results if result is not None]

    if randomize:
        random.shuffle(valid_results)
    else:
        valid_results.sort(
            key=lambda d: d.duration
            if d.duration is not None else float('-inf'),
        )

    return valid_results


def generate_unique_proxies() -> list[str]:
    response = requests.get(PROXY_LIST_URL)
    response.raise_for_status()
    proxies = [
        text.split(' ')[0]
        for text in response.text.splitlines()
    ]
    proxies = [
        text for text in proxies if is_valid_format(text)
    ]
    proxies = list(set(proxies))
    return proxies
