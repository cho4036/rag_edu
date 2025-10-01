"""1. DomainBootstrap 노드 - 전문가 부팅 및 도메인 자료 로딩 (동적)"""
from typing import Dict, Any
from ..state import GraphState, DomainPack


def domain_bootstrap_node(state: GraphState) -> Dict[str, Any]:
    """
    감지된 분야의 전문가 페르소나 준비 및 도메인 자료 로딩
    
    입력: detected_domain, domain_pack (이미 생성됨)
    출력: 전문가 페르소나 활성화
    """
    print("🚀 [DomainBootstrap] 전문가 부팅 중...")
    
    detected_domain = state.get("detected_domain", "General")
    domain_pack_data = state.get("domain_pack")
    
    if domain_pack_data:
        # 이미 동적으로 생성된 domain_pack 사용
        domain_pack = domain_pack_data
        print(f"✅ [DomainBootstrap] {detected_domain} 전문가 부팅 완료")
    else:
        # fallback: 기본 도메인 팩 생성
        print(f"⚠️ [DomainBootstrap] domain_pack이 없어 기본 팩 생성")
        from ..utils.domain_data import get_domain_pack
        domain_data = get_domain_pack()
        domain_pack = DomainPack(
            taxonomy=domain_data["taxonomy"],
            glossary=domain_data["glossary"],
            question_bank=domain_data["question_bank"],
            tool_recipes=domain_data["tool_recipes"],
            version=domain_data["version"]
        )
    
    # 분야별 전문가 페르소나 메시지
    expert_persona = f"""
당신은 이제 {detected_domain} 분야의 최고 전문가입니다.

역할:
- 사용자의 {detected_domain} 학습을 단계별로 지원
- 사용자 수준에 맞는 맞춤형 설명 제공
- 실전에 필요한 도구와 기법 추천
- 지식 갭을 자동으로 감지하고 보완

전문 지식:
- {len(domain_pack.taxonomy) if hasattr(domain_pack, 'taxonomy') else 0}개 핵심 개념
- {len(domain_pack.glossary) if hasattr(domain_pack, 'glossary') else 0}개 전문 용어
- 검증된 도구 및 레시피

목표: 사용자가 {detected_domain}를 효과적으로 학습하고 실전에 적용할 수 있도록 돕기
"""
    
    print(expert_persona)
    
    eval_obj = state["eval"]
    eval_obj.confidence = 0.9
    
    return {
        "domain_pack": domain_pack,
        "current_step": "domain_bootstrap",
        "eval": eval_obj
    }

