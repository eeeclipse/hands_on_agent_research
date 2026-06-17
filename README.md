# Research Digest Agent

**프로필 기반 주간 리서치 다이제스트 자동화**

arXiv 최신 논문과 기술 블로그를 매주 자동 수집·요약하고,
시맨틱 유사도 기반으로 필터링하여 **Discord로 주간 뉴스레터를 자동 발송**하는 Research Agent입니다.

---

## 프로필

| 프로필 | 실행 커맨드 | 스케줄 | 주제 |
|---|---|---|---|
| **PhD Research** | `--profile phd` | 월요일 08:00 KST | GDL · TDA · TSP |
| **Industry Practice** | `--profile industry` | 월요일 09:00 KST | 데이터 실무 · 추천시스템 · AI 에이전트 |

### PhD Research (`profiles/phd_research.py`)
- Geometric Deep Learning (GDL)
- Topological Data Analysis (TDA)
- Topological Signal Processing (TSP)

### Industry Practice (`profiles/industry.py`)
- 데이터 과학 / 데이터 분석 (A/B testing, Feature Engineering, Anomaly Detection)
- 데이터 엔지니어링 (Data Pipeline, Lakehouse, MLOps)
- 추천시스템 (Two-tower, Sequential RecSys, Cold-start)
- AI 에이전트 실무 (LLM Agent, RAG, Multi-agent, Tool Use)

---

## 아키텍처

```
              GitHub Actions (매주 월요일 08:00 / 09:00 KST)
                               │
        ┌──────────┐   ┌──────────┐ ┌──────────┐   ┌──────────┐
        │ Collect  │ → │  Rank    │ │ Summarize│ → │ Generate │
        │          │   │          │ │          │   │          │
        │ arXiv    │   │sentence- │ │ Claude   │   │ Jinja2   │
        │ RSS Feed │   │transform │ │ tool_use │   │ Markdown │
        └──────────┘   └──────────┘ └──────────┘   └──────────┘
             │               │            │               │
          수집          필터링·랭킹     LLM 요약      뉴스레터 생성
                                                         │
                                Git commit & push   Discord Embed
```

### 기술 스택

| 컴포넌트 | 기술 | 역할 |
|---|---|---|
| 수집 | `feedparser`, `requests`, `BeautifulSoup` | arXiv Atom API + RSS 파싱 |
| 랭킹 | `sentence-transformers` (all-MiniLM-L6-v2) | 연구 주제 시맨틱 유사도 |
| 요약 | `anthropic` Claude (`tool_use`) | 구조화된 JSON 요약 강제 |
| 출력 | `jinja2`, `rich` | Markdown 렌더링 + CLI UI |
| 자동화 | GitHub Actions | 주간 스케줄 실행 + 알림 |
| 알림 | Discord Webhook | Embed 카드 형식 전송 |

---

## 파일 구조

```
hands_on_agent_research/
├── agent.py                         # 메인 오케스트레이터 (4-step 파이프라인)
├── config.py                        # 프로필 기반 동적 설정 로더
├── profiles/
│   ├── __init__.py                  # 프로필 로더
│   ├── phd_research.py              # PhD Research 프로필 (GDL/TDA/TSP)
│   └── industry.py                  # Industry Practice 프로필
├── models.py                        # Paper, BlogPost, Newsletter 데이터클래스
├── ranker.py                        # 시맨틱 유사도 필터링 & 랭킹
├── summarizer.py                    # Claude tool_use 기반 LLM 요약
├── newsletter.py                    # Jinja2 Markdown 뉴스레터 렌더러
├── collectors/
│   ├── arxiv_collector.py           # arXiv Atom API 수집
│   └── blog_collector.py            # RSS 피드 + 크롤링
├── .github/
│   ├── workflows/
│   │   ├── weekly_phd_digest.yml    # PhD 주간 다이제스트 (월 08:00 KST)
│   │   └── weekly_industry_digest.yml # Industry 주간 다이제스트 (월 09:00 KST)
│   └── scripts/
│       └── notify_discord.py        # Discord Embed 알림 스크립트
├── output/                          # 생성된 뉴스레터
│   ├── phd_digest_YYYYMMDD.md
│   └── industry_digest_YYYYMMDD.md
├── pyproject.toml                   # uv 프로젝트 설정 & 의존성
├── uv.lock                          # uv 락파일
├── run.sh                           # 로컬 실행 편의 스크립트
└── .env.example                     # 환경 변수 템플릿
```

---

## 로컬 설치 및 실행

```bash
# 1. 환경 변수 설정
cp .env.example .env
# .env 에 ANTHROPIC_API_KEY 입력

# 2. 프로필별 실행 (uv가 자동으로 의존성 설치)
uv run agent.py --profile phd              # PhD Research
uv run agent.py --profile industry         # Industry Practice

# 3. dry-run (LLM 호출 없이 수집·랭킹만 테스트)
uv run agent.py --profile industry --dry-run

# 4. 옵션 조정
uv run agent.py --profile phd --days 14 --threshold 0.4

# 또는 run.sh 사용
./run.sh --profile phd
```

---

## 테스트

```bash
uv run --group dev pytest -q
```

---

## GitHub Actions 자동화

### Secrets 설정

`Settings → Secrets and variables → Actions`에서 추가:

| Secret | 설명 |
|---|---|
| `ANTHROPIC_API_KEY` | Anthropic API 키 |
| `DISCORD_WEBHOOK_URL` | Discord 채널 웹훅 URL |

### 실행 스케줄

| 워크플로우 | 자동 스케줄 | 수동 실행 |
|---|---|---|
| PhD Research | 매주 **월요일 08:00 KST** | Actions → `Weekly PhD Research Digest` → Run workflow |
| Industry Practice | 매주 **월요일 09:00 KST** | Actions → `Weekly Industry Practice Digest` → Run workflow |

수동 실행 시 `days`(수집 기간)와 `threshold`(관련성 임계값)를 UI에서 직접 조정할 수 있습니다.

---

### 수집 품질 리포트

각 실행은 `output/quality_reports/{profile}_quality_YYYYMMDD.md`를 생성합니다.
리포트에는 arXiv 쿼리별 수집 수, 중복 제거 수, 기간 필터 탈락 수,
블로그 피드별 키워드 필터 탈락 수, 본문 크롤링 성공 수, 최종 선정 수가 포함됩니다.

---

## 커스터마이징

### 프로필 주제 변경

각 프로필 파일(`profiles/phd_research.py`, `profiles/industry.py`)에서 수정:

```python
TEAM_RESEARCH_TOPICS = [
    "Your research topic here",
    # 임베딩 기준 벡터로 사용됨
]

ARXIV_QUERIES = [
    "your custom arXiv search query",
]

BLOG_FEEDS = [
    {"name": "Your Blog", "url": "https://...", "tags": [...]},
]
```

### 새 프로필 추가

1. `profiles/new_profile.py` 생성 (기존 프로필 복사 후 수정)
2. `profiles/__init__.py`의 `AVAILABLE_PROFILES`와 `mapping`에 추가
3. `.github/workflows/`에 워크플로우 추가

---

## 학습 포인트

| # | 개념 | 구현 위치 |
|---|---|---|
| 1 | **Agent 오케스트레이션** — 순차 파이프라인 패턴 | `agent.py` |
| 2 | **LLM Tool Use** — JSON schema 강제 구조화 출력 | `summarizer.py` |
| 3 | **시맨틱 유사도 필터링** — 연구 주제 벡터 vs 논문 임베딩 | `ranker.py` |
| 4 | **프로필 기반 설정** — 동적 모듈 로딩 | `config.py`, `profiles/` |
| 5 | **외부 API 통합** — arXiv Atom feed, RSS 파싱 | `collectors/` |
| 6 | **GitHub Actions 자동화** — 주간 스케줄·시크릿·아티팩트 커밋 | `.github/workflows/` |
| 7 | **Discord Webhook** — Embed 카드 포맷 알림 | `.github/scripts/` |
