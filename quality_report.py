from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


@dataclass
class SourceQualityStats:
    source_type: str
    name: str
    url: str = ""
    fetched_count: int = 0
    added_count: int = 0
    duplicate_count: int = 0
    old_count: int = 0
    keyword_filtered_count: int = 0
    full_text_attempt_count: int = 0
    full_text_success_count: int = 0
    failure: str = ""


@dataclass
class CollectionQualityReport:
    profile_key: str
    profile_name: str
    days_back: int
    threshold: float
    generated_at: datetime
    paper_sources: list[SourceQualityStats] = field(default_factory=list)
    blog_sources: list[SourceQualityStats] = field(default_factory=list)
    paper_selected_count: int = 0
    blog_selected_count: int = 0

    @property
    def paper_added_count(self) -> int:
        return sum(source.added_count for source in self.paper_sources)

    @property
    def blog_added_count(self) -> int:
        return sum(source.added_count for source in self.blog_sources)

    def to_markdown(self) -> str:
        generated = self.generated_at.strftime("%Y-%m-%d %H:%M")
        lines = [
            f"# Collection Quality Report — {self.profile_name}",
            "",
            f"> Generated: {generated} | Window: {self.days_back} days | Threshold: {self.threshold:.2f}",
            "",
            "## Summary",
            "",
            "| Metric | Count |",
            "|---|---:|",
            f"| Papers added | {self.paper_added_count} |",
            f"| Papers selected | {self.paper_selected_count} |",
            f"| Blogs added | {self.blog_added_count} |",
            f"| Blogs selected | {self.blog_selected_count} |",
            "",
            "## arXiv Queries",
            "",
        ]
        lines.extend(_render_source_table(self.paper_sources))
        lines.extend(["", "## Blog Feeds", ""])
        lines.extend(_render_source_table(self.blog_sources))
        lines.append("")
        return "\n".join(lines)


def _render_source_table(sources: list[SourceQualityStats]) -> list[str]:
    if not sources:
        return ["_No sources recorded._"]

    lines = [
        "| Source | URL/Query | Fetched | Added | Duplicates | Old | Keyword Filtered | Full Text | Failure |",
        "|---|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for source in sources:
        full_text = f"{source.full_text_success_count}/{source.full_text_attempt_count}"
        lines.append(
            "| "
            f"{source.name} | "
            f"{source.url} | "
            f"{source.fetched_count} | "
            f"{source.added_count} | "
            f"{source.duplicate_count} | "
            f"{source.old_count} | "
            f"{source.keyword_filtered_count} | "
            f"{full_text} | "
            f"{source.failure or '-'} |"
        )
    return lines


def save_quality_report(report: CollectionQualityReport, output_dir: str | Path) -> Path:
    directory = Path(output_dir) / "quality_reports"
    directory.mkdir(parents=True, exist_ok=True)
    filename = f"{report.profile_key}_quality_{report.generated_at.strftime('%Y%m%d')}.md"
    path = directory / filename
    path.write_text(report.to_markdown(), encoding="utf-8")
    return path
