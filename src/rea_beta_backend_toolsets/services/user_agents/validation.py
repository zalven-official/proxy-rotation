from __future__ import annotations

import re


def is_valid(user_agent: str) -> str | None:

    if user_agent == '':
        return None
    common_keywords = [
        'Mozilla', 'Chrome', 'Safari', 'Firefox', 'Opera', 'MSIE',
        'Trident', 'Edge', 'AppleWebKit', 'Gecko', 'Windows NT',
        'Macintosh', 'Linux', 'Android', 'iPhone', 'iPad',
    ]

    version_regex = re.compile(r'\d+(\.\d+)+')

    if not any(keyword in user_agent for keyword in common_keywords):
        return None

    if not version_regex.search(user_agent):
        return None

    if not user_agent.startswith('Mozilla/'):
        return None

    return user_agent
