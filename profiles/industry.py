"""
Industry 프로필
데이터 과학 · 데이터 분석 · 데이터 엔지니어링 · 추천시스템 · 에이전트 실무
"""

PROFILE_NAME = "Industry Practice"
PROFILE_DESCRIPTION = "데이터 과학 · 데이터 분석 · 데이터 엔지니어링 · 추천시스템 · AI 에이전트 실무"

# ── 실무 주제 (시맨틱 유사도 필터링 기준) ────────────────────────────────────────
TEAM_RESEARCH_TOPICS = [
    # ── 데이터 과학 / 데이터 분석 ─────────────────────────────────────────────
    "A/B testing and causal inference for product experimentation",
    "Feature engineering and feature store for production ML pipelines",
    "Time series forecasting with deep learning for business metrics",
    "Anomaly detection and outlier analysis in large-scale data",
    "Explainable AI and model interpretability for business decisions",
    "AutoML and hyperparameter optimization for production models",
    "Natural language processing for text analytics and sentiment analysis",
    # ── 데이터 엔지니어링 ─────────────────────────────────────────────────────
    "Real-time data pipeline architecture with streaming processing",
    "Data lakehouse architecture and modern data stack",
    "ETL/ELT pipeline optimization and orchestration with Airflow or Dagster",
    "Data quality monitoring and observability in production",
    "Distributed computing with Spark and large-scale data processing",
    "Vector database and embedding storage for ML applications",
    "MLOps and ML platform engineering for model serving",
    # ── 추천시스템 ────────────────────────────────────────────────────────────
    "Recommendation system with deep learning and neural collaborative filtering",
    "Two-tower model and retrieval-ranking architecture for recommendations",
    "Graph neural networks for social and e-commerce recommendation",
    "Multi-task learning and multi-objective optimization in recommender systems",
    "Sequential recommendation with transformer-based models",
    "Cold-start problem and exploration-exploitation in recommendations",
    "Real-time personalization and online learning for recommendation",
    # ── AI 에이전트 실무 ──────────────────────────────────────────────────────
    "LLM-based autonomous agents with tool use and function calling",
    "Retrieval augmented generation RAG for enterprise applications",
    "Multi-agent systems and agent orchestration frameworks",
    "LLM evaluation and benchmarking for production deployment",
    "Prompt engineering and chain-of-thought reasoning in practice",
    "AI agent workflow automation and human-in-the-loop systems",
    "Fine-tuning and RLHF for domain-specific language models",
]

# ── arXiv 검색 쿼리 ──────────────────────────────────────────────────────────────
ARXIV_QUERIES = [
    # 데이터 과학 / 분석
    "A/B testing causal inference experimentation",
    "feature engineering production machine learning",
    "time series forecasting deep learning",
    "anomaly detection large-scale data",
    "explainable AI interpretability",
    # 데이터 엔지니어링
    "real-time data pipeline streaming architecture",
    "data lakehouse modern data stack",
    "MLOps model serving production",
    "vector database embedding retrieval",
    # 추천시스템
    "recommendation system deep learning collaborative filtering",
    "two-tower retrieval ranking recommendation",
    "graph neural network recommendation",
    "sequential recommendation transformer",
    "multi-task learning recommender system",
    "cold-start exploration exploitation recommendation",
    # AI 에이전트
    "LLM autonomous agent tool use",
    "retrieval augmented generation RAG",
    "multi-agent system orchestration",
    "LLM evaluation benchmark production",
    "AI agent workflow automation",
]

ARXIV_CATEGORIES = [
    "cs.LG",    # Machine Learning
    "cs.IR",    # Information Retrieval
    "cs.AI",    # Artificial Intelligence
    "cs.CL",    # Computation and Language
    "cs.DB",    # Databases
    "cs.DC",    # Distributed Computing
    "cs.SE",    # Software Engineering
    "stat.ML",  # Statistics - Machine Learning
]
ARXIV_MAX_RESULTS = 15
ARXIV_DAYS_BACK = 7

# ── 기술 블로그 RSS 피드 ──────────────────────────────────────────────────────────
BLOG_FEEDS = [
    {
        "name": "Netflix Tech Blog",
        "url": "https://netflixtechblog.com/feed",
        "tags": ["recommendation", "data pipeline", "A/B testing", "personalization"],
    },
    {
        "name": "Uber Engineering",
        "url": "https://www.uber.com/blog/engineering/rss/",
        "tags": ["data platform", "real-time", "ML platform", "recommendation"],
    },
    {
        "name": "Airbnb Tech Blog",
        "url": "https://medium.com/feed/airbnb-engineering",
        "tags": ["data science", "experimentation", "recommendation", "search"],
    },
    {
        "name": "Spotify Engineering",
        "url": "https://engineering.atspotify.com/feed/",
        "tags": ["recommendation", "personalization", "data pipeline", "ML"],
    },
    {
        "name": "Towards Data Science",
        "url": "https://towardsdatascience.com/feed",
        "tags": ["data science", "machine learning", "recommendation", "agent"],
    },
    {
        "name": "Google AI Blog",
        "url": "https://blog.research.google/feeds/posts/default?alt=rss",
        "tags": ["recommendation", "LLM", "agent", "data"],
    },
    {
        "name": "OpenAI Blog",
        "url": "https://openai.com/blog/rss.xml",
        "tags": ["LLM", "agent", "tool use", "RAG"],
    },
    {
        "name": "LangChain Blog",
        "url": "https://blog.langchain.dev/rss/",
        "tags": ["agent", "RAG", "LLM", "orchestration", "tool use"],
    },
    {
        "name": "Lil'Log (Lilian Weng)",
        "url": "https://lilianweng.github.io/index.xml",
        "tags": ["agent", "LLM", "recommendation", "generative"],
    },
]

BLOG_DAYS_BACK = 7
BLOG_KEYWORDS = [
    # 데이터 과학 / 분석
    "A/B testing", "causal inference", "feature engineering", "feature store",
    "time series", "anomaly detection", "explainability", "interpretability",
    # 데이터 엔지니어링
    "data pipeline", "data lakehouse", "ETL", "data quality", "observability",
    "Spark", "Airflow", "Dagster", "vector database", "MLOps",
    # 추천시스템
    "recommendation", "collaborative filtering", "two-tower", "retrieval",
    "ranking", "personalization", "cold-start", "sequential recommendation",
    # AI 에이전트
    "LLM agent", "tool use", "function calling", "RAG",
    "retrieval augmented", "multi-agent", "agent orchestration",
    "prompt engineering", "chain-of-thought", "fine-tuning", "RLHF",
]

# ── 임베딩 & 시맨틱 유사도 ────────────────────────────────────────────────────────
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
RELEVANCE_THRESHOLD = 0.35
TOP_N_PAPERS = 10
TOP_N_BLOGS = 5

# ── LLM 설정 ──────────────────────────────────────────────────────────────────────
LLM_MODEL = "claude-opus-4-6"
LLM_MAX_TOKENS = 1024
SUMMARY_MAX_TOKENS = 512

# ── 출력 설정 ──────────────────────────────────────────────────────────────────────
OUTPUT_DIR = "./output"
NEWSLETTER_FILENAME = "industry_digest_{date}.md"
