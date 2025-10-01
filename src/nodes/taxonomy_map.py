"""7. TaxonomyMap 노드 - 개념 매핑"""
from typing import Dict, Any, List
from ..state import GraphState


def taxonomy_map_node(state: GraphState) -> Dict[str, Any]:
    """
    질문을 taxonomy의 관련 노드들에 매핑
    
    입력: intent, signals
    출력: 관련 개념 리스트 (핵심/보조), 선후관계 (Prereq Chain)
    """
    print("🗺️ [TaxonomyMap] 개념 매핑 중...")
    
    signals = state["signals"]
    intent = state["intent"]
    domain_pack = state["domain_pack"]
    mastery = state["mastery"]
    
    if not domain_pack:
        return {"taxonomy_map": [], "current_step": "taxonomy_map"}
    
    # 신호와 매칭되는 개념 찾기
    related_concepts = []
    
    taxonomy = domain_pack.taxonomy if hasattr(domain_pack, 'taxonomy') else []
    for concept in taxonomy:
        relevance_score = 0.0
        
        # 용어 매칭
        for term in signals.terms:
            if term.lower() in [c.lower() for c in concept["concepts"]]:
                relevance_score += 0.3
        
        # 스킬 매칭
        for skill in signals.skills:
            if skill in concept["concepts"]:
                relevance_score += 0.2
        
        # 의도 기반 관련성
        if intent.type == "design" and "design" in concept["name"].lower():
            relevance_score += 0.2
        elif intent.type == "evaluation" and "평가" in concept["name"]:
            relevance_score += 0.3
        elif intent.type == "optimization" and "최적화" in concept["name"]:
            relevance_score += 0.3
        
        # 임베딩, 검색, 생성은 대부분의 RAG 질문에 관련
        if concept["id"] in ["embedding", "retrieval", "generation"]:
            relevance_score += 0.1
        
        if relevance_score > 0:
            related_concepts.append({
                "concept_id": concept["id"],
                "name": concept["name"],
                "relevance": min(1.0, relevance_score),
                "importance": concept["importance"],
                "level": concept["level"],
                "prerequisites": concept["prerequisites"],
                "mastery_score": mastery.levels.get(concept["id"], 0.5)
            })
    
    # 관련성 점수로 정렬
    related_concepts.sort(key=lambda x: x["relevance"] * x["importance"], reverse=True)
    
    # 선수지식 자동 확장 (부족한 mastery면 추가)
    prereq_chain = []
    for concept in related_concepts[:5]:  # 상위 5개만
        if concept["mastery_score"] < 0.5:
            for prereq_id in concept["prerequisites"]:
                if prereq_id not in [c["concept_id"] for c in prereq_chain]:
                    # 선수지식 개념 찾기
                    prereq_concept = next(
                        (c for c in taxonomy if c["id"] == prereq_id),
                        None
                    )
                    if prereq_concept:
                        prereq_chain.append({
                            "concept_id": prereq_id,
                            "name": prereq_concept["name"],
                            "reason": f"{concept['name']}의 선수지식"
                        })
    
    taxonomy_map = {
        "core_concepts": related_concepts[:5],
        "prerequisites": prereq_chain,
        "total_matched": len(related_concepts)
    }
    
    print(f"✅ [TaxonomyMap] 매핑 완료: {len(related_concepts)}개 개념, {len(prereq_chain)}개 선수지식")
    
    return {
        "taxonomy_map": [taxonomy_map],
        "current_step": "taxonomy_map"
    }

