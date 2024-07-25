from __future__ import annotations

from pydantic import BaseModel


class Proxy(BaseModel):
    ip: str | None = None
    proxy: str
    hostname: str | None = None
    city: str | None = None
    region: str | None = None
    country: str | None = None
    loc: str | None = None
    org: str | None = None
    postal: str | None = None
    timezone: str | None = None
    readme: str | None = None
    duration: float | None = None
