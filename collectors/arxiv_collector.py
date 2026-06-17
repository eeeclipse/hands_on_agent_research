"""
arXiv 논문 수집기
arXiv API(Atom feed)를 통해 최신 추천 시스템 논문을 수집합니다.
"""

import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from typing import List

import feedparser
from rich.console import Console

from models import Paper
from quality_report import SourceQualityStats
import config

console = Console()


def _build_arxiv_query(query: str, categories: List[str]) -> str:
    """arXiv API 검색 URL 생성"""
    cat_filter = " OR ".join(f"cat:{c}" for c in categories)
    full_query = f"({query}) AND ({cat_filter})"
    encoded = urllib.parse.quote(full_query)
    return (
        f"https://export.arxiv.org/api/query?"
        f"search_query={encoded}"
        f"&sortBy=submittedDate&sortOrder=descending"
        f"&max_results={config.ARXIV_MAX_RESULTS}"
    )


def _parse_entry(entry) -> Paper:
    """feedparser entry → Paper 변환"""
    arxiv_id = entry.id.split("/abs/")[-1]
    authors = [a.name for a in getattr(entry, "authors", [])]

    # 날짜 파싱 (published vs updated 둘 다 처리)
    raw_date = getattr(entry, "published", None) or getattr(entry, "updated", "")
    try:
        published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
    except Exception:
        published = datetime.now(timezone.utc)

    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}"
    abs_url = f"https://arxiv.org/abs/{arxiv_id}"

    categories = [
        tag.term for tag in getattr(entry, "tags", [])
    ]

    return Paper(
        arxiv_id=arxiv_id,
        title=entry.title.replace("\n", " ").strip(),
        authors=authors,
        abstract=entry.summary.replace("\n", " ").strip(),
        url=abs_url,
        pdf_url=pdf_url,
        published=published,
        categories=categories,
    )


def collect_papers(report=None) -> List[Paper]:
    """
    설정된 모든 쿼리로 arXiv 논문 수집 후 중복 제거 및 날짜 필터링.
    Returns: 최근 ARXIV_DAYS_BACK 일 이내의 Paper 목록
    """
    cutoff = datetime.now(timezone.utc) - timedelta(days=config.ARXIV_DAYS_BACK)
    seen_ids: set = set()
    papers: List[Paper] = []

    console.print(f"[bold cyan]📡 arXiv 수집 시작[/] (최근 {config.ARXIV_DAYS_BACK}일, {len(config.ARXIV_QUERIES)}개 쿼리)")

    for query in config.ARXIV_QUERIES:
        url = _build_arxiv_query(query, config.ARXIV_CATEGORIES)
        stats = SourceQualityStats(source_type="arxiv", name=f"query: {query}", url=url)
        if report is not None:
            report.paper_sources.append(stats)
        try:
            feed = feedparser.parse(url)
            stats.fetched_count = len(feed.entries)
        except Exception as e:
            stats.failure = str(e)
            console.print(f"  [red]쿼리 실패:[/] {query[:50]}… → {e}")
            continue

        new_count = 0
        for entry in feed.entries:
            paper = _parse_entry(entry)
            if paper.arxiv_id in seen_ids:
                stats.duplicate_count += 1
                continue
            if paper.published < cutoff:
                stats.old_count += 1
                continue
            seen_ids.add(paper.arxiv_id)
            papers.append(paper)
            stats.added_count += 1
            new_count += 1

        console.print(f"  [green]✓[/] [{query[:45]:45s}] → {new_count}편 수집")
        time.sleep(0.5)   # arXiv rate-limit 준수

    console.print(f"[bold]총 {len(papers)}편 수집 완료[/] (중복 제거 후)\n")
    return papers
