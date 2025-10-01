"""11. ComposeAnswer 노드 - 최종 응답 구성"""
from typing import Dict, Any
from ..state import GraphState, Answer, Evaluation


def compose_answer_node(state: GraphState) -> Dict[str, Any]:
    """
    레벨 적응형 답변/체크리스트/아티팩트 요약
    
    입력: plan, tool_advice, gaps
    출력: answer (구조화된 섹션), eval (자신감/리스크/다음 행동)
    """
    print("✍️ [ComposeAnswer] 최종 답변 구성 중...")
    
    user = state["user"]
    intent = state["intent"]
    task = state["task"]
    plan = state["plan"]
    tool_advice = state["tool_advice"]
    gaps = state["gaps"]
    taxonomy_map = state["taxonomy_map"][0] if state["taxonomy_map"] else {}
    
    experience_level = user.prefs.get("experience_level", 1)
    
    # (1) 목표/제약 요약
    constraints_summary = "제약사항: "
    if user.constraints:
        constraints_summary += ", ".join([f"{k}={v}" for k, v in user.constraints.items()])
    else:
        constraints_summary += "없음"
    
    # (2) 권장 아키텍처
    architecture_section = "## 권장 아키텍처\n\n"
    if plan.options:
        recommended_option = plan.options[min(experience_level, len(plan.options) - 1)]
        architecture_section += f"**{recommended_option['name']}** ({recommended_option['level']})\n\n"
        architecture_section += "**구성 요소:**\n"
        for comp_name, comp_value in recommended_option['components'].items():
            architecture_section += f"- {comp_name}: {comp_value}\n"
        architecture_section += "\n**장점:** " + ", ".join(recommended_option['pros']) + "\n"
        architecture_section += "**단점:** " + ", ".join(recommended_option['cons']) + "\n"
    
    # (3) 단계별 체크리스트
    checklist_section = "\n## 단계별 체크리스트\n\n"
    for step in plan.steps:
        checklist_section += f"- [ ] {step}\n"
    
    # (4) 도구 추천
    tools_section = "\n## 추천 도구 및 설정\n\n"
    if tool_advice:
        for tool in tool_advice[:3]:  # 상위 3개
            tools_section += f"### {tool['name']} ({tool['category']})\n"
            tools_section += f"- **장점:** {', '.join(tool['pros'])}\n"
            tools_section += f"- **단점:** {', '.join(tool['cons'])}\n"
            if 'cost' in tool:
                tools_section += f"- **비용:** {tool['cost']}\n"
            if 'when_to_use' in tool:
                tools_section += f"- **사용 시기:** {tool['when_to_use']}\n"
            tools_section += "\n"
    
    # (5) 트레이드오프
    tradeoffs_section = "\n## 주요 트레이드오프\n\n"
    if plan.tradeoffs:
        for tradeoff in plan.tradeoffs:
            tradeoffs_section += f"**{tradeoff['dimension']}**\n"
            tradeoffs_section += f"- {tradeoff['description']}\n"
            tradeoffs_section += f"- 권장: {tradeoff['recommendation']}\n\n"
    
    # (6) 모르는 용어 Top-5
    gaps_section = "\n## 📚 알아두면 좋은 개념\n\n"
    if gaps.unknown_terms_ranked:
        for i, term in enumerate(gaps.unknown_terms_ranked[:5], 1):
            gaps_section += f"{i}. **{term['name']}** (중요도: {term['importance']}/10, 숙련도: {term['mastery_score']:.1f})\n"
            if term['related_terms']:
                for rt in term['related_terms'][:2]:
                    gaps_section += f"   - *{rt['term']}*: {rt['definition']}\n"
            gaps_section += "\n"
    
    if gaps.prereq_recos:
        gaps_section += "\n**선수지식 추천:**\n"
        for prereq in gaps.prereq_recos:
            gaps_section += f"- {prereq}\n"
    
    # (7) 다음 액션
    next_actions_section = "\n## 🎯 다음 단계\n\n"
    next_actions = []
    
    if experience_level == 0:
        next_actions = [
            "기본 개념 학습하기 (RAG 기초 튜토리얼)",
            "간단한 RAG 예제 따라하기",
            "미니퀴즈로 이해도 확인하기"
        ]
    elif experience_level == 1:
        next_actions = [
            "권장 아키텍처로 프로토타입 구축하기",
            "샘플 데이터로 검색 품질 테스트하기",
            "RAGAS로 기본 평가 수행하기"
        ]
    else:
        next_actions = [
            "프로덕션 환경 설정 및 배포",
            "성능 최적화 및 비용 분석",
            "A/B 테스트로 개선점 찾기"
        ]
    
    for action in next_actions:
        next_actions_section += f"1. {action}\n"
    
    # 전체 답변 조합
    outline = f"""
# {intent.type.upper()} 답변

**질문:** {task.question}

**경험 수준:** {experience_level} ({['초보', '입문', '중급', '고급'][experience_level]})
{constraints_summary}
"""
    
    content_blocks = [
        {"title": "권장 아키텍처", "content": architecture_section},
        {"title": "체크리스트", "content": checklist_section},
        {"title": "도구 추천", "content": tools_section},
        {"title": "트레이드오프", "content": tradeoffs_section},
        {"title": "학습 갭", "content": gaps_section},
        {"title": "다음 액션", "content": next_actions_section}
    ]
    
    # 전체 텍스트 생성
    full_response = outline
    for block in content_blocks:
        full_response += "\n" + block["content"]
    
    answer = Answer(
        outline=outline,
        content_blocks=content_blocks,
        snippets=[],
        citations=[]
    )
    
    # 평가 정보
    eval_obj = Evaluation(
        confidence=0.8 if intent.confidence > 0.6 else 0.6,
        risks=[],
        next_actions=next_actions
    )
    
    # 리스크 식별
    if not plan.options:
        eval_obj.risks.append("구체적인 아키텍처 옵션 부족")
    if not tool_advice:
        eval_obj.risks.append("도구 추천 정보 제한적")
    if len(gaps.unknown_terms_ranked) > 5:
        eval_obj.risks.append("많은 개념 갭 존재 - 단계적 학습 필요")
    
    print(f"✅ [ComposeAnswer] 답변 생성 완료: {len(content_blocks)}개 섹션")
    
    return {
        "answer": answer,
        "eval": eval_obj,
        "final_response": full_response,
        "current_step": "compose_answer"
    }

