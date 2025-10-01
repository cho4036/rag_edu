"""9. ToolAdvisors 노드 - 도구 조언 모듈 (선택적)"""
from typing import Dict, Any, List
from ..state import GraphState


def tool_advisors_node(state: GraphState) -> Dict[str, Any]:
    """
    설정/모델/재랭커/평가 템플릿 추천
    
    입력: plan, user.constraints
    출력: 후보 옵션 표 (장단점/비용/지연)
    """
    print("🛠️ [ToolAdvisors] 도구 추천 생성 중...")
    
    user = state["user"]
    constraints = user.constraints
    experience_level = user.prefs.get("experience_level", 1)
    
    tool_advice = []
    
    # 임베딩 모델 추천
    embedding_options = [
        {
            "category": "embedding",
            "name": "OpenAI text-embedding-3-small",
            "pros": ["빠른 속도", "낮은 비용", "간단한 API"],
            "cons": ["한국어 성능 보통", "외부 의존성"],
            "cost": "낮음 ($0.02/1M tokens)",
            "latency": "낮음 (~100ms)",
            "suitable_for": [0, 1]
        },
        {
            "category": "embedding",
            "name": "multilingual-e5-large",
            "pros": ["우수한 한국어 성능", "오픈소스", "자체 호스팅 가능"],
            "cons": ["큰 모델 크기", "GPU 필요"],
            "cost": "중간 (호스팅 비용)",
            "latency": "중간 (~200ms)",
            "suitable_for": [1, 2, 3]
        },
        {
            "category": "embedding",
            "name": "bge-m3",
            "pros": ["다중 언어 지원", "dense+sparse 하이브리드", "SOTA 성능"],
            "cons": ["높은 컴퓨팅 요구", "복잡한 설정"],
            "cost": "높음",
            "latency": "높음 (~300ms)",
            "suitable_for": [2, 3]
        }
    ]
    
    # 경험 수준에 맞는 임베딩 추천
    for option in embedding_options:
        if experience_level in option["suitable_for"]:
            tool_advice.append(option)
    
    # 재랭킹 옵션
    if experience_level >= 1:
        rerank_options = [
            {
                "category": "reranking",
                "name": "cross-encoder (ms-marco)",
                "pros": ["높은 정확도", "검증된 모델"],
                "cons": ["추가 지연 (~100ms/doc)", "GPU 권장"],
                "cost": "중간",
                "latency": "중간",
                "when_to_use": "정확도가 중요하고 문서가 10개 이하일 때"
            },
            {
                "category": "reranking",
                "name": "LLM-based reranking",
                "pros": ["최고 정확도", "컨텍스트 이해"],
                "cons": ["높은 비용", "높은 지연"],
                "cost": "높음",
                "latency": "높음",
                "when_to_use": "고가치 쿼리, 복잡한 판단 필요시"
            }
        ]
        
        if "quality_priority" in constraints:
            tool_advice.extend(rerank_options)
    
    # 평가 도구
    if experience_level >= 1:
        eval_option = {
            "category": "evaluation",
            "name": "RAGAS",
            "pros": ["포괄적 지표", "자동화 가능", "오픈소스"],
            "cons": ["LLM API 비용", "설정 필요"],
            "metrics": ["Faithfulness", "Answer Relevance", "Context Precision", "Context Recall"],
            "setup_difficulty": "중간"
        }
        tool_advice.append(eval_option)
    
    print(f"✅ [ToolAdvisors] 추천 완료: {len(tool_advice)}개 도구")
    
    return {
        "tool_advice": tool_advice,
        "current_step": "tool_advisors"
    }

