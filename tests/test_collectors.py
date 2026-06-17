from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

import config
from collectors import arxiv_collector, blog_collector
from quality_report import CollectionQualityReport


def _entry(identifier, published, title="Paper", summary="Abstract", categories=None):
    return SimpleNamespace(
        id=f"https://arxiv.org/abs/{identifier}",
        title=title,
        summary=summary,
        published_parsed=published.timetuple(),
        authors=[SimpleNamespace(name="Ada Lovelace")],
        tags=[SimpleNamespace(term=term) for term in (categories or ["cs.LG"])],
    )


def test_collect_papers_records_query_stats(monkeypatch):
    now = datetime.now(timezone.utc)
    monkeypatch.setattr(config, "ARXIV_QUERIES", ["LLM agent"])
    monkeypatch.setattr(config, "ARXIV_CATEGORIES", ["cs.AI"])
    monkeypatch.setattr(config, "ARXIV_MAX_RESULTS", 15)
    monkeypatch.setattr(config, "ARXIV_DAYS_BACK", 7)
    feed = SimpleNamespace(
        entries=[
            _entry("2601.00001", now),
            _entry("2601.00001", now),
            _entry("2501.00001", now - timedelta(days=30)),
        ]
    )
    monkeypatch.setattr(arxiv_collector.feedparser, "parse", lambda url: feed)
    monkeypatch.setattr(arxiv_collector.time, "sleep", lambda seconds: None)
    report = CollectionQualityReport(
        "industry", "Industry Practice", 7, 0.35, now.replace(tzinfo=None)
    )

    papers = arxiv_collector.collect_papers(report=report)

    assert len(papers) == 1
    stats = report.paper_sources[0]
    assert stats.fetched_count == 3
    assert stats.added_count == 1
    assert stats.duplicate_count == 1
    assert stats.old_count == 1


def test_collect_blogs_records_feed_stats(monkeypatch):
    now = datetime.now(timezone.utc)
    monkeypatch.setattr(
        config,
        "BLOG_FEEDS",
        [{"name": "Example", "url": "https://example.com/feed", "tags": ["agent"]}],
    )
    monkeypatch.setattr(config, "BLOG_DAYS_BACK", 7)
    monkeypatch.setattr(config, "BLOG_KEYWORDS", ["agent"])
    entries = [
        SimpleNamespace(
            title="Useful agent post",
            summary="An LLM agent article",
            link="https://example.com/a",
            published_parsed=now.timetuple(),
        ),
        SimpleNamespace(
            title="Unrelated post",
            summary="Cooking notes",
            link="https://example.com/b",
            published_parsed=now.timetuple(),
        ),
    ]
    monkeypatch.setattr(
        blog_collector.feedparser,
        "parse",
        lambda url: SimpleNamespace(entries=entries),
    )
    monkeypatch.setattr(blog_collector, "_fetch_full_text", lambda url: "")
    monkeypatch.setattr(blog_collector.time, "sleep", lambda seconds: None)
    report = CollectionQualityReport(
        "industry", "Industry Practice", 7, 0.35, now.replace(tzinfo=None)
    )

    posts = blog_collector.collect_blogs(report=report)

    assert len(posts) == 1
    stats = report.blog_sources[0]
    assert stats.fetched_count == 2
    assert stats.added_count == 1
    assert stats.keyword_filtered_count == 1
    assert stats.full_text_attempt_count == 1
    assert stats.full_text_success_count == 0
