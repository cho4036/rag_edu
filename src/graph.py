"""LangGraph 그래프 구성 - 동적 분야 학습을 위한 워크플로우"""
from langgraph.graph import StateGraph, END
from typing import Literal

from .state import GraphState, create_initial_state
from .nodes.domain_detect import domain_detect_node
from .nodes.dynamic_knowledge import generate_domain_knowledge_node
from .nodes.domain_bootstrap import domain_bootstrap_node
from .nodes.user_signals import user_signals_node
from .nodes.coldstart_probe import coldstart_probe_node
from .nodes.infer_level import infer_level_node
from .nodes.adaptive_diagnostic import adaptive_diagnostic_node
from .nodes.intent_detect import intent_detect_node
from .nodes.taxonomy_map import taxonomy_map_node
from .nodes.plan_answer import plan_answer_node
from .nodes.tool_advisors import tool_advisors_node
from .nodes.gap_mining import gap_mining_node
from .nodes.compose_answer import compose_answer_node
from .nodes.quality_gate import quality_gate_node
from .nodes.memory_write import memory_write_node
from .nodes.deliver import deliver_node


# ============ 조건부 엣지 함수들 ============

def should_coldstart(state: GraphState) -> Literal["coldstart_probe", "infer_level"]:
    """UserSignals 후 콜드스타트가 필요한지 판단"""
    if state["needs_coldstart"]:
        return "coldstart_probe"
    return "infer_level"


def should_diagnostic(state: GraphState) -> Literal["adaptive_diagnostic", "intent_detect"]:
    """InferLevel 후 진단 퀴즈가 필요한지 판단"""
    if state["needs_diagnostic"]:
        return "adaptive_diagnostic"
    return "intent_detect"


def should_use_tool_advisors(state: GraphState) -> Literal["tool_advisors", "gap_mining"]:
    """PlanAnswer 후 도구 추천이 필요한지 판단"""
    experience_level = state["user"].prefs.get("experience_level", 1)
    intent_type = state["intent"].type
    
    # 중급 이상이거나 설계/구현 의도일 때 도구 추천
    if experience_level >= 1 or intent_type in ["design", "implementation", "optimization"]:
        return "tool_advisors"
    return "gap_mining"


# ============ 그래프 빌드 ============

def create_graph():
    """동적 분야 학습 챗봇 그래프 생성"""
    
    # StateGraph 초기화
    workflow = StateGraph(GraphState)
    
    # 노드 추가 (NEW: 분야 감지 및 동적 지식 생성)
    workflow.add_node("domain_detect", domain_detect_node)
    workflow.add_node("dynamic_knowledge", generate_domain_knowledge_node)
    workflow.add_node("domain_bootstrap", domain_bootstrap_node)
    workflow.add_node("user_signals", user_signals_node)
    workflow.add_node("coldstart_probe", coldstart_probe_node)
    workflow.add_node("infer_level", infer_level_node)
    workflow.add_node("adaptive_diagnostic", adaptive_diagnostic_node)
    workflow.add_node("intent_detect", intent_detect_node)
    workflow.add_node("taxonomy_map", taxonomy_map_node)
    workflow.add_node("plan_answer", plan_answer_node)
    workflow.add_node("tool_advisors", tool_advisors_node)
    workflow.add_node("gap_mining", gap_mining_node)
    workflow.add_node("compose_answer", compose_answer_node)
    workflow.add_node("quality_gate", quality_gate_node)
    workflow.add_node("memory_write", memory_write_node)
    workflow.add_node("deliver", deliver_node)
    
    # 시작점 설정 (NEW: 분야 감지부터 시작)
    workflow.set_entry_point("domain_detect")
    
    # 엣지 연결 (노드 간 전이)
    # 0. DomainDetect → DynamicKnowledge (NEW)
    workflow.add_edge("domain_detect", "dynamic_knowledge")
    
    # 1. DynamicKnowledge → DomainBootstrap (NEW)
    workflow.add_edge("dynamic_knowledge", "domain_bootstrap")
    
    # 2. DomainBootstrap → UserSignals (항상)
    workflow.add_edge("domain_bootstrap", "user_signals")
    
    # 3. UserSignals → ColdstartProbe or InferLevel (조건부)
    workflow.add_conditional_edges(
        "user_signals",
        should_coldstart,
        {
            "coldstart_probe": "coldstart_probe",
            "infer_level": "infer_level"
        }
    )
    
    # 4. ColdstartProbe → InferLevel
    workflow.add_edge("coldstart_probe", "infer_level")
    
    # 5. InferLevel → AdaptiveDiagnostic or IntentDetect (조건부)
    workflow.add_conditional_edges(
        "infer_level",
        should_diagnostic,
        {
            "adaptive_diagnostic": "adaptive_diagnostic",
            "intent_detect": "intent_detect"
        }
    )
    
    # 6. AdaptiveDiagnostic → IntentDetect
    workflow.add_edge("adaptive_diagnostic", "intent_detect")
    
    # 7. IntentDetect → TaxonomyMap
    workflow.add_edge("intent_detect", "taxonomy_map")
    
    # 8. TaxonomyMap → PlanAnswer
    workflow.add_edge("taxonomy_map", "plan_answer")
    
    # 9. PlanAnswer → ToolAdvisors or GapMining (조건부)
    workflow.add_conditional_edges(
        "plan_answer",
        should_use_tool_advisors,
        {
            "tool_advisors": "tool_advisors",
            "gap_mining": "gap_mining"
        }
    )
    
    # 10. ToolAdvisors → GapMining
    workflow.add_edge("tool_advisors", "gap_mining")
    
    # 11. GapMining → ComposeAnswer
    workflow.add_edge("gap_mining", "compose_answer")
    
    # 12. ComposeAnswer → QualityGate
    workflow.add_edge("compose_answer", "quality_gate")
    
    # 13. QualityGate → MemoryWrite
    workflow.add_edge("quality_gate", "memory_write")
    
    # 14. MemoryWrite → Deliver
    workflow.add_edge("memory_write", "deliver")
    
    # 15. Deliver → END
    workflow.add_edge("deliver", END)
    
    # 그래프 컴파일
    app = workflow.compile()
    
    return app


# ============ 실행 함수 ============

def run_rag_education_bot(user_message: str) -> str:
    """
    동적 분야 학습 챗봇 실행
    
    Args:
        user_message: 사용자 입력 메시지
        
    Returns:
        최종 응답 문자열
    """
    # 그래프 생성
    app = create_graph()
    
    # 초기 상태 생성
    initial_state = create_initial_state(user_message)
    
    # 그래프 실행
    print("\n" + "=" * 50)
    print("🤖 동적 분야 학습 챗봇 시작")
    print("=" * 50 + "\n")
    
    try:
        # invoke로 전체 그래프 실행
        result = app.invoke(initial_state)
        
        # 최종 응답 반환
        return result.get("final_response", "응답을 생성할 수 없습니다.")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return f"오류가 발생했습니다: {str(e)}"


def run_rag_education_bot_stream(user_message: str):
    """
    동적 분야 학습 챗봇 스트리밍 실행 (각 노드의 출력을 실시간으로 확인)
    
    Args:
        user_message: 사용자 입력 메시지
        
    Yields:
        각 노드의 출력
    """
    # 그래프 생성
    app = create_graph()
    
    # 초기 상태 생성
    initial_state = create_initial_state(user_message)
    
    print("\n" + "=" * 50)
    print("🤖 동적 분야 학습 챗봇 시작 (스트리밍 모드)")
    print("=" * 50 + "\n")
    
    try:
        # stream으로 각 노드의 출력 확인
        for output in app.stream(initial_state):
            yield output
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        yield {"error": str(e)}

