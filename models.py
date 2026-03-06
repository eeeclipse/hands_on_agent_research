"""
데이터 모델 정의
"""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass
class Paper:
    """arXiv 논문 데이터"""
    arxiv_id: str
    title: str
    authors: List[str]
    abstract: str
    url: str
    pdf_url: str
    published: datetime
    categories: List[str]
    # 이후 단계에서 채워지는 필드
    relevance_score: float = 0.0
    summary: str = ""
    key_contributions: List[str] = field(default_factory=list)
    relevance_reason: str = ""

    @property
    def author_str(self) -> str:
        if len(self.authors) <= 3:
            return ", ".join(self.authors)
        return f"{self.authors[0]} et al."

    @property
    def published_str(self) -> str:
        return self.published.strftime("%Y-%m-%d")


@dataclass
class BlogPost:
    """기술 블로그 포스트 데이터"""
    source: str
    title: str
    url: str
    published: datetime
    summary: str           # 원문 요약(RSS description)
    content: str = ""      # 전문(선택적으로 크롤링)
    # 이후 단계에서 채워지는 필드
    relevance_score: float = 0.0
    llm_summary: str = ""
    relevance_reason: str = ""

    @property
    def published_str(self) -> str:
        return self.published.strftime("%Y-%m-%d")


@dataclass
class NewsletterSection:
    """뉴스레터 섹션"""
    title: str
    items: list
    section_summary: str = ""


@dataclass
class Newsletter:
    """최종 뉴스레터"""
    generated_at: datetime
    date_range: str
    executive_summary: str
    top_papers: List[Paper]
    top_blogs: List[BlogPost]
    trend_analysis: str
    raw_markdown: str = ""
