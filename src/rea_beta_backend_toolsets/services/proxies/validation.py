from __future__ import annotations

import re
import time

import requests  # type: ignore
from requests.exceptions import ConnectTimeout  # type: ignore
from requests.exceptions import HTTPError
from requests.exceptions import ProxyError
from requests.exceptions import ReadTimeout
from requests.exceptions import SSLError

from .constants import PROXY_PROXY_CHECKER_URL
from .constants import PROXY_TIME_OUT_VALIDATION
from .types import Proxy

proxy_pattern = re.compile(
    r'^'
    r'(?:(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.){3}'
    r'(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])'
    r':'
    r'(?:6553[0-5]|655[0-2][0-9]|65[0-4][0-9]{2}|6[0-4][0-9]{3}|'
    r'[1-5][0-9]{4}|[1-9][0-9]{0,3})'
    r'$',
)


def check_proxy(url: str, proxy: str) -> bool:
    proxies = {'http': proxy, 'https': proxy}
    for _ in range(3):
        try:
            response = requests.get(
                url, proxies=proxies, timeout=PROXY_TIME_OUT_VALIDATION,
            )
            if response.status_code == 200 and 'Server' in response.headers:
                return 'cloudflare' in response.headers['Server'].lower()
        except (
            ProxyError,
            ConnectTimeout,
            SSLError,
            ReadTimeout,
            ConnectionError,
            HTTPError,
        ):
            time.sleep(2)
        except Exception:
            pass

    return False


def is_valid_format(proxy: str) -> bool:
    return (
        bool(proxy.strip())
        and proxy_pattern.match(proxy) is not None
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

            return Proxy(
                ip=data.get('ip'),
                proxy=proxy,
                hostname=data.get('hostname'),
                city=data.get('city'),
                region=data.get('region'),
                country=data.get('country'),
                loc=data.get('loc'),
                org=data.get('org'),
                postal=data.get('postal'),
                timezone=data.get('timezone'),
                readme=data.get('readme'),
                duration=duration,
            )
    except requests.RequestException:
        pass
    return None


def is_valid(proxy: str) -> Proxy | None:

    # if not check_proxy('https://www.cloudflare.com/', proxy):
    #     return None

    # if not check_proxy('https://www.google.com/', proxy):
    #     return None

    return is_valid_request(proxy) if is_valid_format(proxy) else None
