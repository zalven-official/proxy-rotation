from __future__ import annotations

import random
from concurrent.futures import ThreadPoolExecutor

import requests  # type: ignore

from .constants import USER_AGENT_LIST_URL
from .validation import is_valid


def valid_user_agents(user_agents: list[str], randomize=False) -> list[str]:
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(is_valid, user_agents))

    valid_results = [result for result in results if result is not None]
    if randomize:
        random.shuffle(valid_results)
    return valid_results


def generate_unique_user_agents() -> list[str]:
    response = requests.get(USER_AGENT_LIST_URL)
    response.raise_for_status()

    user_agents = list(set(response.text.splitlines()))
    user_agents = valid_user_agents(user_agents)

    return list(user_agents)
