"""12. QualityGate 노드 - 품질/가드레일 검수"""
from typing import Dict, Any
from ..state import GraphState


def quality_gate_node(state: GraphState) -> Dict[str, Any]:
    """
    응답의 일관성/안전성/유용성 확인
    
    입력: answer, eval
    출력: 보정된 answer, 업데이트된 eval
    """
    print("✅ [QualityGate] 품질 검수 중...")
    
    answer = state["answer"]
    eval_obj = state["eval"]
    final_response = state["final_response"]
    
    # Self-consistency 체크 (간단한 버전)
    response_length = len(final_response)
    has_structure = "##" in final_response
    has_actionable = "다음 단계" in final_response or "액션" in final_response
    
    quality_score = 0.0
    
    if response_length > 500:
        quality_score += 0.3
    if has_structure:
        quality_score += 0.3
    if has_actionable:
        quality_score += 0.2
    if len(answer.content_blocks) >= 4:
        quality_score += 0.2
    
    # 반례 탐색 - 언제 이 답변이 실패할 수 있는가?
    failure_modes = []
    
    if "초보" in final_response and "고급" in final_response:
        failure_modes.append("경험 수준이 일관되지 않을 수 있음")
    
    if "비용" not in final_response and "cost" not in final_response.lower():
        failure_modes.append("비용 고려사항 누락 가능")
    
    if len(final_response) < 300:
        failure_modes.append("응답이 너무 짧아 실행 가능성 낮음")
    
    # eval 업데이트
    eval_obj.confidence = min(0.95, eval_obj.confidence * (0.5 + quality_score))
    
    if failure_modes:
        eval_obj.risks.extend(failure_modes[:2])  # 상위 2개만
    
    # 신뢰도가 낮으면 추가 액션 제안
    if eval_obj.confidence < 0.7:
        eval_obj.next_actions.append("더 구체적인 질문으로 다시 물어보기")
        eval_obj.next_actions.append("미니퀴즈로 개념 확인하기")
    
    # 중복/장황 제거 (실제로는 LLM으로 처리, 여기서는 간단히)
    # final_response는 이미 구조화되어 있어 그대로 사용
    
    print(f"✅ [QualityGate] 검수 완료: 품질 점수 {quality_score:.2f}, 신뢰도 {eval_obj.confidence:.2f}")
    
    return {
        "answer": answer,
        "eval": eval_obj,
        "final_response": final_response,
        "current_step": "quality_gate"
    }

