from __future__ import annotations

import random
import threading


class UserAgent:
    def __init__(self, user_agents: list[str]):
        """
        Initialize the UserAgent class with a list of user agents.

        Args:
            user_agents (List[str]): Initial list of user agent strings.
        """
        self.lock = threading.Lock()
        self.user_agents = user_agents.copy()
        self.index = 0
        random.shuffle(self.user_agents)

    def get_next_user_agent(self) -> str:
        """
        Get the next user agent in the rotation.

        Returns:
            str: The next user agent string.

        Raises:
            ValueError: If no user agents are available.
        """
        with self.lock:
            if not self.user_agents:
                raise ValueError('No user agents available')

            user_agent = self.user_agents[self.index]
            self.index = (self.index + 1) % len(self.user_agents)
            return user_agent

    def add_user_agent(self, user_agent: str):
        """
        Add a new user agent to the list.

        Args:
            user_agent (str): The user agent string to add.
        """
        with self.lock:
            self.user_agents.append(user_agent)
            random.shuffle(self.user_agents)  # Re-randomize the list

    def remove_user_agent(self, user_agent: str):
        """
        Remove a user agent from the list.

        Args:
            user_agent (str): The user agent string to remove.
        """
        with self.lock:
            self.user_agents = [
                ua for ua in self.user_agents if ua != user_agent
            ]
            self.index = 0
            random.shuffle(self.user_agents)  # Re-randomize the list

    def get_all_user_agents(self) -> list[str]:
        """
        Get a copy of all user agents.

        Returns:
            List[str]: A list of all user agent strings.
        """
        with self.lock:
            return self.user_agents.copy()
