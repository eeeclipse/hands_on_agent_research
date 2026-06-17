from datetime import datetime

from quality_report import CollectionQualityReport, SourceQualityStats, save_quality_report


def test_quality_report_renders_summary_and_sources(tmp_path):
    report = CollectionQualityReport(
        profile_key="industry",
        profile_name="Industry Practice",
        days_back=7,
        threshold=0.35,
        generated_at=datetime(2026, 6, 17, 9, 30),
    )
    report.paper_sources.append(
        SourceQualityStats(
            source_type="arxiv",
            name="query: LLM agent",
            fetched_count=12,
            added_count=5,
            duplicate_count=2,
            old_count=1,
        )
    )
    report.blog_sources.append(
        SourceQualityStats(
            source_type="blog",
            name="OpenAI Blog",
            url="https://openai.com/blog/rss.xml",
            fetched_count=4,
            added_count=1,
            keyword_filtered_count=2,
            full_text_attempt_count=1,
            full_text_success_count=1,
        )
    )
    report.paper_selected_count = 3
    report.blog_selected_count = 1

    markdown = report.to_markdown()

    assert "# Collection Quality Report — Industry Practice" in markdown
    assert "| Papers added | 5 |" in markdown
    assert "| Papers selected | 3 |" in markdown
    assert "OpenAI Blog" in markdown
    assert "https://openai.com/blog/rss.xml" in markdown


def test_save_quality_report_uses_profile_and_date(tmp_path):
    report = CollectionQualityReport(
        profile_key="phd",
        profile_name="PhD Research",
        days_back=7,
        threshold=0.35,
        generated_at=datetime(2026, 6, 17, 9, 30),
    )

    path = save_quality_report(report, output_dir=tmp_path)

    assert path == tmp_path / "quality_reports" / "phd_quality_20260617.md"
    assert path.exists()
    assert "PhD Research" in path.read_text(encoding="utf-8")
