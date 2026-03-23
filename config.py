"""
Agent 설정 파일 — 프로필 기반 동적 로딩

사용법:
    import config
    config.load("phd")       # PhD Research 프로필 로드
    config.load("industry")  # Industry Practice 프로필 로드

프로필 로드 후 config.TEAM_RESEARCH_TOPICS 등 모든 설정에 접근 가능합니다.
"""

from profiles import load_profile

# ── 기본값 (프로필 로드 전) ────────────────────────────────────────────────────────
PROFILE_NAME = ""
PROFILE_DESCRIPTION = ""
TEAM_RESEARCH_TOPICS = []
ARXIV_QUERIES = []
ARXIV_CATEGORIES = []
ARXIV_MAX_RESULTS = 15
ARXIV_DAYS_BACK = 7
BLOG_FEEDS = []
BLOG_DAYS_BACK = 7
BLOG_KEYWORDS = []
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
RELEVANCE_THRESHOLD = 0.35
TOP_N_PAPERS = 10
TOP_N_BLOGS = 5
LLM_MODEL = "claude-opus-4-6"
LLM_MAX_TOKENS = 1024
SUMMARY_MAX_TOKENS = 512
OUTPUT_DIR = "./output"
NEWSLETTER_FILENAME = "digest_{date}.md"

# 프로필에서 복사할 속성 목록
_PROFILE_ATTRS = [
    "PROFILE_NAME", "PROFILE_DESCRIPTION",
    "TEAM_RESEARCH_TOPICS", "ARXIV_QUERIES", "ARXIV_CATEGORIES",
    "ARXIV_MAX_RESULTS", "ARXIV_DAYS_BACK",
    "BLOG_FEEDS", "BLOG_DAYS_BACK", "BLOG_KEYWORDS",
    "EMBEDDING_MODEL", "RELEVANCE_THRESHOLD", "TOP_N_PAPERS", "TOP_N_BLOGS",
    "LLM_MODEL", "LLM_MAX_TOKENS", "SUMMARY_MAX_TOKENS",
    "OUTPUT_DIR", "NEWSLETTER_FILENAME",
]


def load(profile_name: str) -> None:
    """프로필 설정을 config 모듈 전역 변수에 로드합니다."""
    import sys
    profile = load_profile(profile_name)
    this = sys.modules[__name__]
    for attr in _PROFILE_ATTRS:
        if hasattr(profile, attr):
            setattr(this, attr, getattr(profile, attr))
