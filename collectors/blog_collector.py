"""
기술 블로그 수집기
RSS/Atom 피드를 파싱하여 최신 추천 시스템 관련 포스트를 수집합니다.
"""

import time
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from typing import List

import feedparser
import requests
from bs4 import BeautifulSoup
from rich.console import Console

from models import BlogPost
from quality_report import SourceQualityStats
import config

console = Console()

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; RecSysResearchBot/1.0; "
        "+https://github.com/your-org/recsys-research-agent)"
    )
}


def _parse_date(entry) -> datetime:
    """feedparser entry에서 datetime 추출 (UTC)"""
    for attr in ("published_parsed", "updated_parsed"):
        parsed = getattr(entry, attr, None)
        if parsed:
            try:
                return datetime(*parsed[:6], tzinfo=timezone.utc)
            except Exception:
                pass
    return datetime.now(timezone.utc)


def _is_relevant(title: str, summary: str) -> bool:
    """제목/요약에 관련 키워드가 하나라도 포함되면 True"""
    text = (title + " " + summary).lower()
    return any(kw.lower() in text for kw in config.BLOG_KEYWORDS)


def _fetch_full_text(url: str, max_chars: int = 3000) -> str:
    """
    URL에서 본문 텍스트 추출 (선택적). 실패하면 빈 문자열 반환.
    max_chars: LLM 요약 비용 절감을 위해 앞부분만 사용
    """
    try:
        resp = requests.get(url, headers=_HEADERS, timeout=8)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        # article 태그 → main → body 순으로 본문 추출 시도
        for tag in ("article", "main", "body"):
            el = soup.find(tag)
            if el:
                text = el.get_text(separator=" ", strip=True)
                return text[:max_chars]
        return ""
    except Exception:
        return ""


def collect_blogs(report=None) -> List[BlogPost]:
    """
    설정된 RSS 피드에서 최근 BLOG_DAYS_BACK 일 이내 포스트를 수집합니다.
    관련 키워드 사전 필터링 → 본문 일부 크롤링
    """
    cutoff = datetime.now(timezone.utc) - timedelta(days=config.BLOG_DAYS_BACK)
    posts: List[BlogPost] = []

    console.print(f"[bold cyan]📰 블로그 수집 시작[/] (최근 {config.BLOG_DAYS_BACK}일, {len(config.BLOG_FEEDS)}개 피드)")

    for feed_cfg in config.BLOG_FEEDS:
        stats = SourceQualityStats(
            source_type="blog",
            name=feed_cfg["name"],
            url=feed_cfg["url"],
        )
        if report is not None:
            report.blog_sources.append(stats)
        try:
            feed = feedparser.parse(feed_cfg["url"])
            stats.fetched_count = len(feed.entries)
        except Exception as e:
            stats.failure = str(e)
            console.print(f"  [red]피드 파싱 실패:[/] {feed_cfg['name']} → {e}")
            continue

        new_count = 0
        for entry in feed.entries:
            published = _parse_date(entry)
            if published < cutoff:
                stats.old_count += 1
                continue

            title = getattr(entry, "title", "")
            summary = getattr(entry, "summary", "") or getattr(entry, "description", "")
            url = getattr(entry, "link", "")

            # 키워드 사전 필터
            if not _is_relevant(title, summary):
                stats.keyword_filtered_count += 1
                continue

            # 본문 추가 크롤링 (짧은 요약만 있을 경우)
            content = ""
            if len(summary) < 300 and url:
                stats.full_text_attempt_count += 1
                content = _fetch_full_text(url)
                if content:
                    stats.full_text_success_count += 1
                time.sleep(0.3)

            posts.append(BlogPost(
                source=feed_cfg["name"],
                title=title.strip(),
                url=url,
                published=published,
                summary=BeautifulSoup(summary, "html.parser").get_text(strip=True)[:1000],
                content=content,
            ))
            stats.added_count += 1
            new_count += 1

        console.print(f"  [green]✓[/] [{feed_cfg['name']:25s}] → {new_count}편 수집")
        time.sleep(0.5)

    console.print(f"[bold]총 {len(posts)}편 블로그 포스트 수집 완료[/]\n")
    return posts
