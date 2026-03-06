"""
시맨틱 유사도 기반 랭킹 모듈
sentence-transformers + FAISS를 사용하여
팀 연구 주제와 논문/블로그의 코사인 유사도를 계산합니다.
"""

from typing import List, Tuple, Union
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from rich.console import Console

from models import Paper, BlogPost
import config

console = Console()

# 모델은 모듈 로드 시 한 번만 초기화
_model: SentenceTransformer = None


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        console.print(f"[dim]임베딩 모델 로드 중: {config.EMBEDDING_MODEL}[/]")
        _model = SentenceTransformer(config.EMBEDDING_MODEL)
    return _model


def _embed(texts: List[str]) -> np.ndarray:
    """텍스트 리스트 → 정규화된 임베딩 행렬 (N, D)"""
    model = _get_model()
    embeddings = model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
    return np.array(embeddings, dtype=np.float32)


def _topic_embeddings() -> np.ndarray:
    """팀 연구 주제 임베딩 (캐싱)"""
    if not hasattr(_topic_embeddings, "_cache"):
        _topic_embeddings._cache = _embed(config.TEAM_RESEARCH_TOPICS)
    return _topic_embeddings._cache


def score_paper(paper: Paper) -> float:
    """
    논문 제목 + 초록 → 팀 주제와의 최대 코사인 유사도 반환
    """
    text = f"{paper.title}. {paper.abstract}"
    doc_emb = _embed([text])                          # (1, D)
    topic_embs = _topic_embeddings()                  # (T, D)
    sims = cosine_similarity(doc_emb, topic_embs)     # (1, T)
    return float(sims.max())


def score_blog(post: BlogPost) -> float:
    """
    블로그 제목 + 요약/본문 → 팀 주제와의 최대 코사인 유사도 반환
    """
    body = post.content if post.content else post.summary
    text = f"{post.title}. {body[:1000]}"
    doc_emb = _embed([text])
    topic_embs = _topic_embeddings()
    sims = cosine_similarity(doc_emb, topic_embs)
    return float(sims.max())


def rank_papers(papers: List[Paper]) -> List[Paper]:
    """
    전체 논문에 점수를 매기고, 임계값 이상만 상위 TOP_N 반환
    """
    console.print(f"[bold cyan]🔍 논문 랭킹 시작[/] ({len(papers)}편)")

    for paper in papers:
        paper.relevance_score = score_paper(paper)

    filtered = [p for p in papers if p.relevance_score >= config.RELEVANCE_THRESHOLD]
    ranked = sorted(filtered, key=lambda p: p.relevance_score, reverse=True)
    top = ranked[: config.TOP_N_PAPERS]

    console.print(
        f"  임계값({config.RELEVANCE_THRESHOLD:.2f}) 이상: {len(filtered)}편 "
        f"→ 상위 {len(top)}편 선정\n"
    )
    return top


def rank_blogs(posts: List[BlogPost]) -> List[BlogPost]:
    """
    전체 블로그 포스트에 점수를 매기고, 임계값 이상만 상위 TOP_N 반환
    """
    console.print(f"[bold cyan]🔍 블로그 랭킹 시작[/] ({len(posts)}편)")

    for post in posts:
        post.relevance_score = score_blog(post)

    filtered = [p for p in posts if p.relevance_score >= config.RELEVANCE_THRESHOLD]
    ranked = sorted(filtered, key=lambda p: p.relevance_score, reverse=True)
    top = ranked[: config.TOP_N_BLOGS]

    console.print(
        f"  임계값({config.RELEVANCE_THRESHOLD:.2f}) 이상: {len(filtered)}편 "
        f"→ 상위 {len(top)}편 선정\n"
    )
    return top
