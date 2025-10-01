"""0. DomainDetect 노드 - 사용자 질문에서 분야 자동 감지"""
from typing import Dict, Any


def domain_detect_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    사용자 질문을 분석하여 어떤 분야인지 자동 감지
    
    입력: user_message
    출력: detected_domain (분야명)
    """
    print("🔎 [DomainDetect] 분야 감지 중...")
    
    user_message = state["user_message"].lower()
    
    # 분야별 키워드 패턴 (확장 가능)
    domain_patterns = {
        "RAG": [
            "rag", "retrieval", "augmented", "generation", 
            "벡터", "임베딩", "검색", "생성", "llm", "랭체인",
            "pinecone", "weaviate", "chroma", "qdrant"
        ],
        "Machine Learning": [
            "머신러닝", "딥러닝", "학습", "모델", "훈련", "추론",
            "tensorflow", "pytorch", "keras", "scikit", "신경망",
            "cnn", "rnn", "transformer", "accuracy", "loss"
        ],
        "Backend Development": [
            "백엔드", "서버", "api", "rest", "graphql", "데이터베이스",
            "django", "flask", "fastapi", "express", "spring",
            "postgresql", "mongodb", "redis", "kafka"
        ],
        "Frontend Development": [
            "프론트엔드", "웹", "react", "vue", "angular", "ui", "ux",
            "javascript", "typescript", "css", "html", "component",
            "next.js", "nuxt", "svelte"
        ],
        "DevOps": [
            "데브옵스", "배포", "ci/cd", "docker", "kubernetes", "k8s",
            "jenkins", "github actions", "terraform", "ansible",
            "모니터링", "로깅", "prometheus", "grafana"
        ],
        "Data Science": [
            "데이터 과학", "분석", "시각화", "통계", "pandas", "numpy",
            "matplotlib", "seaborn", "jupyter", "분포", "상관관계",
            "회귀", "분류", "군집"
        ],
        "Blockchain": [
            "블록체인", "암호화폐", "스마트 컨트랙트", "이더리움",
            "solidity", "web3", "nft", "defi", "dapp", "합의"
        ],
        "Cloud Computing": [
            "클라우드", "aws", "azure", "gcp", "람다", "s3", "ec2",
            "serverless", "cloud", "iaas", "paas", "saas"
        ],
        "Cybersecurity": [
            "보안", "해킹", "취약점", "암호화", "인증", "방화벽",
            "penetration", "vulnerability", "encryption", "ssl", "tls"
        ],
        "Mobile Development": [
            "모바일", "앱", "android", "ios", "swift", "kotlin",
            "react native", "flutter", "xamarin", "cross-platform"
        ]
    }
    
    # 점수 기반 분야 감지
    domain_scores = {}
    
    for domain, keywords in domain_patterns.items():
        score = sum(1 for kw in keywords if kw in user_message)
        if score > 0:
            domain_scores[domain] = score
    
    # 가장 높은 점수의 분야 선택
    detected_domain = "General"  # 기본값
    confidence = 0.0
    
    if domain_scores:
        detected_domain = max(domain_scores, key=domain_scores.get)
        max_score = domain_scores[detected_domain]
        total_keywords = len(domain_patterns[detected_domain])
        confidence = min(0.95, max_score / total_keywords * 2)  # 정규화
    
    # 일반 학습 키워드 체크
    general_keywords = ["배우", "학습", "공부", "시작", "입문", "알려줘", "설명"]
    if any(kw in user_message for kw in general_keywords) and confidence < 0.3:
        # 일반적인 질문이지만 분야가 명확하지 않음
        # 첫 명사/주요 개념을 분야로 추출 시도
        detected_domain = "General Knowledge"
    
    print(f"✅ [DomainDetect] 감지된 분야: {detected_domain} (신뢰도: {confidence:.2f})")
    
    return {
        "detected_domain": detected_domain,
        "domain_confidence": confidence,
        "current_step": "domain_detect"
    }

