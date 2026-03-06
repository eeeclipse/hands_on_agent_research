"""
LLM 기반 요약 및 관련성 평가 모듈
Anthropic Claude API의 tool_use를 활용하여 구조화된 출력을 생성합니다.
"""

import json
import os
from typing import List

import anthropic
from rich.console import Console

from models import Paper, BlogPost
import config

console = Console()

# Anthropic 클라이언트 (모듈 로드 시 한 번 초기화)
_client: anthropic.Anthropic = None


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not api_key:
            raise EnvironmentError("ANTHROPIC_API_KEY 환경 변수가 설정되지 않았습니다.")
        _client = anthropic.Anthropic(api_key=api_key)
    return _client


# ── 논문 요약 Tool Schema ────────────────────────────────────────────────────
_PAPER_SUMMARY_TOOL = {
    "name": "summarize_paper",
    "description": "Summarize an academic paper for a RecSys research team newsletter.",
    "input_schema": {
        "type": "object",
        "properties": {
            "one_line_summary": {
                "type": "string",
                "description": "One sentence (≤30 words) capturing the paper's core contribution.",
            },
            "key_contributions": {
                "type": "array",
                "items": {"type": "string"},
                "description": "3-4 bullet points of key technical contributions.",
            },
            "relevance_reason": {
                "type": "string",
                "description": "1-2 sentences explaining why this is relevant to RecSys researchers.",
            },
        },
        "required": ["one_line_summary", "key_contributions", "relevance_reason"],
    },
}

# ── 블로그 요약 Tool Schema ──────────────────────────────────────────────────
_BLOG_SUMMARY_TOOL = {
    "name": "summarize_blog",
    "description": "Summarize a tech blog post for a RecSys research team newsletter.",
    "input_schema": {
        "type": "object",
        "properties": {
            "one_line_summary": {
                "type": "string",
                "description": "One sentence (≤30 words) capturing the post's main point.",
            },
            "key_takeaways": {
                "type": "array",
                "items": {"type": "string"},
                "description": "2-3 practical takeaways for RecSys practitioners.",
            },
            "relevance_reason": {
                "type": "string",
                "description": "1-2 sentences on relevance to the team's research topics.",
            },
        },
        "required": ["one_line_summary", "key_takeaways", "relevance_reason"],
    },
}

# ── 트렌드 분석 Tool Schema ──────────────────────────────────────────────────
_TREND_TOOL = {
    "name": "analyze_trends",
    "description": "Analyze weekly RecSys research trends from papers and blogs.",
    "input_schema": {
        "type": "object",
        "properties": {
            "executive_summary": {
                "type": "string",
                "description": "2-3 paragraph executive summary of this week's RecSys research landscape.",
            },
            "emerging_trends": {
                "type": "array",
                "items": {"type": "string"},
                "description": "3-5 emerging research trends or themes observed this week.",
            },
            "team_recommendations": {
                "type": "array",
                "items": {"type": "string"},
                "description": "2-3 specific action items or reading priorities for the team.",
            },
        },
        "required": ["executive_summary", "emerging_trends", "team_recommendations"],
    },
}


def _call_llm(system: str, user: str, tools: list, tool_name: str) -> dict:
    """
    Claude API 호출 (tool_use 강제)
    Returns: tool_use input dict
    """
    client = _get_client()
    response = client.messages.create(
        model=config.LLM_MODEL,
        max_tokens=config.LLM_MAX_TOKENS,
        system=system,
        messages=[{"role": "user", "content": user}],
        tools=tools,
        tool_choice={"type": "auto"},
    )
    for block in response.content:
        if block.type == "tool_use" and block.name == tool_name:
            return block.input
    # Fallback: 텍스트 응답에서 JSON 추출 시도
    for block in response.content:
        if hasattr(block, "text"):
            try:
                return json.loads(block.text)
            except Exception:
                pass
    return {}


def summarize_paper(paper: Paper) -> Paper:
    """논문에 LLM 요약을 채워 반환"""
    system = (
        "You are an expert RecSys researcher writing concise, insightful summaries "
        "for a team newsletter. Focus on novelty, technical depth, and practical relevance. "
        "Always respond in the same language as the input (English for English papers)."
    )
    user = (
        f"Title: {paper.title}\n"
        f"Authors: {paper.author_str}\n"
        f"Abstract:\n{paper.abstract}\n\n"
        f"Team research topics for context:\n"
        + "\n".join(f"- {t}" for t in config.TEAM_RESEARCH_TOPICS)
    )

    result = _call_llm(system, user, [_PAPER_SUMMARY_TOOL], "summarize_paper")

    paper.summary = result.get("one_line_summary", "")
    paper.key_contributions = result.get("key_contributions", [])
    paper.relevance_reason = result.get("relevance_reason", "")
    return paper


def summarize_blog(post: BlogPost) -> BlogPost:
    """블로그 포스트에 LLM 요약을 채워 반환"""
    system = (
        "You are an expert RecSys researcher writing concise, insightful blog summaries "
        "for a team newsletter. Extract practical engineering insights and research implications."
    )
    body = post.content[:2000] if post.content else post.summary
    user = (
        f"Source: {post.source}\n"
        f"Title: {post.title}\n"
        f"Content:\n{body}\n\n"
        f"Team research topics for context:\n"
        + "\n".join(f"- {t}" for t in config.TEAM_RESEARCH_TOPICS)
    )

    result = _call_llm(system, user, [_BLOG_SUMMARY_TOOL], "summarize_blog")

    post.llm_summary = result.get("one_line_summary", "")
    # key_takeaways를 relevance_reason 필드에 병합 저장 (모델 간소화)
    takeaways = result.get("key_takeaways", [])
    post.relevance_reason = result.get("relevance_reason", "")
    if takeaways:
        post.llm_summary += "\n" + "\n".join(f"• {t}" for t in takeaways)
    return post


def analyze_trends(papers: List[Paper], blogs: List[BlogPost]) -> dict:
    """
    상위 논문 + 블로그를 바탕으로 이번 주 트렌드 분석 생성
    Returns: {executive_summary, emerging_trends, team_recommendations}
    """
    console.print("[bold cyan]🧠 트렌드 분석 중...[/]")

    paper_summaries = "\n".join(
        f"[Paper] {p.title}: {p.summary}" for p in papers[:8]
    )
    blog_summaries = "\n".join(
        f"[Blog/{b.source}] {b.title}: {b.llm_summary.split(chr(10))[0]}"
        for b in blogs[:5]
    )

    system = (
        "You are a senior RecSys researcher synthesizing weekly research highlights. "
        "Identify cross-cutting themes, emerging directions, and actionable insights for the team."
    )
    user = (
        f"This week's top RecSys papers and blog posts:\n\n"
        f"{paper_summaries}\n\n"
        f"{blog_summaries}\n\n"
        f"Team's current research focus areas:\n"
        + "\n".join(f"- {t}" for t in config.TEAM_RESEARCH_TOPICS)
    )

    result = _call_llm(system, user, [_TREND_TOOL], "analyze_trends")
    console.print("[green]✓[/] 트렌드 분석 완료\n")
    return result


def batch_summarize_papers(papers: List[Paper]) -> List[Paper]:
    """논문 목록 전체에 요약 적용 (진행 상황 출력)"""
    console.print(f"[bold cyan]✍️  논문 요약 시작[/] ({len(papers)}편)")
    for i, paper in enumerate(papers, 1):
        try:
            summarize_paper(paper)
            console.print(f"  [{i:02d}/{len(papers):02d}] {paper.title[:65]}…")
        except Exception as e:
            console.print(f"  [red]요약 실패:[/] {paper.title[:50]} → {e}")
            paper.summary = paper.abstract[:200]
    console.print()
    return papers


def batch_summarize_blogs(posts: List[BlogPost]) -> List[BlogPost]:
    """블로그 포스트 목록 전체에 요약 적용"""
    console.print(f"[bold cyan]✍️  블로그 요약 시작[/] ({len(posts)}편)")
    for i, post in enumerate(posts, 1):
        try:
            summarize_blog(post)
            console.print(f"  [{i:02d}/{len(posts):02d}] {post.title[:65]}…")
        except Exception as e:
            console.print(f"  [red]요약 실패:[/] {post.title[:50]} → {e}")
            post.llm_summary = post.summary[:200]
    console.print()
    return posts
