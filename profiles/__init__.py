"""
프로필 로더 — phd / industry 프로필을 동적으로 로드합니다.
"""

import importlib
from types import ModuleType

AVAILABLE_PROFILES = ["phd", "industry"]


def load_profile(name: str) -> ModuleType:
    """프로필 이름으로 설정 모듈을 로드합니다."""
    if name not in AVAILABLE_PROFILES:
        raise ValueError(
            f"알 수 없는 프로필: '{name}'. "
            f"사용 가능: {', '.join(AVAILABLE_PROFILES)}"
        )
    mapping = {
        "phd": "profiles.phd_research",
        "industry": "profiles.industry",
    }
    return importlib.import_module(mapping[name])
