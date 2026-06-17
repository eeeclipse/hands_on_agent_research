from datetime import datetime, timezone

from agent import update_report_after_rank
from models import BlogPost, Paper
from quality_report import CollectionQualityReport


def test_update_report_after_rank_records_selected_counts():
    report = CollectionQualityReport(
        "industry", "Industry Practice", 7, 0.35, datetime(2026, 6, 17)
    )
    paper = Paper(
        arxiv_id="2601.00001",
        title="Paper",
        authors=["Ada"],
        abstract="Abstract",
        url="https://arxiv.org/abs/2601.00001",
        pdf_url="https://arxiv.org/pdf/2601.00001",
        published=datetime(2026, 1, 1, tzinfo=timezone.utc),
        categories=["cs.LG"],
    )
    blog = BlogPost(
        source="Blog",
        title="Post",
        url="https://example.com",
        published=datetime(2026, 1, 1, tzinfo=timezone.utc),
        summary="Summary",
    )

    update_report_after_rank(report, [paper], [blog])

    assert report.paper_selected_count == 1
    assert report.blog_selected_count == 1
