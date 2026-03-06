# 📚 RecSys Research Agent

추천 시스템(RecSys) 관련 최신 논문(arXiv)과 기술 블로그를 자동 수집·요약하고,
팀 연구 주제와의 관련성을 평가하여 **주간 뉴스레터를 자동 생성**하는 Agent입니다.

## 아키텍처

```
┌─────────────────────────────────────────────────────────────────┐
│                     RecSys Research Agent                        │
│                                                                   │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │  Collect │ →  │   Rank   │ →  │Summarize │ →  │Generate  │  │
│  │          │    │          │    │          │    │          │  │
│  │ arXiv    │    │sentence- │    │ Claude   │    │ Jinja2   │  │
│  │ RSS Feed │    │transforme│    │ tool_use │    │ Template │  │
│  │          │    │ + FAISS  │    │          │    │          │  │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘  │
│                                                                   │
│  Step 1          Step 2          Step 3          Step 4          │
│  수집            필터링·랭킹     LLM 요약         뉴스레터 생성   │
└─────────────────────────────────────────────────────────────────┘
```

### 핵심 기술 스택

| 컴포넌트 | 기술 | 역할 |
|----------|------|------|
| 수집 | `feedparser`, `requests`, `BeautifulSoup` | arXiv API + RSS 파싱 |
| 랭킹 | `sentence-transformers` (all-MiniLM-L6-v2) | 시맨틱 유사도 계산 |
| 요약 | `anthropic` (Claude, tool_use) | 구조화된 LLM 요약 |
| 출력 | `jinja2`, `rich` | Markdown 렌더링 + CLI UI |

## 설치

```bash
# 의존성 설치
pip install anthropic feedparser sentence-transformers faiss-cpu \
            scikit-learn python-dotenv rich jinja2 requests beautifulsoup4

# 환경 변수 설정
cp .env.example .env
# .env 파일에 ANTHROPIC_API_KEY 입력
```

## 사용법

```bash
# 전체 파이프라인 실행 (arXiv + 블로그 수집 → 랭킹 → LLM 요약 → 뉴스레터 생성)
python agent.py

# LLM 호출 없이 수집+랭킹만 확인 (API 키 불필요)
python agent.py --dry-run

# 최근 14일 논문, 관련성 임계값 0.4로 조정
python agent.py --days 14 --threshold 0.4

# 출력 디렉토리 지정
python agent.py --output-dir ./reports
```

## 파일 구조

```
hands_on_agent_research/
├── agent.py                    # 메인 오케스트레이션 (파이프라인 진입점)
├── config.py                   # 팀 연구 주제, 검색 쿼리, 블로그 피드 설정
├── models.py                   # Paper, BlogPost, Newsletter 데이터 모델
├── ranker.py                   # 시맨틱 유사도 기반 필터링 & 랭킹
├── summarizer.py               # Claude tool_use 기반 LLM 요약
├── newsletter.py               # Jinja2 기반 Markdown 뉴스레터 렌더링
├── collectors/
│   ├── arxiv_collector.py      # arXiv API 논문 수집
│   └── blog_collector.py       # RSS 피드 블로그 수집
├── output/                     # 생성된 뉴스레터 저장 (자동 생성)
│   └── newsletter_YYYYMMDD.md
└── .env                        # API 키 (git 제외)
```

## 커스터마이징

### 팀 연구 주제 변경 (`config.py`)

```python
TEAM_RESEARCH_TOPICS = [
    "Semantic ID representation for recommendation systems",
    "Causal inference for debiased recommendation",
    # 팀 주제에 맞게 추가/수정
]
```

### 블로그 피드 추가 (`config.py`)

```python
BLOG_FEEDS = [
    {
        "name": "Your Company Blog",
        "url": "https://your-blog.com/feed.rss",
        "tags": ["recommendation", "ML"],
    },
    # ...
]
```

### arXiv 검색 쿼리 조정 (`config.py`)

```python
ARXIV_QUERIES = [
    "recommendation system LLM large language model",
    "your custom query here",
]
```

## 학습 포인트

이 프로젝트는 다음 개념의 실습 예제입니다:

1. **Agent 오케스트레이션** — 순차적 파이프라인 패턴 (collect → rank → summarize → generate)
2. **LLM Tool Use** — Anthropic tool_use를 활용한 구조화된 출력 (JSON schema 강제)
3. **RAG 패턴** — 팀 연구 주제를 쿼리로 사용하는 시맨틱 유사도 필터링
4. **임베딩 기반 검색** — sentence-transformers + 코사인 유사도
5. **외부 API 통합** — arXiv Atom feed, RSS 피드 파싱
