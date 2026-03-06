"""
RecSys Research Agent — 메인 오케스트레이션
검색 → 필터링 → 요약 → 뉴스레터 생성의 전체 파이프라인을 실행합니다.

사용법:
    python agent.py                  # 전체 파이프라인 실행
    python agent.py --dry-run        # LLM 요약 없이 수집+랭킹만 실행
    python agent.py --days 14        # 최근 14일 논문 수집
    python agent.py --threshold 0.4  # 관련성 임계값 조정
"""

import argparse
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table

# 로컬 모듈
import config
from collectors.arxiv_collector import collect_papers
from collectors.blog_collector import collect_blogs
from ranker import rank_papers, rank_blogs
from summarizer import batch_summarize_papers, batch_summarize_blogs, analyze_trends
from newsletter import render_newsletter, save_newsletter

load_dotenv()
console = Console()


# ── 파이프라인 단계별 함수 ────────────────────────────────────────────────────

def step_collect(days_back: int):
    """Step 1: arXiv + 블로그 수집"""
    console.print(Rule("[bold blue]Step 1: 데이터 수집[/]"))
    config.ARXIV_DAYS_BACK = days_back
    config.BLOG_DAYS_BACK = days_back

    papers = collect_papers()
    blogs = collect_blogs()
    return papers, blogs


def step_rank(papers, blogs, threshold: float):
    """Step 2: 시맨틱 유사도 기반 필터링 & 랭킹"""
    console.print(Rule("[bold blue]Step 2: 관련성 랭킹[/]"))
    config.RELEVANCE_THRESHOLD = threshold

    top_papers = rank_papers(papers)
    top_blogs = rank_blogs(blogs)
    return top_papers, top_blogs


def step_summarize(top_papers, top_blogs, dry_run: bool):
    """Step 3: LLM 요약 (dry_run이면 스킵)"""
    console.print(Rule("[bold blue]Step 3: LLM 요약 생성[/]"))

    if dry_run:
        console.print("[yellow]⚡ dry-run 모드: LLM 호출 스킵[/]\n")
        for p in top_papers:
            p.summary = p.abstract[:200] + "..."
            p.key_contributions = ["(dry-run: LLM 요약 생략)"]
            p.relevance_reason = f"관련성 점수: {p.relevance_score:.3f}"
        for b in top_blogs:
            b.llm_summary = b.summary[:200] + "..."
            b.relevance_reason = f"관련성 점수: {b.relevance_score:.3f}"
        trends = {
            "executive_summary": "(dry-run 모드)",
            "emerging_trends": ["(dry-run: 트렌드 분석 생략)"],
            "team_recommendations": ["(dry-run: 액션 아이템 생략)"],
        }
    else:
        top_papers = batch_summarize_papers(top_papers)
        top_blogs = batch_summarize_blogs(top_blogs)
        trends = analyze_trends(top_papers, top_blogs)

    return top_papers, top_blogs, trends


def step_generate(top_papers, top_blogs, trends, days_back: int):
    """Step 4: 뉴스레터 렌더링 & 저장"""
    console.print(Rule("[bold blue]Step 4: 뉴스레터 생성[/]"))

    end = datetime.now()
    start = end - timedelta(days=days_back)
    date_range = f"{start.strftime('%Y-%m-%d')} ~ {end.strftime('%Y-%m-%d')}"

    markdown = render_newsletter(top_papers, top_blogs, trends, date_range)
    path = save_newsletter(markdown)
    return path, markdown


# ── 결과 출력 헬퍼 ────────────────────────────────────────────────────────────

def print_summary_table(top_papers, top_blogs):
    """선정된 논문/블로그 요약 테이블 출력"""
    console.print(Rule("[bold green]선정 결과[/]"))

    if top_papers:
        table = Table(title="📄 Top Papers", show_lines=True, expand=True)
        table.add_column("#", width=3)
        table.add_column("제목", ratio=5)
        table.add_column("저자", ratio=2)
        table.add_column("점수", width=7, justify="right")
        table.add_column("날짜", width=10)
        for i, p in enumerate(top_papers, 1):
            table.add_row(
                str(i),
                p.title[:70] + ("…" if len(p.title) > 70 else ""),
                p.author_str[:30],
                f"{p.relevance_score:.3f}",
                p.published_str,
            )
        console.print(table)

    if top_blogs:
        table = Table(title="🏭 Top Blogs", show_lines=True, expand=True)
        table.add_column("#", width=3)
        table.add_column("제목", ratio=5)
        table.add_column("출처", ratio=2)
        table.add_column("점수", width=7, justify="right")
        for i, b in enumerate(top_blogs, 1):
            table.add_row(
                str(i),
                b.title[:70] + ("…" if len(b.title) > 70 else ""),
                b.source,
                f"{b.relevance_score:.3f}",
            )
        console.print(table)


# ── CLI 진입점 ────────────────────────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        description="RecSys Research Agent — 주간 뉴스레터 자동 생성"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="LLM 호출 없이 수집+랭킹만 실행 (API 키 불필요)",
    )
    parser.add_argument(
        "--days", type=int, default=config.ARXIV_DAYS_BACK,
        help=f"수집 기간 (일, 기본값: {config.ARXIV_DAYS_BACK})",
    )
    parser.add_argument(
        "--threshold", type=float, default=config.RELEVANCE_THRESHOLD,
        help=f"관련성 점수 임계값 (기본값: {config.RELEVANCE_THRESHOLD})",
    )
    parser.add_argument(
        "--output-dir", type=str, default=config.OUTPUT_DIR,
        help=f"출력 디렉토리 (기본값: {config.OUTPUT_DIR})",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    config.OUTPUT_DIR = args.output_dir

    # API 키 체크 (dry-run이 아닌 경우)
    if not args.dry_run and not os.environ.get("ANTHROPIC_API_KEY"):
        console.print(
            "[red bold]오류:[/] ANTHROPIC_API_KEY 환경 변수가 없습니다.\n"
            ".env 파일을 생성하거나 --dry-run 옵션을 사용하세요."
        )
        sys.exit(1)

    console.print(Panel(
        "[bold]RecSys Research Agent[/]\n"
        f"기간: 최근 {args.days}일 | "
        f"임계값: {args.threshold} | "
        f"{'[yellow]dry-run 모드[/]' if args.dry_run else '[green]전체 파이프라인[/]'}",
        title="🤖 Agent 시작",
        border_style="blue",
    ))

    start_time = time.time()

    # ── 파이프라인 실행 ──────────────────────────────────────────────────────
    papers, blogs = step_collect(args.days)

    if not papers and not blogs:
        console.print("[yellow]수집된 데이터가 없습니다. 종료합니다.[/]")
        sys.exit(0)

    top_papers, top_blogs = step_rank(papers, blogs, args.threshold)

    if not top_papers and not top_blogs:
        console.print(
            f"[yellow]임계값({args.threshold}) 이상의 관련 항목이 없습니다. "
            f"--threshold 값을 낮춰보세요.[/]"
        )
        sys.exit(0)

    top_papers, top_blogs, trends = step_summarize(top_papers, top_blogs, args.dry_run)

    path, _ = step_generate(top_papers, top_blogs, trends, args.days)

    # ── 결과 요약 ────────────────────────────────────────────────────────────
    print_summary_table(top_papers, top_blogs)

    elapsed = time.time() - start_time
    console.print(Panel(
        f"[green]✅ 완료[/]\n"
        f"논문 수집: {len(papers)}편 → 선정: {len(top_papers)}편\n"
        f"블로그 수집: {len(blogs)}편 → 선정: {len(top_blogs)}편\n"
        f"뉴스레터: {path}\n"
        f"소요 시간: {elapsed:.1f}초",
        title="🎉 Agent 완료",
        border_style="green",
    ))


if __name__ == "__main__":
    main()
