"""13. MemoryWrite 노드 - 장기 개인화"""
from typing import Dict, Any
from ..state import GraphState


def memory_write_node(state: GraphState) -> Dict[str, Any]:
    """
    사용자 프로필/숙련도/용어 히스토리 기록
    
    입력: mastery, gaps, 상호작용 로그
    출력: 갱신된 memory
    """
    print("💾 [MemoryWrite] 메모리 저장 중...")
    
    memory = state["memory"]
    mastery = state["mastery"]
    gaps = state["gaps"]
    user_message = state["user_message"]
    final_response = state["final_response"]
    
    # 상호작용 로그 추가
    interaction_log = {
        "user_message": user_message[:100],  # 첫 100자만
        "intent": state["intent"].type,
        "concepts_covered": [c["name"] for c in state["taxonomy_map"][0].get("core_concepts", [])[:3]] if state["taxonomy_map"] else [],
        "confidence": state["eval"].confidence
    }
    
    memory.history.append(interaction_log)
    
    # mastery 스냅샷 (변화 추적용)
    # 실제 구현에서는 DB나 파일에 저장
    
    # seen_terms 업데이트 (이미 이전 노드에서 업데이트됨)
    for term_info in gaps.unknown_terms_ranked:
        if term_info["name"] not in memory.seen_terms:
            memory.seen_terms.append(term_info["name"])
    
    # 다음 세션용 콜드스타트 단축키 (캐싱)
    # 실제로는 user profile을 persistent storage에 저장
    
    print(f"✅ [MemoryWrite] 저장 완료: {len(memory.history)}개 인터랙션, {len(memory.seen_terms)}개 본 용어")
    
    return {
        "memory": memory,
        "current_step": "memory_write"
    }

