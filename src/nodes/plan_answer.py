"""8. PlanAnswer 노드 - 솔루션 플랜 생성"""
from typing import Dict, Any
from ..state import GraphState, Plan


def plan_answer_node(state: GraphState) -> Dict[str, Any]:
    """
    사용자 제약/숙련도에 맞춘 답변 계획
    
    입력: taxonomy_map, user.constraints, mastery
    출력: plan.steps[], plan.options[], plan.tradeoffs[]
    """
    print("📋 [PlanAnswer] 답변 플랜 생성 중...")
    
    user = state["user"]
    intent = state["intent"]
    taxonomy_map = state["taxonomy_map"][0] if state["taxonomy_map"] else {}
    domain_pack = state["domain_pack"]
    
    # 경험 수준에 따른 설명 스타일 결정
    experience_level = user.prefs.get("experience_level", 1)
    explanation_levels = {
        0: "초보자용 (기본 개념부터)",
        1: "입문자용 (핵심 개념 중심)",
        2: "중급자용 (실전 구현 중심)",
        3: "고급자용 (최적화 및 고급 기법)"
    }
    explanation_style = explanation_levels.get(experience_level, "입문자용")
    
    # 의도별 체크리스트 구성
    steps = []
    
    if intent.type in ["design", "implementation", "learn_path"]:
        steps = [
            "1. 목표 및 제약사항 정의",
            "2. 데이터 준비 및 전처리",
            "3. 인덱싱 전략 (청킹, 메타데이터, 임베딩)",
            "4. 검색 전략 (BM25/Dense/Hybrid, k값 설정)",
            "5. 재랭킹 (필요시 cross-encoder 또는 LLM)",
            "6. 생성 단계 (프롬프트 설계, 출처 표시)",
            "7. 평가 (RAGAS, LLM-judge, 사용자 피드백)",
            "8. 배포 및 모니터링"
        ]
    elif intent.type == "evaluation":
        steps = [
            "1. 평가 데이터셋 준비 (질문-답변-참조문서)",
            "2. 평가 지표 선택 (Faithfulness, Relevance, Answer Quality)",
            "3. RAGAS 또는 LLM-judge 설정",
            "4. 베이스라인 성능 측정",
            "5. 개선 실험 및 A/B 테스트"
        ]
    elif intent.type == "optimization":
        steps = [
            "1. 현재 성능 프로파일링 (지연시간, 비용)",
            "2. 병목 구간 식별",
            "3. 캐싱 전략 적용",
            "4. 배치 처리 및 비동기 처리",
            "5. 모델 최적화 (양자화, 프루닝)",
            "6. 인프라 스케일링 (오토스케일링, 로드밸런싱)"
        ]
    else:
        steps = [
            "1. 문제 상황 분석",
            "2. 관련 개념 이해",
            "3. 솔루션 탐색",
            "4. 실행 및 검증"
        ]
    
    # 대안 옵션 (간단/표준/고급)
    options = []
    if domain_pack:
        tool_recipes = domain_pack.tool_recipes if hasattr(domain_pack, 'tool_recipes') else []
        for recipe in tool_recipes:
            options.append({
                "name": recipe["name"],
                "level": recipe["level"],
                "components": recipe["components"],
                "pros": recipe["pros"],
                "cons": recipe["cons"]
            })
    
    # 트레이드오프
    tradeoffs = []
    constraints = user.constraints
    
    if "latency_priority" in constraints and "quality_priority" in constraints:
        tradeoffs.append({
            "dimension": "속도 vs 품질",
            "description": "저지연을 위해서는 재랭킹 생략, 고품질을 위해서는 cross-encoder 사용",
            "recommendation": "하이브리드 접근: 초기엔 빠르게, 중요 쿼리만 재랭킹"
        })
    
    if "cost_priority" in constraints:
        tradeoffs.append({
            "dimension": "비용 vs 성능",
            "description": "임베딩 모델 크기, LLM 선택에 따라 비용 차이",
            "recommendation": f"경험 수준 {experience_level}에 맞춰 {'기본' if experience_level < 2 else '프로덕션'} 구성 추천"
        })
    
    plan = Plan(
        steps=steps,
        options=options,
        tradeoffs=tradeoffs
    )
    
    print(f"✅ [PlanAnswer] 플랜 생성 완료: {len(steps)}단계, {len(options)}개 옵션")
    
    return {
        "plan": plan,
        "current_step": "plan_answer"
    }

