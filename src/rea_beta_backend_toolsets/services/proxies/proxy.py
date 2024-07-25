from __future__ import annotations

import threading

from .helpers import is_valid
from .helpers import valid_proxies
from .types import Proxy


class ProxyRotationManager:
    def __init__(self, proxies: list[str]):
        """
        Initialize the ProxyRotationManager with a list of proxies.

        Args:
            proxies (List[str]): Initial list of proxy strings.
        """
        self.lock = threading.Lock()
        self.index = 0
        self.proxies = proxies.copy()
        self.valid_proxies: list[Proxy] = []
        self.validate_proxies()

    def get_next_proxy(self) -> Proxy:
        """
        Get the next valid proxy in the rotation.

        Returns:
            Proxy: The next valid proxy.

        Raises:
            ValueError: If no valid proxies are available.
        """
        with self.lock:
            if not self.valid_proxies:
                raise ValueError('No proxies available')

            proxy = self.valid_proxies[self.index]
            self.index = (self.index + 1) % len(self.valid_proxies)
            return proxy

    def add_proxy(self, proxy: str):
        """
        Add a new proxy to the list of valid proxies if it is valid.

        Args:
            proxy (str): The proxy string to add.
        """
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
        """
        Remove a proxy from the list of valid proxies.

        Args:
            proxy (str): The proxy string to remove.
        """
        with self.lock:
            self.valid_proxies = [
                p for p in self.valid_proxies if p.proxy != proxy
            ]
            self.index = 0

    def get_all_proxies(self) -> list[Proxy]:
        """
        Get a copy of all valid proxies.

        Returns:
            List[Proxy]: A list of all valid proxies.
        """
        with self.lock:
            return self.valid_proxies.copy()

    def validate_proxies(self):
        """
        Validate and update the list of valid proxies from the initial set.
        """
        with self.lock:
            proxies = list(set(self.proxies))
            self.valid_proxies = valid_proxies(proxies)
