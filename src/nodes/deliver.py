"""14. Deliver 노드 - 응답 출력"""
from typing import Dict, Any
from ..state import GraphState


def deliver_node(state: GraphState) -> Dict[str, Any]:
    """
    사용자에게 최종 결과 제공
    
    입력: answer, eval
    출력: 메시지 (섹션/체크리스트/다음 액션)
    """
    print("📤 [Deliver] 최종 응답 전달 중...")
    
    final_response = state["final_response"]
    eval_obj = state["eval"]
    
    # 신뢰도 및 리스크 정보 추가
    footer = "\n\n---\n\n"
    footer += f"**신뢰도:** {eval_obj.confidence:.0%}\n\n"
    
    if eval_obj.risks:
        footer += "**⚠️ 주의사항:**\n"
        for risk in eval_obj.risks:
            footer += f"- {risk}\n"
        footer += "\n"
    
    # 인터랙티브 옵션 제안
    footer += "**💡 다음으로 할 수 있는 것:**\n"
    footer += "- 더 구체적인 질문하기\n"
    footer += "- 특정 개념에 대해 깊이 파고들기\n"
    footer += "- 코드 예제 요청하기\n"
    footer += "- 미니퀴즈로 이해도 확인하기\n"
    
    complete_response = final_response + footer
    
    # 채팅 히스토리에 추가
    chat_history = [
        {"role": "user", "content": state["user_message"]},
        {"role": "assistant", "content": complete_response}
    ]
    
    print("✅ [Deliver] 전달 완료!")
    print("=" * 50)
    
    return {
        "final_response": complete_response,
        "chat_history": chat_history,
        "current_step": "deliver"
    }

