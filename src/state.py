"""상태 스키마 정의 - LangGraph에서 사용할 전역 상태 구조"""
from typing import TypedDict, List, Dict, Optional, Annotated, Any
from pydantic import BaseModel, Field
import operator


# ============ Pydantic 모델 정의 ============

class User(BaseModel):
    """사용자 정보"""
    id: str = "default_user"
    lang: str = "ko"
    prefs: Dict[str, Any] = Field(default_factory=dict)
    constraints: Dict[str, Any] = Field(default_factory=dict)
    # budget, latency_ms, deploy_env, code_langs 등


class DomainPack(BaseModel):
    """도메인 지식 팩"""
    taxonomy: List[Dict[str, Any]] = Field(default_factory=list)
    glossary: Dict[str, str] = Field(default_factory=dict)
    question_bank: List[Dict[str, Any]] = Field(default_factory=list)
    tool_recipes: List[Dict[str, Any]] = Field(default_factory=list)
    version: str = "1.0"


class Signals(BaseModel):
    """사용자 대화에서 추출한 신호"""
    terms: List[str] = Field(default_factory=list)
    skills: List[str] = Field(default_factory=list)
    code_fragments: List[str] = Field(default_factory=list)
    logs: List[str] = Field(default_factory=list)


class Mastery(BaseModel):
    """개념별 숙련도 (0.0 ~ 1.0)"""
    levels: Dict[str, float] = Field(default_factory=dict)


class Intent(BaseModel):
    """사용자 의도 분류"""
    type: str = "unknown"  # design, implementation, evaluation, optimization, troubleshoot, compare, explain, learn_path
    sub_type: str = ""
    confidence: float = 0.0


class Task(BaseModel):
    """태스크 정보"""
    question: str = ""
    context_docs_meta: List[Dict[str, Any]] = Field(default_factory=list)
    required_outputs: List[str] = Field(default_factory=list)


class Plan(BaseModel):
    """솔루션 플랜"""
    steps: List[str] = Field(default_factory=list)
    options: List[Dict[str, Any]] = Field(default_factory=list)
    tradeoffs: List[Dict[str, Any]] = Field(default_factory=list)


class Answer(BaseModel):
    """최종 답변"""
    outline: str = ""
    content_blocks: List[Dict[str, str]] = Field(default_factory=list)
    snippets: List[str] = Field(default_factory=list)
    citations: List[str] = Field(default_factory=list)


class Gaps(BaseModel):
    """지식 갭"""
    unknown_terms_ranked: List[Dict[str, Any]] = Field(default_factory=list)
    prereq_recos: List[str] = Field(default_factory=list)


class Evaluation(BaseModel):
    """평가 정보"""
    confidence: float = 0.5
    risks: List[str] = Field(default_factory=list)
    next_actions: List[str] = Field(default_factory=list)


class Memory(BaseModel):
    """장기 메모리"""
    seen_terms: List[str] = Field(default_factory=list)
    history: List[Dict[str, Any]] = Field(default_factory=list)
    quiz_records: List[Dict[str, Any]] = Field(default_factory=list)


# ============ LangGraph State TypedDict ============

class GraphState(TypedDict):
    """LangGraph에서 사용할 전역 상태
    
    Annotated[List, operator.add]를 사용하여 메시지 누적
    """
    # 사용자 입력
    user_message: str
    chat_history: Annotated[List[Dict[str, str]], operator.add]
    
    # 분야 감지 (NEW)
    detected_domain: str
    domain_confidence: float
    
    # 핵심 상태
    user: User
    domain_pack: Optional[DomainPack]
    signals: Signals
    mastery: Mastery
    intent: Intent
    task: Task
    plan: Plan
    answer: Answer
    gaps: Gaps
    eval: Evaluation
    memory: Memory
    
    # 제어 플래그
    needs_coldstart: bool
    needs_diagnostic: bool
    taxonomy_map: List[Dict[str, Any]]
    tool_advice: List[Dict[str, Any]]
    
    # 현재 단계
    current_step: str
    
    # 최종 출력
    final_response: str


def create_initial_state(user_message: str = "") -> GraphState:
    """초기 상태 생성"""
    return GraphState(
        user_message=user_message,
        chat_history=[],
        detected_domain="",
        domain_confidence=0.0,
        user=User(),
        domain_pack=None,
        signals=Signals(),
        mastery=Mastery(),
        intent=Intent(),
        task=Task(question=user_message),
        plan=Plan(),
        answer=Answer(),
        gaps=Gaps(),
        eval=Evaluation(),
        memory=Memory(),
        needs_coldstart=False,
        needs_diagnostic=False,
        taxonomy_map=[],
        tool_advice=[],
        current_step="start",
        final_response=""
    )

