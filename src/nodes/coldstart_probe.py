"""3. ColdstartProbe 노드 - 초기 진단 및 선호 수집"""
from typing import Dict, Any
from ..state import GraphState


def coldstart_probe_node(state: GraphState) -> Dict[str, Any]:
    """
    최소 질문으로 제약/선호/경험 수집
    
    입력: 없음 (내부 질문)
    출력: user.prefs, user.constraints 갱신
    """
    print("❓ [ColdstartProbe] 초기 진단 시작...")
    
    # 실제로는 사용자에게 질문을 하고 응답을 받아야 하지만,
    # 데모에서는 user_message에서 추론
    user_message = state["user_message"].lower()
    user = state["user"]
    
    # 경험 수준 추론
    beginner_keywords = ["처음", "시작", "입문", "초보", "모르", "배우"]
    intermediate_keywords = ["경험", "해봤", "알고", "구현"]
    advanced_keywords = ["최적화", "프로덕션", "배포", "성능", "고급"]
    
    experience_level = 1  # 기본값
    if any(kw in user_message for kw in advanced_keywords):
        experience_level = 3
    elif any(kw in user_message for kw in intermediate_keywords):
        experience_level = 2
    elif any(kw in user_message for kw in beginner_keywords):
        experience_level = 0
    
    # 언어 선호 추론
    code_lang = "python"  # 기본값
    if "golang" in user_message or "go" in user_message:
        code_lang = "go"
    
    # 배포 환경 추론
    deploy_env = "local"
    if "k8s" in user_message or "kubernetes" in user_message:
        deploy_env = "kubernetes"
    elif "서버리스" in user_message or "serverless" in user_message:
        deploy_env = "serverless"
    elif "프로덕션" in user_message or "production" in user_message:
        deploy_env = "production"
    
    # 제약사항 추론
    constraints = {}
    if "빠른" in user_message or "지연" in user_message or "latency" in user_message:
        constraints["latency_priority"] = "high"
    if "비용" in user_message or "cost" in user_message or "저렴" in user_message:
        constraints["cost_priority"] = "high"
    if "정확" in user_message or "품질" in user_message or "accuracy" in user_message:
        constraints["quality_priority"] = "high"
    
    # 사용자 정보 업데이트
    user.prefs = {
        "experience_level": experience_level,
        "code_lang": code_lang,
        "deploy_env": deploy_env
    }
    user.constraints = constraints
    
    print(f"✅ [ColdstartProbe] 프로필 설정: 경험={experience_level}, 언어={code_lang}, 환경={deploy_env}")
    
    return {
        "user": user,
        "current_step": "coldstart_probe"
    }

