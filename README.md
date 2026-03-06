# 📚 PhD Research Digest Agent

**Geometric Deep Learning · Topological Data Analysis · Topological Signal Processing**

arXiv 최신 논문과 연구 블로그를 매일 자동 수집·요약하고,
개인 연구 주제와의 시맨틱 유사도를 기반으로 필터링하여
**Discord로 일일 뉴스레터를 자동 발송**하는 Research Agent입니다.

---

## 아키텍처

```
                        GitHub Actions (매일 09:00 KST)
                                     │
          ┌──────────┐   ┌──────────┐│┌──────────┐   ┌──────────┐
          │ Collect  │ → │  Rank    │││ Summarize│ → │ Generate │
          │          │   │          │││          │   │          │
          │ arXiv    │   │sentence- │││ Claude   │   │ Jinja2   │
          │ RSS Feed │   │transform │││ tool_use │   │ Markdown │
          └──────────┘   └──────────┘│└──────────┘   └──────────┘
               │               │     │      │               │
            수집            필터링·랭킹   LLM 요약      뉴스레터 생성
                                     │               │
                              Git commit & push   Discord Embed
```

### 기술 스택

| 컴포넌트 | 기술 | 역할 |
|---|---|---|
| 수집 | `feedparser`, `requests`, `BeautifulSoup` | arXiv Atom API + RSS 파싱 |
| 랭킹 | `sentence-transformers` (all-MiniLM-L6-v2) | 연구 주제 시맨틱 유사도 |
| 요약 | `anthropic` Claude (`tool_use`) | 구조화된 JSON 요약 강제 |
| 출력 | `jinja2`, `rich` | Markdown 렌더링 + CLI UI |
| 자동화 | GitHub Actions | 일별 스케줄 실행 + 알림 |
| 알림 | Discord Webhook | Embed 카드 형식 전송 |

---

## 연구 주제 (필터링 기준)

`config.py`의 `TEAM_RESEARCH_TOPICS`가 시맨틱 유사도 계산의 기준 벡터로 사용됩니다.

### Geometric Deep Learning (GDL)
- Equivariant neural networks with symmetry group representations
- SE(3) / E(3) equivariant networks for 3D geometric data
- Message passing neural networks on graphs and manifolds
- Gauge equivariant convolutional networks on manifolds

### Topological Data Analysis (TDA)
- Persistent homology and persistence diagrams for data analysis
- Simplicial complexes and cell complexes in machine learning
- Sheaf theory and sheaf neural networks on graphs
- Mapper algorithm and topological descriptors

### Topological Signal Processing (TSP)
- Hodge Laplacian and Hodge decomposition for signal processing
- Signal processing on simplicial complexes and higher-order networks
- Simplicial neural networks for flow and edge signal learning
- Cell complex / combinatorial complex neural networks

### Cross-cutting
- Topological deep learning unifying GDL and TDA
- Diffusion processes on Riemannian manifolds
- Geometric and topological methods for graph representation learning

---

## 파일 구조

```
hands_on_agent_research/
├── agent.py                         # 메인 오케스트레이터 (4-step 파이프라인)
├── config.py                        # 연구 주제·쿼리·피드 설정
├── models.py                        # Paper, BlogPost, Newsletter 데이터클래스
├── ranker.py                        # 시맨틱 유사도 필터링 & 랭킹
├── summarizer.py                    # Claude tool_use 기반 LLM 요약
├── newsletter.py                    # Jinja2 Markdown 뉴스레터 렌더러
├── collectors/
│   ├── arxiv_collector.py           # arXiv Atom API 수집
│   └── blog_collector.py            # RSS 피드 + 크롤링
├── .github/
│   ├── workflows/
│   │   └── daily_digest.yml         # 일별 자동 실행 워크플로우
│   └── scripts/
│       └── notify_discord.py        # Discord Embed 알림 스크립트
├── output/                          # 생성된 뉴스레터 (gitignore 제외)
│   └── phd_digest_YYYYMMDD.md
├── requirements.txt
├── run.sh                           # 로컬 실행 편의 스크립트
└── .env.example                     # 환경 변수 템플릿
```

---

## 로컬 설치 및 실행

```bash
# 1. 가상환경 생성 (numpy<2 호환 필요)
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

# 2. 환경 변수 설정
cp .env.example .env
# .env 에 ANTHROPIC_API_KEY 입력

# 3-a. 전체 파이프라인 실행
./run.sh

# 3-b. LLM 호출 없이 수집·랭킹만 테스트 (API 키 불필요)
./run.sh --dry-run

# 3-c. 옵션 조정
./run.sh --days 14 --threshold 0.4 --output-dir ./reports
```

---

## GitHub Actions 자동화

### Secrets 설정

`Settings → Secrets and variables → Actions`에서 추가:

| Secret | 설명 |
|---|---|
| `ANTHROPIC_API_KEY` | Anthropic API 키 |
| `DISCORD_WEBHOOK_URL` | Discord 채널 웹훅 URL |

> Discord 웹훅: 채널 설정 → 연동 → 웹훅 → 새 웹훅 → URL 복사

### 실행 스케줄

| 방식 | 조건 |
|---|---|
| 자동 | 매일 **09:00 KST** (cron: `0 0 * * *`) |
| 수동 | Actions 탭 → `Daily PhD Research Digest` → `Run workflow` |

수동 실행 시 `days`(수집 기간)와 `threshold`(관련성 임계값)를 UI에서 직접 조정할 수 있습니다.

### 워크플로우 단계

```
1. Checkout + Python 3.11 설치
2. pip install 의존성
3. agent.py 실행 → phd_digest_YYYYMMDD.md 생성
4. output/ 변경사항 자동 커밋 & push
5. Discord Embed 전송 (Top Papers + Trends + 뉴스레터 링크)
   └─ 실패 시: Actions 로그 링크 포함 오류 알림 전송
```

---

## 커스터마이징

### 연구 주제 변경 (`config.py`)

```python
TEAM_RESEARCH_TOPICS = [
    "Equivariant neural networks with symmetry group representations",
    # 본인 연구 주제로 교체 — 임베딩 기준 벡터로 사용됨
]
```

### arXiv 검색 쿼리 추가 (`config.py`)

```python
ARXIV_QUERIES = [
    "persistent homology topological data analysis machine learning",
    "your custom query here",
]

ARXIV_CATEGORIES = [
    "cs.LG", "math.AT", "eess.SP",  # 필요 카테고리 추가
]
```

### 블로그 피드 추가 (`config.py`)

```python
BLOG_FEEDS = [
    {
        "name": "Your Blog",
        "url":  "https://your-blog.com/feed.rss",
        "tags": ["topology", "geometric"],
    },
]
```

---

## 학습 포인트

| # | 개념 | 구현 위치 |
|---|---|---|
| 1 | **Agent 오케스트레이션** — 순차 파이프라인 패턴 | `agent.py` |
| 2 | **LLM Tool Use** — JSON schema 강제 구조화 출력 | `summarizer.py` |
| 3 | **시맨틱 유사도 필터링** — 연구 주제 벡터 vs 논문 임베딩 | `ranker.py` |
| 4 | **외부 API 통합** — arXiv Atom feed, RSS 파싱 | `collectors/` |
| 5 | **GitHub Actions 자동화** — 스케줄·시크릿·아티팩트 커밋 | `.github/workflows/` |
| 6 | **Discord Webhook** — Embed 카드 포맷 알림 | `.github/scripts/` |
