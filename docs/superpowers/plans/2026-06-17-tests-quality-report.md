# Tests And Collection Quality Report Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a minimal, network-free test suite and generate a collection quality report for each digest run.

**Architecture:** Keep the existing four-step pipeline intact. Add small pytest tests around current pure functions, then introduce a focused `quality_report.py` module that collectors and `agent.py` can use without changing newsletter rendering responsibilities.

**Tech Stack:** Python 3.11, pytest, dataclasses, uv, existing `feedparser`, `BeautifulSoup`, `rich`, and Markdown output under `output/quality_reports/`.

---

## File Structure

- Modify: `pyproject.toml`
  - Add a `dev` dependency group with `pytest`.
- Create: `tests/test_profiles.py`
  - Verify profile loading and unknown-profile errors.
- Create: `tests/test_newsletter.py`
  - Verify Markdown rendering from in-memory `Paper` and `BlogPost` instances.
- Create: `tests/test_collectors.py`
  - Verify arXiv query construction, arXiv dedupe/date filtering stats, blog keyword/date/full-text stats using monkeypatches.
- Create: `tests/test_quality_report.py`
  - Verify report counters, Markdown rendering, and file saving.
- Create: `quality_report.py`
  - Own report data structures, counter helpers, Markdown rendering, and saving.
- Modify: `collectors/arxiv_collector.py`
  - Accept optional report object and record per-query stats.
- Modify: `collectors/blog_collector.py`
  - Accept optional report object and record per-feed stats.
- Modify: `agent.py`
  - Create the report per run, pass it into collectors, update ranking stats, and save it on success or early exit.
- Modify: `README.md`
  - Document tests and the quality report artifact.

---

### Task 1: Add Pytest Harness

**Files:**
- Modify: `pyproject.toml`
- Create: `tests/test_profiles.py`

- [ ] **Step 1: Add the dev dependency group**

Add this block to `pyproject.toml` after the `[project]` dependencies block:

```toml
[dependency-groups]
dev = [
    "pytest>=8.3.0",
]
```

- [ ] **Step 2: Write profile loading tests**

Create `tests/test_profiles.py`:

```python
import pytest

from profiles import load_profile


def test_load_known_profiles():
    phd = load_profile("phd")
    industry = load_profile("industry")

    assert phd.PROFILE_NAME == "PhD Research"
    assert industry.PROFILE_NAME == "Industry Practice"
    assert phd.TEAM_RESEARCH_TOPICS
    assert industry.BLOG_FEEDS


def test_load_unknown_profile_raises_clear_error():
    with pytest.raises(ValueError, match="알 수 없는 프로필"):
        load_profile("career")
```

- [ ] **Step 3: Run the new test and verify the harness**

Run:

```bash
uv run --group dev pytest tests/test_profiles.py -q
```

Expected:

```text
2 passed
```

- [ ] **Step 4: Commit the harness**

```bash
git add pyproject.toml uv.lock tests/test_profiles.py
git commit -m "test: add pytest harness"
```

---

### Task 2: Add Newsletter Rendering Tests

**Files:**
- Create: `tests/test_newsletter.py`

- [ ] **Step 1: Write the rendering test**

Create `tests/test_newsletter.py`:

```python
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
```

- [ ] **Step 2: Run the focused test**

```bash
uv run --group dev pytest tests/test_newsletter.py -q
```

Expected:

```text
1 passed
```

- [ ] **Step 3: Commit newsletter tests**

```bash
git add tests/test_newsletter.py
git commit -m "test: cover newsletter rendering"
```

---

### Task 3: Add Quality Report Module With Tests First

**Files:**
- Create: `tests/test_quality_report.py`
- Create: `quality_report.py`

- [ ] **Step 1: Write failing tests for report rendering and saving**

Create `tests/test_quality_report.py`:

```python
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
```

- [ ] **Step 2: Run tests and verify failure**

```bash
uv run --group dev pytest tests/test_quality_report.py -q
```

Expected:

```text
ModuleNotFoundError: No module named 'quality_report'
```

- [ ] **Step 3: Implement the quality report module**

Create `quality_report.py`:

```python
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
```

- [ ] **Step 4: Run tests and commit**

```bash
uv run --group dev pytest tests/test_quality_report.py -q
git add quality_report.py tests/test_quality_report.py
git commit -m "feat: add collection quality report model"
```

Expected:

```text
2 passed
```

---

### Task 4: Instrument Collectors With Report Stats

**Files:**
- Modify: `collectors/arxiv_collector.py`
- Modify: `collectors/blog_collector.py`
- Create: `tests/test_collectors.py`

- [ ] **Step 1: Write collector stat tests**

Create `tests/test_collectors.py` with monkeypatched feed responses and no network calls:

```python
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
    config.ARXIV_QUERIES = ["LLM agent"]
    config.ARXIV_CATEGORIES = ["cs.AI"]
    config.ARXIV_MAX_RESULTS = 15
    config.ARXIV_DAYS_BACK = 7
    feed = SimpleNamespace(entries=[
        _entry("2601.00001", now),
        _entry("2601.00001", now),
        _entry("2501.00001", now - timedelta(days=30)),
    ])
    monkeypatch.setattr(arxiv_collector.feedparser, "parse", lambda url: feed)
    monkeypatch.setattr(arxiv_collector.time, "sleep", lambda seconds: None)
    report = CollectionQualityReport("industry", "Industry Practice", 7, 0.35, now.replace(tzinfo=None))

    papers = arxiv_collector.collect_papers(report=report)

    assert len(papers) == 1
    stats = report.paper_sources[0]
    assert stats.fetched_count == 3
    assert stats.added_count == 1
    assert stats.duplicate_count == 1
    assert stats.old_count == 1


def test_collect_blogs_records_feed_stats(monkeypatch):
    now = datetime.now(timezone.utc)
    config.BLOG_FEEDS = [{"name": "Example", "url": "https://example.com/feed", "tags": ["agent"]}]
    config.BLOG_DAYS_BACK = 7
    config.BLOG_KEYWORDS = ["agent"]
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
    monkeypatch.setattr(blog_collector.feedparser, "parse", lambda url: SimpleNamespace(entries=entries))
    monkeypatch.setattr(blog_collector.time, "sleep", lambda seconds: None)
    report = CollectionQualityReport("industry", "Industry Practice", 7, 0.35, now.replace(tzinfo=None))

    posts = blog_collector.collect_blogs(report=report)

    assert len(posts) == 1
    stats = report.blog_sources[0]
    assert stats.fetched_count == 2
    assert stats.added_count == 1
    assert stats.keyword_filtered_count == 1
```

- [ ] **Step 2: Run tests and verify failure**

```bash
uv run --group dev pytest tests/test_collectors.py -q
```

Expected:

```text
TypeError: collect_papers() got an unexpected keyword argument 'report'
```

- [ ] **Step 3: Update `collect_papers`**

Change the signature to:

```python
def collect_papers(report=None) -> List[Paper]:
```

Inside each query loop, create and append stats:

```python
from quality_report import SourceQualityStats

stats = SourceQualityStats(source_type="arxiv", name=f"query: {query}", url=url)
if report is not None:
    report.paper_sources.append(stats)
```

After parsing the feed:

```python
stats.fetched_count = len(feed.entries)
```

Increment:

```python
stats.duplicate_count += 1
stats.old_count += 1
stats.added_count += 1
stats.failure = str(e)
```

- [ ] **Step 4: Update `collect_blogs`**

Change the signature to:

```python
def collect_blogs(report=None) -> List[BlogPost]:
```

Inside each feed loop, create and append stats:

```python
from quality_report import SourceQualityStats

stats = SourceQualityStats(
    source_type="blog",
    name=feed_cfg["name"],
    url=feed_cfg["url"],
)
if report is not None:
    report.blog_sources.append(stats)
```

Increment fetched, old, keyword-filtered, full-text, added, and failure counts at the existing branch points.

- [ ] **Step 5: Run tests and commit**

```bash
uv run --group dev pytest tests/test_collectors.py tests/test_quality_report.py -q
git add collectors/arxiv_collector.py collectors/blog_collector.py tests/test_collectors.py
git commit -m "feat: record collection quality stats"
```

Expected:

```text
4 passed
```

---

### Task 5: Save Quality Reports From Agent Runs

**Files:**
- Modify: `agent.py`
- Create: `tests/test_agent_quality_report.py`

- [ ] **Step 1: Write tests for rank-stat update and early report save**

Create `tests/test_agent_quality_report.py`:

```python
from datetime import datetime, timezone

from agent import update_report_after_rank
from models import BlogPost, Paper
from quality_report import CollectionQualityReport


def test_update_report_after_rank_records_selected_counts():
    report = CollectionQualityReport("industry", "Industry Practice", 7, 0.35, datetime(2026, 6, 17))
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
```

- [ ] **Step 2: Run test and verify failure**

```bash
uv run --group dev pytest tests/test_agent_quality_report.py -q
```

Expected:

```text
ImportError: cannot import name 'update_report_after_rank'
```

- [ ] **Step 3: Add report flow to `agent.py`**

Add imports:

```python
from quality_report import CollectionQualityReport, save_quality_report
```

Change `step_collect`:

```python
def step_collect(days_back: int, report=None):
    console.print(Rule("[bold blue]Step 1: 데이터 수집[/]"))
    config.ARXIV_DAYS_BACK = days_back
    config.BLOG_DAYS_BACK = days_back

    papers = collect_papers(report=report)
    blogs = collect_blogs(report=report)
    return papers, blogs
```

Add helper:

```python
def update_report_after_rank(report, top_papers, top_blogs):
    report.paper_selected_count = len(top_papers)
    report.blog_selected_count = len(top_blogs)
```

In `main`, create the report after `days` and `threshold` are known:

```python
quality_report = CollectionQualityReport(
    profile_key=args.profile,
    profile_name=config.PROFILE_NAME,
    days_back=days,
    threshold=threshold,
    generated_at=datetime.now(),
)
```

Pass it into collection:

```python
papers, blogs = step_collect(days, report=quality_report)
```

Save on early exits and success:

```python
quality_path = save_quality_report(quality_report, config.OUTPUT_DIR)
console.print(f"[bold green]수집 품질 리포트 저장됨:[/] {quality_path}")
```

Call `update_report_after_rank` after ranking and before the no-selected exit.

- [ ] **Step 4: Run focused tests**

```bash
uv run --group dev pytest tests/test_agent_quality_report.py tests/test_quality_report.py -q
```

Expected:

```text
3 passed
```

- [ ] **Step 5: Commit agent integration**

```bash
git add agent.py tests/test_agent_quality_report.py
git commit -m "feat: save quality reports from agent runs"
```

---

### Task 6: Update README And Run Full Verification

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Document test command**

Add under local execution:

````markdown
## 테스트

```bash
uv run --group dev pytest -q
```
````

- [ ] **Step 2: Document quality reports**

Add under output or automation:

```markdown
### 수집 품질 리포트

각 실행은 `output/quality_reports/{profile}_quality_YYYYMMDD.md`를 생성합니다.
리포트에는 arXiv 쿼리별 수집 수, 중복 제거 수, 기간 필터 탈락 수,
블로그 피드별 키워드 필터 탈락 수, 본문 크롤링 성공 수, 최종 선정 수가 포함됩니다.
```

- [ ] **Step 3: Run the complete test suite**

```bash
uv run --group dev pytest -q
```

Expected:

```text
8 passed
```

- [ ] **Step 4: Run a dry-run smoke test**

```bash
uv run --group dev python agent.py --profile industry --dry-run --days 1 --threshold 0.99
```

Expected:

```text
수집 품질 리포트 저장됨: output/quality_reports/industry_quality_YYYYMMDD.md
```

The command may exit early because no item passes the high threshold; that is acceptable if the quality report is saved before exit.

- [ ] **Step 5: Commit docs and lockfile**

```bash
git add README.md uv.lock output/quality_reports/
git commit -m "docs: document quality reports and tests"
```

---

## Final Verification Gate

- [ ] Run:

```bash
git status --short
uv run --group dev pytest -q
uv run --group dev python agent.py --profile industry --dry-run --days 1 --threshold 0.99
```

- [ ] Confirm:
  - Existing untracked `AGENTS.md` remains untouched unless the user asks otherwise.
  - `output/quality_reports/industry_quality_YYYYMMDD.md` is generated.
  - Tests pass without network calls.
  - The dry-run smoke test does not require `ANTHROPIC_API_KEY`.
