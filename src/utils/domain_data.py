"""도메인 지식 데이터 - RAG 관련 taxonomy, glossary 등"""
from typing import Dict, List, Any


# RAG 도메인 Taxonomy (개념 계층 구조)
RAG_TAXONOMY = [
    {
        "id": "rag_basics",
        "name": "RAG 기초",
        "level": 0,
        "importance": 10,
        "prerequisites": [],
        "concepts": ["retrieval", "generation", "augmentation"]
    },
    {
        "id": "indexing",
        "name": "인덱싱",
        "level": 1,
        "importance": 9,
        "prerequisites": ["rag_basics"],
        "concepts": ["chunking", "embedding", "vector_db", "metadata"]
    },
    {
        "id": "chunking",
        "name": "청킹 전략",
        "level": 2,
        "importance": 8,
        "prerequisites": ["indexing"],
        "concepts": ["fixed_size", "semantic_chunking", "recursive_chunking"]
    },
    {
        "id": "embedding",
        "name": "임베딩 선택",
        "level": 2,
        "importance": 9,
        "prerequisites": ["indexing"],
        "concepts": ["dense_vectors", "sparse_vectors", "multilingual", "domain_specific"]
    },
    {
        "id": "retrieval",
        "name": "검색 전략",
        "level": 1,
        "importance": 10,
        "prerequisites": ["rag_basics", "indexing"],
        "concepts": ["similarity_search", "bm25", "hybrid_search", "mmr"]
    },
    {
        "id": "reranking",
        "name": "재랭킹",
        "level": 2,
        "importance": 7,
        "prerequisites": ["retrieval"],
        "concepts": ["cross_encoder", "llm_rerank", "relevance_scoring"]
    },
    {
        "id": "generation",
        "name": "생성 단계",
        "level": 1,
        "importance": 9,
        "prerequisites": ["rag_basics"],
        "concepts": ["prompting", "context_injection", "citation", "guardrails"]
    },
    {
        "id": "evaluation",
        "name": "평가",
        "level": 1,
        "importance": 8,
        "prerequisites": ["rag_basics"],
        "concepts": ["ragas", "faithfulness", "relevance", "answer_quality"]
    },
    {
        "id": "optimization",
        "name": "최적화",
        "level": 2,
        "importance": 7,
        "prerequisites": ["retrieval", "generation"],
        "concepts": ["latency", "cost", "caching", "batch_processing"]
    },
    {
        "id": "deployment",
        "name": "배포",
        "level": 2,
        "importance": 6,
        "prerequisites": ["optimization"],
        "concepts": ["kubernetes", "serverless", "monitoring", "autoscaling"]
    }
]


# RAG 용어 사전
RAG_GLOSSARY = {
    "RAG": "Retrieval-Augmented Generation. 외부 지식을 검색하여 LLM의 생성 품질을 향상시키는 기법",
    "Chunking": "문서를 작은 단위로 분할하는 과정. 검색 효율성과 컨텍스트 품질에 영향",
    "Embedding": "텍스트를 고차원 벡터로 변환하는 과정. 의미적 유사도 계산에 사용",
    "Vector DB": "벡터 임베딩을 저장하고 유사도 검색을 수행하는 데이터베이스 (예: Pinecone, Weaviate, Qdrant)",
    "BM25": "키워드 기반 검색 알고리즘. Sparse retrieval의 대표적 방법",
    "Hybrid Search": "Dense vector search와 sparse keyword search를 결합한 검색 방법",
    "Cross-encoder": "쿼리와 문서를 함께 입력받아 관련성을 직접 평가하는 재랭킹 모델",
    "RAGAS": "RAG 시스템을 평가하기 위한 프레임워크. Faithfulness, Answer Relevance 등 측정",
    "MMR": "Maximal Marginal Relevance. 다양성과 관련성을 동시에 고려하는 검색 알고리즘",
    "Semantic Chunking": "의미적 경계를 고려하여 문서를 분할하는 방법",
    "Dense Vectors": "의미 기반 임베딩. BERT, Sentence Transformers 등 사용",
    "Sparse Vectors": "키워드 기반 표현. TF-IDF, BM25 등",
    "Reranking": "초기 검색 결과를 더 정교한 모델로 재정렬하는 과정",
    "Context Injection": "검색된 문서를 프롬프트에 삽입하는 방법",
    "Guardrails": "LLM 출력의 안전성과 품질을 보장하는 메커니즘",
    "Faithfulness": "생성된 답변이 검색된 문서에 충실한 정도",
    "Answer Relevance": "생성된 답변이 질문과 얼마나 관련있는지",
    "vLLM": "고성능 LLM 추론 서버. PagedAttention 기법 사용",
    "TEI": "Text Embeddings Inference. HuggingFace의 임베딩 추론 서버",
    "Gateway API": "Kubernetes의 표준 Ingress 대체 API"
}


# 질문 은행 (진단용)
QUESTION_BANK = [
    {
        "id": "q1",
        "concept": "rag_basics",
        "difficulty": 1,
        "question": "RAG에서 'Retrieval' 단계의 주요 목적은 무엇인가요?",
        "options": [
            "외부 지식 소스에서 관련 정보를 찾는다",
            "LLM을 파인튜닝한다",
            "사용자 질문을 분류한다",
            "응답 품질을 평가한다"
        ],
        "correct": 0
    },
    {
        "id": "q2",
        "concept": "chunking",
        "difficulty": 2,
        "question": "Semantic Chunking의 장점은 무엇인가요?",
        "options": [
            "구현이 가장 간단하다",
            "의미적 경계를 고려하여 문맥을 보존한다",
            "항상 고정 크기 청크를 생성한다",
            "추가 모델이 필요없다"
        ],
        "correct": 1
    },
    {
        "id": "q3",
        "concept": "retrieval",
        "difficulty": 2,
        "question": "Hybrid Search가 효과적인 이유는?",
        "options": [
            "오직 키워드 매칭만 사용하기 때문",
            "오직 의미적 유사도만 사용하기 때문",
            "키워드 검색과 벡터 검색의 장점을 결합하기 때문",
            "가장 빠른 검색 방법이기 때문"
        ],
        "correct": 2
    },
    {
        "id": "q4",
        "concept": "reranking",
        "difficulty": 3,
        "question": "Cross-encoder를 사용한 재랭킹의 단점은?",
        "options": [
            "정확도가 낮다",
            "구현이 어렵다",
            "계산 비용이 높고 지연시간이 증가한다",
            "키워드 검색에만 적용 가능하다"
        ],
        "correct": 2
    },
    {
        "id": "q5",
        "concept": "evaluation",
        "difficulty": 2,
        "question": "RAGAS의 'Faithfulness' 지표는 무엇을 측정하나요?",
        "options": [
            "검색 속도",
            "생성된 답변이 검색된 문서에 근거하는지",
            "사용자 만족도",
            "시스템 비용"
        ],
        "correct": 1
    }
]


# 도구 레시피 (권장 구성)
TOOL_RECIPES = [
    {
        "name": "basic_rag",
        "level": "beginner",
        "components": {
            "chunking": "fixed_size (500 chars)",
            "embedding": "OpenAI text-embedding-3-small",
            "vector_db": "Chroma (로컬)",
            "retrieval": "similarity search (k=3)",
            "reranking": "없음",
            "llm": "GPT-3.5-turbo"
        },
        "pros": ["간단한 구현", "낮은 비용", "빠른 프로토타입"],
        "cons": ["제한적인 정확도", "한국어 최적화 부족"]
    },
    {
        "name": "production_rag",
        "level": "intermediate",
        "components": {
            "chunking": "semantic chunking",
            "embedding": "multilingual-e5-large",
            "vector_db": "Qdrant (클러스터)",
            "retrieval": "hybrid search (k=10)",
            "reranking": "cross-encoder (top-3)",
            "llm": "GPT-4"
        },
        "pros": ["높은 정확도", "다국어 지원", "확장 가능"],
        "cons": ["높은 비용", "복잡한 설정"]
    },
    {
        "name": "optimized_rag",
        "level": "advanced",
        "components": {
            "chunking": "adaptive semantic + hierarchical",
            "embedding": "domain-tuned model",
            "vector_db": "Pinecone (serverless)",
            "retrieval": "hybrid + MMR",
            "reranking": "LLM-based reranking",
            "llm": "vLLM (self-hosted)",
            "extras": ["caching", "query rewriting", "self-querying"]
        },
        "pros": ["최고 정확도", "최적화된 성능", "커스터마이징"],
        "cons": ["높은 복잡도", "운영 부담", "초기 투자 큼"]
    }
]


def get_domain_pack() -> Dict[str, Any]:
    """전체 도메인 팩 반환"""
    return {
        "taxonomy": RAG_TAXONOMY,
        "glossary": RAG_GLOSSARY,
        "question_bank": QUESTION_BANK,
        "tool_recipes": TOOL_RECIPES,
        "version": "1.0"
    }


def get_concept_by_id(concept_id: str) -> Dict[str, Any]:
    """ID로 개념 검색"""
    for concept in RAG_TAXONOMY:
        if concept["id"] == concept_id:
            return concept
    return {}


def get_prerequisites(concept_id: str) -> List[str]:
    """개념의 선수지식 반환"""
    concept = get_concept_by_id(concept_id)
    return concept.get("prerequisites", [])


def get_term_definition(term: str) -> str:
    """용어 정의 반환"""
    return RAG_GLOSSARY.get(term, "정의를 찾을 수 없습니다.")

