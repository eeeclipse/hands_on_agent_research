"""
Discord Webhook 알림 스크립트
생성된 뉴스레터 Markdown을 파싱해 Discord Embed 메시지를 전송합니다.

환경 변수:
  DISCORD_WEBHOOK_URL  Discord 채널 웹훅 URL
  NEWSLETTER_PATH      뉴스레터 Markdown 파일 경로
  GITHUB_SERVER_URL    GitHub 서버 URL (Actions 자동 주입)
  GITHUB_REPOSITORY    owner/repo (Actions 자동 주입)
  GITHUB_REF_NAME      브랜치명 (Actions 자동 주입)
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
import urllib.request
import urllib.error


# ── 환경 변수 ─────────────────────────────────────────────────────────────────
WEBHOOK_URL    = os.environ.get("DISCORD_WEBHOOK_URL", "")
NEWSLETTER_PATH = os.environ.get("NEWSLETTER_PATH", "")
GH_SERVER      = os.environ.get("GITHUB_SERVER_URL", "https://github.com")
GH_REPO        = os.environ.get("GITHUB_REPOSITORY", "")
GH_BRANCH      = os.environ.get("GITHUB_REF_NAME", "main")


# ── Markdown 파싱 ─────────────────────────────────────────────────────────────

def parse_newsletter(path: str) -> dict:
    """뉴스레터 Markdown에서 핵심 정보 추출"""
    text = Path(path).read_text(encoding="utf-8")

    # 날짜 범위
    date_range = ""
    m = re.search(r"RecSys Research Digest — (.+)", text)
    if m:
        date_range = m.group(1).strip()

    # Executive Summary (첫 단락)
    exec_summary = ""
    m = re.search(r"## 🧠 Executive Summary\n+(.+?)(?=\n---|\n##)", text, re.DOTALL)
    if m:
        exec_summary = m.group(1).strip()
        # dry-run 또는 너무 길면 자름
        if len(exec_summary) > 300:
            exec_summary = exec_summary[:300] + "…"

    # Top Papers (제목 + arXiv 링크 + 점수)
    papers = []
    for block in re.finditer(
        r"### \d+\. (.+?)\n.*?\*\*arXiv\*\* \| \[링크\]\(([^)]+)\).*?\*\*관련성 점수\*\* \| ([0-9.]+)",
        text, re.DOTALL
    ):
        papers.append({
            "title": block.group(1).strip(),
            "url":   block.group(2).strip(),
            "score": float(block.group(3)),
        })

    # Top Blogs
    blogs = []
    for block in re.finditer(
        r"### \d+\. \[(.+?)\]\(([^)]+)\)\n.*?\*\*관련성 점수\*\* \| ([0-9.]+)",
        text, re.DOTALL
    ):
        blogs.append({
            "title": block.group(1).strip(),
            "url":   block.group(2).strip(),
            "score": float(block.group(3)),
        })

    # Emerging Trends
    trends = re.findall(r"^- (.+)$", re.search(
        r"### Emerging Trends\n(.*?)(?=###|\Z)", text, re.DOTALL
    ).group(1) if re.search(r"### Emerging Trends", text) else "", re.MULTILINE)
    trends = [t for t in trends if "dry-run" not in t][:3]

    return {
        "date_range":     date_range,
        "exec_summary":   exec_summary,
        "papers":         papers,
        "blogs":          blogs,
        "trends":         trends,
    }


# ── Discord Embed 생성 ────────────────────────────────────────────────────────

def build_payload(data: dict, newsletter_url: str) -> dict:
    """Discord webhook payload (Embed) 생성"""

    # 논문 목록 (상위 5개)
    paper_lines = []
    for i, p in enumerate(data["papers"][:5], 1):
        paper_lines.append(f"`{p['score']:.3f}` [{p['title'][:60]}]({p['url']})")
    papers_value = "\n".join(paper_lines) if paper_lines else "_수집된 논문 없음_"

    # 블로그 목록
    blog_lines = []
    for b in data["blogs"][:3]:
        blog_lines.append(f"`{b['score']:.3f}` [{b['title'][:60]}]({b['url']})")
    blogs_value = "\n".join(blog_lines) if blog_lines else "_수집된 블로그 없음_"

    # 트렌드
    trends_value = "\n".join(f"• {t}" for t in data["trends"]) or "_분석 없음_"

    # Embed 색상: 보라 계열 (GDL/TDA/TSP 이미지)
    color = 0x7B68EE  # MediumSlateBlue

    embed = {
        "title": f"📚 PhD Research Digest — {data['date_range']}",
        "url":   newsletter_url,
        "color": color,
        "description": (
            data["exec_summary"]
            or "오늘의 GDL · TDA · TSP 연구 동향을 확인하세요."
        ),
        "fields": [
            {
                "name":   f"📄 Top Papers ({len(data['papers'])}편 선정)",
                "value":  papers_value,
                "inline": False,
            },
        ],
        "footer": {
            "text": f"RecSys Research Agent  •  {datetime.now().strftime('%Y-%m-%d %H:%M')} KST",
        },
    }

    if blog_lines:
        embed["fields"].append({
            "name":   f"🏭 Industry Blogs ({len(data['blogs'])}편)",
            "value":  blogs_value,
            "inline": False,
        })

    if data["trends"]:
        embed["fields"].append({
            "name":   "📈 Emerging Trends",
            "value":  trends_value,
            "inline": False,
        })

    embed["fields"].append({
        "name":   "🔗 전체 뉴스레터",
        "value":  f"[GitHub에서 보기]({newsletter_url})",
        "inline": False,
    })

    return {
        "username": "Research Digest Bot",
        "avatar_url": "https://arxiv.org/static/browse/0.3.4/images/arxiv-logo-fb.png",
        "embeds": [embed],
    }


# ── 전송 ──────────────────────────────────────────────────────────────────────

def send_webhook(webhook_url: str, payload: dict) -> None:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        webhook_url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"Discord 전송 성공: HTTP {resp.status}")
    except urllib.error.HTTPError as e:
        print(f"Discord 전송 실패: HTTP {e.code} — {e.read().decode()}", file=sys.stderr)
        sys.exit(1)


# ── 진입점 ────────────────────────────────────────────────────────────────────

def main():
    if not WEBHOOK_URL:
        print("DISCORD_WEBHOOK_URL 이 설정되지 않았습니다.", file=sys.stderr)
        sys.exit(1)
    if not NEWSLETTER_PATH or not Path(NEWSLETTER_PATH).exists():
        print(f"뉴스레터 파일을 찾을 수 없습니다: {NEWSLETTER_PATH}", file=sys.stderr)
        sys.exit(1)

    # GitHub 파일 링크 생성
    filename = Path(NEWSLETTER_PATH).name
    newsletter_url = f"{GH_SERVER}/{GH_REPO}/blob/{GH_BRANCH}/output/{filename}"

    print(f"뉴스레터 파싱: {NEWSLETTER_PATH}")
    data = parse_newsletter(NEWSLETTER_PATH)

    print(f"논문 {len(data['papers'])}편 / 블로그 {len(data['blogs'])}편 추출")
    payload = build_payload(data, newsletter_url)

    print(f"Discord 웹훅 전송 중...")
    send_webhook(WEBHOOK_URL, payload)


if __name__ == "__main__":
    main()
