"""5. AdaptiveDiagnostic 노드 - 맞춤 진단 퀴즈"""
from typing import Dict, Any, List
import random
from ..state import GraphState


def adaptive_diagnostic_node(state: GraphState) -> Dict[str, Any]:
    """
    약한 개념의 변별도 높은 문항으로 mastery 업데이트
    
    입력: weak_candidates (mastery < 0.5인 개념들)
    출력: 갱신된 mastery, quiz_records
    
    Note: 실제 구현에서는 사용자 응답을 받아야 하지만,
    데모에서는 자동으로 처리
    """
    print("📝 [AdaptiveDiagnostic] 진단 퀴즈 생성 중...")
    
    mastery = state["mastery"]
    domain_pack = state["domain_pack"]
    memory = state["memory"]
    
    if not domain_pack:
        return {"current_step": "adaptive_diagnostic"}
    
    # 약한 개념 찾기
    weak_concepts = [
        concept_id for concept_id, score in mastery.levels.items()
        if score < 0.5
    ]
    
    # 해당 개념의 문항 선택 (최대 3문항)
    selected_questions = []
    question_bank = domain_pack.question_bank if hasattr(domain_pack, 'question_bank') else []
    for question in question_bank[:3]:
        if question["concept"] in weak_concepts:
            selected_questions.append(question)
    
    # 실제로는 사용자에게 질문하고 답변 받음
    # 데모에서는 랜덤 시뮬레이션
    quiz_records = []
    for q in selected_questions:
        # 시뮬레이션: 50% 확률로 정답
        user_answer = random.randint(0, len(q["options"]) - 1)
        is_correct = user_answer == q["correct"]
        
        quiz_records.append({
            "question_id": q["id"],
            "concept": q["concept"],
            "correct": is_correct
        })
        
        # mastery 업데이트
        if q["concept"] in mastery.levels:
            if is_correct:
                mastery.levels[q["concept"]] = min(1.0, mastery.levels[q["concept"]] + 0.15)
            else:
                mastery.levels[q["concept"]] = max(0.0, mastery.levels[q["concept"]] - 0.1)
    
    memory.quiz_records.extend(quiz_records)
    
    print(f"✅ [AdaptiveDiagnostic] 진단 완료: {len(selected_questions)}개 문항")
    
    return {
        "mastery": mastery,
        "memory": memory,
        "current_step": "adaptive_diagnostic"
    }

