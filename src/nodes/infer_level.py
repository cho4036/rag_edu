"""4. InferLevel 노드 - 숙련도 추정"""
from typing import Dict, Any
from ..state import GraphState, Mastery


def infer_level_node(state: GraphState) -> Dict[str, Any]:
    """
    concept 단위 P(mastery) 초기화/업데이트
    
    입력: signals, user.prefs, 콜드스타트 응답
    출력: mastery 초기 분포, memory.seen_terms 갱신
    """
    print("📊 [InferLevel] 숙련도 추정 중...")
    
    signals = state["signals"]
    user = state["user"]
    domain_pack = state["domain_pack"]
    mastery = state["mastery"]
    memory = state["memory"]
    
    # 경험 수준에 따른 기본 mastery
    experience_level = user.prefs.get("experience_level", 1)
    base_mastery = {
        0: 0.2,  # 초보
        1: 0.4,  # 입문
        2: 0.6,  # 중급
        3: 0.8   # 고급
    }.get(experience_level, 0.4)
    
    # taxonomy의 모든 개념에 대해 초기 mastery 설정
    levels = {}
    if domain_pack:
        taxonomy = domain_pack.taxonomy if hasattr(domain_pack, 'taxonomy') else []
        for concept in taxonomy:
            concept_id = concept["id"]
            
            # 신호 기반 보정
            boost = 0.0
            for term in signals.terms:
                if term.lower() in concept["concepts"]:
                    boost += 0.15
            
            for skill in signals.skills:
                if skill in concept["concepts"]:
                    boost += 0.1
            
            # mastery 계산 (0.0 ~ 1.0 범위)
            mastery_value = min(1.0, base_mastery + boost)
            levels[concept_id] = mastery_value
    
    mastery.levels = levels
    
    # 약한 영역 식별
    weak_concepts = [cid for cid, score in levels.items() if score < 0.5]
    needs_diagnostic = len(weak_concepts) >= 3
    
    # 본 용어 기록
    memory.seen_terms.extend(signals.terms)
    memory.seen_terms = list(set(memory.seen_terms))  # 중복 제거
    
    print(f"✅ [InferLevel] 추정 완료: 평균 숙련도 {sum(levels.values())/len(levels):.2f}, 약한 영역 {len(weak_concepts)}개")
    
    return {
        "mastery": mastery,
        "memory": memory,
        "needs_diagnostic": needs_diagnostic,
        "current_step": "infer_level"
    }

