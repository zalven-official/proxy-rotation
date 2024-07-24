from __future__ import annotations

from pydantic import BaseModel


class Proxy(BaseModel):
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
