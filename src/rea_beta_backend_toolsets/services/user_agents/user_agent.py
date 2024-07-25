from __future__ import annotations

import random
import threading

from .helpers import generate_unique_user_agents
from .helpers import valid_user_agents
from .validation import is_valid


class UserAgentRotationManager:
    def __init__(self, user_agents: list[str] | None = None):

        self.lock = threading.Lock()
        self.user_agents = self._user_agents_copy(user_agents)
        self.valid_user_agents: list[str] = []
        self.index = 0
        self.validate_user_agents()

    def _user_agents_copy(
        self,
        user_agents: list[str] | None = None,
    ) -> list[str]:
        if user_agents and len(user_agents) > 0:
            return user_agents.copy()
        return generate_unique_user_agents()

    def get_next_user_agent(self) -> str:

        with self.lock:
            if not self.valid_user_agents:
                raise ValueError('No user agents available')

            user_agent = self.valid_user_agents[self.index]
            self.index = (self.index + 1) % len(self.valid_user_agents)
            return user_agent

    def add_user_agent(self, user_agent: str):

        with self.lock:
            if not is_valid(user_agent):
                raise ValueError(f'Invalid user agent: {user_agent}')
            self.valid_user_agents.append(user_agent)
            random.shuffle(self.valid_user_agents)

    def remove_user_agent(self, user_agent: str):

        with self.lock:
            self.valid_user_agents = [
                ua for ua in self.valid_user_agents if ua != user_agent
            ]
            self.index = 0
            random.shuffle(self.valid_user_agents)

    def get_all_user_agents(self) -> list[str]:

        with self.lock:
            return self.valid_user_agents.copy()

    def validate_user_agents(self):

        with self.lock:
            user_agents = list(set(self.user_agents))
            self.valid_user_agents = valid_user_agents(user_agents)
