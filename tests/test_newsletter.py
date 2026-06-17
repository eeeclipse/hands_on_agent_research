from datetime import datetime, timezone

import config
from models import BlogPost, Paper
from newsletter import render_newsletter


def test_render_newsletter_includes_sections_and_scores():
    config.RELEVANCE_THRESHOLD = 0.42
    paper = Paper(
        arxiv_id="2601.00001",
        title="Test Paper",
        authors=["Ada Lovelace", "Alan Turing"],
        abstract="A test abstract.",
        url="https://arxiv.org/abs/2601.00001",
        pdf_url="https://arxiv.org/pdf/2601.00001",
        published=datetime(2026, 1, 2, tzinfo=timezone.utc),
        categories=["cs.LG"],
        relevance_score=0.512,
        summary="One-line summary.",
        key_contributions=["Contribution A", "Contribution B"],
        relevance_reason="Matches the profile topics.",
    )
    blog = BlogPost(
        source="Example Blog",
        title="Test Blog",
        url="https://example.com/blog",
        published=datetime(2026, 1, 3, tzinfo=timezone.utc),
        summary="RSS summary.",
        relevance_score=0.456,
        llm_summary="Blog summary.",
        relevance_reason="Useful for practice.",
    )
    trends = {
        "executive_summary": "Executive summary.",
        "emerging_trends": ["Trend A"],
        "team_recommendations": ["Read the top paper"],
    }

    markdown = render_newsletter([paper], [blog], trends, "2026-01-01 ~ 2026-01-07")

    assert "# 📚 RecSys Research Digest — 2026-01-01 ~ 2026-01-07" in markdown
    assert "Test Paper" in markdown
    assert "0.512" in markdown
    assert "Test Blog" in markdown
    assert "- [ ] Read the top paper" in markdown
    assert "threshold=0.42" in markdown
