"""2. UserSignals 노드 - 대화 신호 추출"""
from typing import Dict, Any
import re
from ..state import GraphState, Signals


def user_signals_node(state: GraphState) -> Dict[str, Any]:
    """
    사용자의 관심/숙련 단서 추출
    
    입력: 사용자의 현재 메시지
    출력: signals.terms, signals.skills
    """
    print("🔍 [UserSignals] 사용자 신호 추출 중...")
    
    user_message = state["user_message"].lower()
    domain_pack = state["domain_pack"]
    
    # 용어 추출 - glossary와 매칭
    extracted_terms = []
    if domain_pack:
        # DomainPack 객체의 glossary 속성 접근
        glossary = domain_pack.glossary if hasattr(domain_pack, 'glossary') else {}
        for term in glossary.keys():
            if term.lower() in user_message:
                extracted_terms.append(term)
    
    # 기술 스택 감지
    tech_keywords = [
        "bm25", "hybrid", "vector", "embedding", "chunking",
        "rerank", "ragas", "llm", "gpt", "kubernetes", "k8s",
        "pinecone", "weaviate", "chroma", "qdrant",
        "vllm", "langchain", "llamaindex"
    ]
    
    extracted_skills = []
    for keyword in tech_keywords:
        if keyword in user_message:
            extracted_skills.append(keyword)
    
    # 코드/로그 패턴 감지
    code_fragments = re.findall(r'```[\s\S]*?```', state["user_message"])
    
    signals = Signals(
        terms=extracted_terms,
        skills=extracted_skills,
        code_fragments=code_fragments,
        logs=[]
    )
    
    # 신호가 충분한지 판단
    needs_coldstart = len(extracted_terms) == 0 and len(extracted_skills) == 0
    
    print(f"✅ [UserSignals] 추출 완료: {len(extracted_terms)}개 용어, {len(extracted_skills)}개 기술")
    
    return {
        "signals": signals,
        "needs_coldstart": needs_coldstart,
        "current_step": "user_signals"
    }

