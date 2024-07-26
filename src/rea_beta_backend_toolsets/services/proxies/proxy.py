from __future__ import annotations

import threading

from .helpers import generate_unique_proxies
from .helpers import valid_proxies
from .types import Proxy
from .validation import is_valid


class ProxyRotationManager:
    def __init__(self, proxies: list[str] | None = None):
        self.lock = threading.Lock()
        self.index = 0
        self.proxies = self._proxy_copy(proxies)
        self.valid_proxies: list[Proxy] = []
        self.validate_proxies()

    def _proxy_copy(
        self,
        proxies: list[str] | None = None,
    ) -> list[str]:
        if proxies and len(proxies) > 0:
            return proxies.copy()
        return generate_unique_proxies()

    def get_next_proxy(self) -> Proxy:

        with self.lock:
            if not self.valid_proxies:
                raise ValueError('No proxies available')

            proxy = self.valid_proxies[self.index]
            self.index = (self.index + 1) % len(self.valid_proxies)
            return proxy

    def add_proxy(self, proxy: str):
        with self.lock:
            proxy_data = is_valid(proxy)
            if proxy_data is None:
                return

            duration = proxy_data['duration']
            insert_index = len(self.valid_proxies)

            for i, existing_proxy in enumerate(self.valid_proxies):
                if existing_proxy['duration'] > duration:
                    insert_index = i
                    break
            self.valid_proxies.insert(insert_index, proxy_data)

    def remove_proxy(self, proxy: str):
        with self.lock:
            self.valid_proxies = [
                p for p in self.valid_proxies if p.proxy != proxy
            ]
            self.index = 0

    def get_all_proxies(self) -> list[Proxy]:
        with self.lock:
            return self.valid_proxies.copy()

    def validate_proxies(self):
        with self.lock:
            proxies = list(set(self.proxies))
            self.valid_proxies = valid_proxies(proxies)

    def status(self):
        proxies = len(self.valid_proxies)
        print(f'Available proxies: {proxies}')
