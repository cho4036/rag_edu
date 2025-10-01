"""10. GapMining 노드 - 지식 갭/모르는 용어 추천"""
from typing import Dict, Any, List
from ..state import GraphState, Gaps


def gap_mining_node(state: GraphState) -> Dict[str, Any]:
    """
    UnknownScore로 Top-N 용어/개념 추천
    
    입력: signals, mastery, taxonomy_map
    출력: gaps.unknown_terms_ranked, gaps.prereq_recos
    """
    print("🔎 [GapMining] 지식 갭 분석 중...")
    
    signals = state["signals"]
    mastery = state["mastery"]
    taxonomy_map = state["taxonomy_map"][0] if state["taxonomy_map"] else {}
    domain_pack = state["domain_pack"]
    memory = state["memory"]
    
    if not domain_pack:
        return {"gaps": Gaps(), "current_step": "gap_mining"}
    
    # UnknownScore = 빈도 × 중요도 × (1 - P_mastery) × 참신성
    unknown_terms = []
    
    core_concepts = taxonomy_map.get("core_concepts", [])
    
    for concept_data in core_concepts:
        concept_id = concept_data["concept_id"]
        mastery_score = concept_data.get("mastery_score", 0.5)
        importance = concept_data.get("importance", 5)
        
        # 참신성: 처음 보는 개념일수록 높음
        novelty = 1.0 if concept_id not in memory.seen_terms else 0.5
        
        # 빈도: taxonomy_map의 relevance 활용
        frequency = concept_data.get("relevance", 0.5)
        
        # Unknown Score 계산
        unknown_score = frequency * (importance / 10) * (1 - mastery_score) * novelty
        
        # 개념 정보 가져오기
        taxonomy = domain_pack.taxonomy if hasattr(domain_pack, 'taxonomy') else []
        concept_info = next(
            (c for c in taxonomy if c["id"] == concept_id),
            None
        )
        
        if concept_info and unknown_score > 0.1:
            # 관련 용어 정의
            related_terms = []
            glossary = domain_pack.glossary if hasattr(domain_pack, 'glossary') else {}
            for concept_name in concept_info["concepts"]:
                if concept_name in glossary:
                    related_terms.append({
                        "term": concept_name,
                        "definition": glossary[concept_name][:100] + "..."
                    })
            
            unknown_terms.append({
                "concept_id": concept_id,
                "name": concept_info["name"],
                "unknown_score": unknown_score,
                "mastery_score": mastery_score,
                "importance": importance,
                "related_terms": related_terms[:3],  # 상위 3개만
                "prerequisites": concept_info["prerequisites"]
            })
    
    # Unknown Score로 정렬
    unknown_terms.sort(key=lambda x: x["unknown_score"], reverse=True)
    
    # Top-5 추출
    top_unknown = unknown_terms[:5]
    
    # 선수지식 추천
    prereq_recos = []
    for term in top_unknown:
        if term["mastery_score"] < 0.4 and term["prerequisites"]:
            for prereq_id in term["prerequisites"]:
                prereq_concept = next(
                    (c for c in taxonomy if c["id"] == prereq_id),
                    None
                )
                if prereq_concept:
                    prereq_recos.append(
                        f"{prereq_concept['name']} (→ {term['name']}을 위한 선수지식)"
                    )
    
    gaps = Gaps(
        unknown_terms_ranked=top_unknown,
        prereq_recos=list(set(prereq_recos))[:3]  # 중복 제거, 상위 3개
    )
    
    print(f"✅ [GapMining] 갭 분석 완료: {len(top_unknown)}개 미지 용어, {len(prereq_recos)}개 선수지식 추천")
    
    return {
        "gaps": gaps,
        "current_step": "gap_mining"
    }

