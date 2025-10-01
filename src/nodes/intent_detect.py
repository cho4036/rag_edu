"""6. IntentDetect 노드 - 의도/태스크 분류"""
from typing import Dict, Any
from ..state import GraphState, Intent


def intent_detect_node(state: GraphState) -> Dict[str, Any]:
    """
    질문 성격 파악 (설계/디버깅/비교/최적화/코드생성/평가 등)
    
    입력: 사용자 질문 + signals
    출력: intent
    """
    print("🎯 [IntentDetect] 의도 분석 중...")
    
    user_message = state["user_message"].lower()
    
    # 의도 패턴 매칭
    intent_patterns = {
        "design": ["설계", "아키텍처", "구조", "어떻게 구성", "선택", "architecture", "design"],
        "implementation": ["구현", "코드", "만들", "작성", "개발", "implement", "code"],
        "evaluation": ["평가", "측정", "비교", "테스트", "ragas", "evaluate", "measure"],
        "optimization": ["최적화", "성능", "빠르", "지연", "비용", "optimize", "performance"],
        "troubleshoot": ["문제", "오류", "에러", "디버그", "안돼", "error", "debug", "fix"],
        "compare": ["차이", "vs", "비교", "어느게", "compare", "difference"],
        "explain": ["설명", "무엇", "뭐", "이란", "개념", "explain", "what is"],
        "learn_path": ["배우", "학습", "공부", "시작", "learn", "study", "tutorial"]
    }
    
    detected_type = "explain"  # 기본값
    max_score = 0
    
    for intent_type, keywords in intent_patterns.items():
        score = sum(1 for kw in keywords if kw in user_message)
        if score > max_score:
            max_score = score
            detected_type = intent_type
    
    # 신뢰도 계산
    confidence = min(0.9, 0.3 + max_score * 0.2)
    
    # 서브타입 추론
    sub_type = ""
    if detected_type == "design":
        if "인덱싱" in user_message or "indexing" in user_message:
            sub_type = "indexing_design"
        elif "검색" in user_message or "retrieval" in user_message:
            sub_type = "retrieval_design"
    
    intent = Intent(
        type=detected_type,
        sub_type=sub_type,
        confidence=confidence
    )
    
    # 필수 산출물 템플릿 지정
    required_outputs = []
    if detected_type == "design":
        required_outputs = ["architecture_diagram", "component_list", "tradeoffs"]
    elif detected_type == "implementation":
        required_outputs = ["code_snippets", "setup_guide"]
    elif detected_type == "evaluation":
        required_outputs = ["metrics", "evaluation_plan"]
    
    task = state["task"]
    task.required_outputs = required_outputs
    
    print(f"✅ [IntentDetect] 의도: {detected_type} (신뢰도: {confidence:.2f})")
    
    return {
        "intent": intent,
        "task": task,
        "current_step": "intent_detect"
    }

