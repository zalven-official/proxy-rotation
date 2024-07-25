from __future__ import annotations

import random
from concurrent.futures import ThreadPoolExecutor

from .types import Proxy
from .validation import is_valid


def valid_proxies(proxies: list[str], randomize=False) -> list[Proxy]:
    with ThreadPoolExecutor(max_workers=10) as executor:
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
