"""
Agent 설정 파일
박사 과정 진학을 위한 개인 연구 주제 추적:
  - Geometric Deep Learning (GDL)
  - Topological Data Analysis (TDA)
  - Topological Signal Processing (TSP)
"""

from dataclasses import dataclass, field
from typing import List

# ── 개인 연구 주제 (시맨틱 유사도 필터링 기준) ────────────────────────────────
# 세 축(GDL / TDA / TSP)을 고르게 커버하되, 교차 영역도 포함
TEAM_RESEARCH_TOPICS = [
    # ── Geometric Deep Learning ──────────────────────────────────────────────
    "Equivariant neural networks with symmetry group representations",
    "Message passing neural networks on graphs and manifolds",
    "SE(3) and E(3) equivariant networks for 3D geometric data",
    "Spectral and spatial graph convolutional networks",
    "Geometric priors and inductive biases in deep learning",
    "Point cloud learning with geometric deep learning",
    "Gauge equivariant convolutional networks on manifolds",
    # ── Topological Data Analysis ─────────────────────────────────────────────
    "Persistent homology and persistence diagrams for data analysis",
    "Simplicial complexes and cell complexes in machine learning",
    "Mapper algorithm and topological descriptors for high-dimensional data",
    "Topological data analysis for time series and multivariate signals",
    "Sheaf theory and sheaf neural networks on graphs",
    "Betti numbers and homological features for representation learning",
    "Vietoris-Rips and Čech complexes for shape analysis",
    # ── Topological Signal Processing ────────────────────────────────────────
    "Hodge Laplacian and Hodge decomposition for signal processing",
    "Signal processing on simplicial complexes and higher-order networks",
    "Topological filters and wavelets on cell complexes",
    "Simplicial neural networks for flow and edge signal learning",
    "Cell complex neural networks and combinatorial complex networks",
    "Higher-order interactions and hypergraph signal processing",
    # ── Cross-cutting / Emerging ──────────────────────────────────────────────
    "Topological deep learning unifying GDL and TDA",
    "Diffusion processes on Riemannian manifolds for generative models",
    "Geometric and topological methods for graph representation learning",
]

# ── arXiv 검색 쿼리 ────────────────────────────────────────────────────────────
# 각 축마다 핵심 쿼리 + 교차 주제 쿼리 구성
ARXIV_QUERIES = [
    # Geometric Deep Learning
    "equivariant neural network symmetry group",
    "geometric deep learning graph manifold",
    "SE3 E3 equivariant network 3D molecular",
    "message passing neural network graph",
    "gauge equivariant convolutional manifold",
    # Topological Data Analysis
    "persistent homology topological data analysis machine learning",
    "simplicial complex neural network topological",
    "topological data analysis deep learning",
    "sheaf neural network graph topology",
    "mapper algorithm topological descriptor",
    # Topological Signal Processing
    "Hodge Laplacian simplicial complex signal processing",
    "topological signal processing higher-order network",
    "simplicial neural network edge flow signal",
    "cell complex neural network combinatorial",
    "hypergraph neural network higher-order interaction",
    # Cross-cutting
    "topological deep learning",
    "geometric topological graph representation learning",
    "Riemannian manifold diffusion generative model",
]

ARXIV_CATEGORIES = [
    "cs.LG",    # Machine Learning
    "cs.CG",    # Computational Geometry
    "math.AT",  # Algebraic Topology
    "stat.ML",  # Statistics - Machine Learning
    "eess.SP",  # Signal Processing
    "cs.CV",    # Computer Vision (geometric aspects)
    "math.GR",  # Group Theory (equivariance)
    "cs.NE",    # Neural and Evolutionary Computing
]
ARXIV_MAX_RESULTS = 15          # 쿼리당 최대 수집 수
ARXIV_DAYS_BACK = 7             # 최근 N일 논문만 수집

# ── 기술 블로그 RSS 피드 ────────────────────────────────────────────────────────
BLOG_FEEDS = [
    {
        "name": "Google DeepMind Blog",
        "url": "https://deepmind.google/blog/rss.xml",
        "tags": ["geometric", "graph", "topology", "equivariant"],
    },
    {
        "name": "Distill.pub",
        "url": "https://distill.pub/rss.xml",
        "tags": ["geometric deep learning", "graph neural", "topology"],
    },
    {
        "name": "Towards Data Science",
        "url": "https://towardsdatascience.com/feed",
        "tags": ["topological", "geometric", "graph neural", "homology"],
    },
    {
        "name": "The Gradient",
        "url": "https://thegradient.pub/rss/",
        "tags": ["geometric", "equivariant", "topology", "manifold"],
    },
    {
        "name": "Lil'Log (Lilian Weng)",
        "url": "https://lilianweng.github.io/index.xml",
        "tags": ["graph neural", "geometric", "generative", "diffusion"],
    },
    {
        "name": "BAIR Blog",
        "url": "https://bair.berkeley.edu/blog/feed.xml",
        "tags": ["geometric deep learning", "graph", "topology"],
    },
    {
        "name": "Off the Convex Path",
        "url": "https://www.offconvex.org/feed.xml",
        "tags": ["geometric", "graph", "topology", "manifold"],
    },
]

BLOG_DAYS_BACK = 7              # 최근 N일 포스트만 수집
BLOG_KEYWORDS = [               # 블로그 관련성 사전 필터 키워드
    # GDL
    "geometric deep learning", "equivariant", "graph neural", "manifold",
    "SE(3)", "E(3)", "point cloud", "gauge", "symmetry",
    # TDA
    "topological data analysis", "persistent homology", "simplicial",
    "persistence diagram", "Betti", "Hodge", "sheaf", "mapper",
    # TSP
    "topological signal", "cell complex", "higher-order network",
    "hypergraph", "simplicial neural", "combinatorial complex",
    # General
    "topology", "algebraic topology", "Riemannian",
]

# ── 임베딩 & 시맨틱 유사도 ────────────────────────────────────────────────────
EMBEDDING_MODEL = "all-MiniLM-L6-v2"   # sentence-transformers 모델
RELEVANCE_THRESHOLD = 0.35              # 코사인 유사도 최소 임계값
TOP_N_PAPERS = 10
TOP_N_BLOGS = 5

# ── LLM 설정 (Anthropic) ──────────────────────────────────────────────────────
LLM_MODEL = "claude-opus-4-6"
LLM_MAX_TOKENS = 1024
SUMMARY_MAX_TOKENS = 512

# ── 출력 설정 ─────────────────────────────────────────────────────────────────
OUTPUT_DIR = "./output"
NEWSLETTER_FILENAME = "phd_digest_{date}.md"
