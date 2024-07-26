from __future__ import annotations

import requests  # type: ignore
from rea_beta_backend_toolsets.services.proxies.proxy import (
    ProxyRotationManager,
)
from rea_beta_backend_toolsets.services.user_agents.user_agent import (
    UserAgentRotationManager,
)


class RequestManager:

    def __init__(
        self,
        user_agents: list[str] | None = [],
        proxies: list[str] = [],
    ):
        self.user_agent_rotation_manager: UserAgentRotationManager
        self.proxy_rotation_manager: ProxyRotationManager
        self.reset(user_agents, proxies)
        self.status()

    def reset(
        self,
        user_agents: list[str] | None = [],
        proxies: list[str] = [],
    ):
        self.user_agent_rotation_manager = UserAgentRotationManager(
            user_agents or [],
        )
        self.proxy_rotation_manager = ProxyRotationManager(
            proxies or [],
        )

    def status(self):
        self.proxy_rotation_manager.status()
        self.user_agent_rotation_manager.status()

    def _get_proxy_dict(self) -> dict[str, str]:
        proxy = self.proxy_rotation_manager.get_next_proxy()
        return {
            'http': f'http://{proxy.proxy}',
            'https': f'http://{proxy.proxy}',
        }

    def _get_headers(self) -> dict[str, str]:
        user_agent = self.user_agent_rotation_manager.get_next_user_agent()
        return {'User-Agent': user_agent}

    def _request(
        self, method: str,
        url: str, headers:  dict[str, str] | None = None,
        params: dict[str, str] | None = None, data=None, json=None, timeout=20,
        use_proxy=True, use_user_agent=True,
    ) -> requests.Response | None:

        proxies = self._get_proxy_dict() if use_proxy else {}
        user_agents = self._get_headers() if use_user_agent else {}
        if headers is None:
            headers = {}
        headers.update(user_agents)

        request_func = getattr(requests, method.lower())
        response = request_func(
            url, headers=headers, proxies=proxies,
            params=params, data=data, json=json, timeout=timeout,
        )
        response.raise_for_status()
        return response

    def get(
        self, url: str,
        headers: dict | None = None,
        params: dict | None = None, timeout=20,
        use_proxy=True, use_user_agent=True,
    ) -> requests.Response | None:
        return self._request(
            'GET', url,
            headers=headers,
            params=params,
            timeout=timeout,
            use_proxy=use_proxy, use_user_agent=use_user_agent,
        )

    def post(
        self, url: str,
        headers: dict | None = None,
        params: dict | None = None, data=None, json=None, timeout=20,
        use_proxy=True, use_user_agent=True,
    ) -> requests.Response | None:
        return self._request(
            'POST', url,
            headers=headers, params=params,
            data=data, json=json, timeout=timeout,
            use_proxy=use_proxy, use_user_agent=use_user_agent,
        )

    def patch(
        self, url: str,
        headers: dict | None = None,
        params: dict | None = None, data=None, json=None, timeout=20,
        use_proxy=True, use_user_agent=True,
    ) -> requests.Response | None:
        return self._request(
            'PATCH', url,
            headers=headers, params=params,
            data=data, json=json, timeout=timeout,
            use_proxy=use_proxy, use_user_agent=use_user_agent,
        )

    def put(
        self, url:
        str, headers: dict | None = None,
        params: dict | None = None, data=None, json=None, timeout=20,
        use_proxy=True, use_user_agent=True,
    ) -> requests.Response | None:
        return self._request(
            'PUT', url,
            headers=headers, params=params,
            data=data, json=json, timeout=timeout,
            use_proxy=use_proxy, use_user_agent=use_user_agent,
        )
