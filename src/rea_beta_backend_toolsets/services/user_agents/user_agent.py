from __future__ import annotations

import random
import threading

from .helpers import is_valid
from .helpers import valid_user_agents


class UserAgentRotation:
    def __init__(self, user_agents: list[str]):
        """
        Initialize the UserAgentRotation class with a list of user agents.

        Args:
            user_agents (List[str]): Initial list of user agent strings.
        """
        self.lock = threading.Lock()
        self.user_agents = user_agents.copy()
        self.valid_user_agents: list[str] = []
        self.index = 0
        self.validate_user_agents()

    def get_next_user_agent(self) -> str:
        """
        Get the next user agent in the rotation.

        Returns:
            str: The next user agent string.

        Raises:
            ValueError: If no user agents are available.
        """
        with self.lock:
            if not self.valid_user_agents:
                raise ValueError('No user agents available')

            user_agent = self.valid_user_agents[self.index]
            self.index = (self.index + 1) % len(self.valid_user_agents)
            return user_agent

    def add_user_agent(self, user_agent: str):
        """
        Add a new user agent to the list if it is valid.

        Args:
            user_agent (str): The user agent string to add.

        Raises:
            ValueError: If the user agent string is invalid.
        """
        with self.lock:
            if not is_valid(user_agent):
                raise ValueError(f'Invalid user agent: {user_agent}')
            self.valid_user_agents.append(user_agent)
            random.shuffle(self.valid_user_agents)

    def remove_user_agent(self, user_agent: str):
        """
        Remove a user agent from the list.

        Args:
            user_agent (str): The user agent string to remove.
        """
        with self.lock:
            self.valid_user_agents = [
                ua for ua in self.valid_user_agents if ua != user_agent
            ]
            self.index = 0
            random.shuffle(self.valid_user_agents)

    def get_all_user_agents(self) -> list[str]:
        """
        Get a copy of all user agents.

        Returns:
            List[str]: A list of all user agent strings.
        """
        with self.lock:
            return self.valid_user_agents.copy()

    def validate_user_agents(self):
        """
        Validate and update the list of valid user agents from the initial set.
        """
        with self.lock:
            user_agents = list(set(self.user_agents))
            self.valid_user_agents = valid_user_agents(user_agents)
