"""
뉴스레터 생성 모듈
Jinja2 템플릿을 사용하여 Markdown 뉴스레터를 렌더링합니다.
"""

import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import List

from jinja2 import Environment, BaseLoader
from rich.console import Console

from models import Paper, BlogPost, Newsletter
import config

console = Console()

# ── Jinja2 Markdown 템플릿 ────────────────────────────────────────────────────
_NEWSLETTER_TEMPLATE = """\
# 📚 RecSys Research Digest — {{ newsletter.date_range }}

> 자동 생성: {{ newsletter.generated_at.strftime('%Y-%m-%d %H:%M') }} | \
팀 연구 주제 기반 시맨틱 필터링 적용

---

## 🧠 Executive Summary

{{ newsletter.executive_summary }}

---

## 📄 Top Papers This Week

{% for paper in newsletter.top_papers %}
### {{ loop.index }}. {{ paper.title }}

| 항목 | 내용 |
|------|------|
| **저자** | {{ paper.author_str }} |
| **발행일** | {{ paper.published_str }} |
| **카테고리** | {{ paper.categories[:3] | join(', ') }} |
| **관련성 점수** | {{ "%.3f" | format(paper.relevance_score) }} |
| **arXiv** | [링크]({{ paper.url }}) \| [PDF]({{ paper.pdf_url }}) |

**요약:** {{ paper.summary }}

**핵심 기여:**
{% for contrib in paper.key_contributions %}
- {{ contrib }}
{% endfor %}

**팀 관련성:** {{ paper.relevance_reason }}

---
{% endfor %}

## 🏭 Industry Blog Highlights

{% for post in newsletter.top_blogs %}
### {{ loop.index }}. [{{ post.title }}]({{ post.url }})

| 항목 | 내용 |
|------|------|
| **출처** | {{ post.source }} |
| **발행일** | {{ post.published_str }} |
| **관련성 점수** | {{ "%.3f" | format(post.relevance_score) }} |

{{ post.llm_summary }}

**팀 관련성:** {{ post.relevance_reason }}

---
{% endfor %}

## 📈 이번 주 트렌드 분석

### Emerging Trends
{% for trend in trends.get('emerging_trends', []) %}
- {{ trend }}
{% endfor %}

### 팀 액션 아이템
{% for action in trends.get('team_recommendations', []) %}
- [ ] {{ action }}
{% endfor %}

---

*이 뉴스레터는 RecSys Research Agent가 자동 생성했습니다.*
*arXiv + {{ newsletter.top_blogs | length }}개 기술 블로그 → 시맨틱 필터링(threshold={{ threshold }}) → LLM 요약*
"""


def render_newsletter(
    papers: List[Paper],
    blogs: List[BlogPost],
    trends: dict,
    date_range: str = "",
) -> str:
    """
    뉴스레터 Markdown 문자열 생성
    """
    if not date_range:
        end = datetime.now()
        start = end - timedelta(days=config.ARXIV_DAYS_BACK)
        date_range = f"{start.strftime('%Y-%m-%d')} ~ {end.strftime('%Y-%m-%d')}"

    newsletter = Newsletter(
        generated_at=datetime.now(),
        date_range=date_range,
        executive_summary=trends.get("executive_summary", ""),
        top_papers=papers,
        top_blogs=blogs,
        trend_analysis="",
    )

    env = Environment(loader=BaseLoader())
    template = env.from_string(_NEWSLETTER_TEMPLATE)
    rendered = template.render(
        newsletter=newsletter,
        trends=trends,
        threshold=config.RELEVANCE_THRESHOLD,
    )
    return rendered


def save_newsletter(markdown: str) -> Path:
    """Markdown 파일로 저장하고 경로 반환"""
    output_dir = Path(config.OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    filename = config.NEWSLETTER_FILENAME.format(
        date=datetime.now().strftime("%Y%m%d")
    )
    path = output_dir / filename
    path.write_text(markdown, encoding="utf-8")
    console.print(f"[bold green]💾 뉴스레터 저장됨:[/] {path}")
    return path
