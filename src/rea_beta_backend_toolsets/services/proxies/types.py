from __future__ import annotations

from typing import TypedDict


class Proxy(TypedDict):
    ip: str
    proxy: str
    hostname: str
    city: str
    region: str
    country: str
    loc: str
    org: str
    postal: str
    timezone: str
    readme: str
    duration: float
