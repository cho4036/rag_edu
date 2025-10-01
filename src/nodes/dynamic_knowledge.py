"""동적 도메인 지식 생성 - LLM을 통해 분야별 전문 지식 자동 생성"""
from typing import Dict, Any, List
import os
from ..state import DomainPack


def generate_domain_knowledge_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    감지된 분야에 대해 LLM을 활용하여 동적으로 전문 지식 생성
    
    입력: detected_domain
    출력: domain_pack (taxonomy, glossary, question_bank 등)
    """
    print("🧠 [DynamicKnowledge] 동적 지식 생성 중...")
    
    detected_domain = state.get("detected_domain", "General")
    
    # OpenAI API 사용 가능 여부 확인
    has_openai = os.getenv("OPENAI_API_KEY") is not None
    
    if has_openai:
        # LLM을 통한 동적 지식 생성
        domain_pack = generate_knowledge_with_llm(detected_domain)
    else:
        # API 키 없을 때 기본 템플릿 사용
        domain_pack = generate_knowledge_template(detected_domain)
    
    print(f"✅ [DynamicKnowledge] {detected_domain} 지식 생성 완료")
    
    return {
        "domain_pack": domain_pack,
        "current_step": "dynamic_knowledge"
    }


def generate_knowledge_with_llm(domain: str) -> DomainPack:
    """LLM을 사용하여 도메인 지식 생성"""
    try:
        from langchain_openai import ChatOpenAI
        from langchain.prompts import PromptTemplate
        import json
        
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
        
        # Taxonomy 생성 프롬프트
        taxonomy_prompt = PromptTemplate.from_template("""
You are an expert in {domain}. Create a comprehensive learning taxonomy.

Generate a JSON array of 8-10 core concepts with this structure:
[
  {{
    "id": "concept_id",
    "name": "개념명 (한국어)",
    "level": 0-3,
    "importance": 1-10,
    "prerequisites": ["prerequisite_ids"],
    "concepts": ["관련 세부 개념들"]
  }}
]

Domain: {domain}
Return ONLY valid JSON array, no explanation.
""")
        
        # Glossary 생성 프롬프트
        glossary_prompt = PromptTemplate.from_template("""
You are an expert in {domain}. Create a glossary of key terms.

Generate a JSON object with 15-20 essential terms and their definitions in Korean:
{{
  "Term1": "정의 (100자 이내)",
  "Term2": "정의 (100자 이내)",
  ...
}}

Domain: {domain}
Return ONLY valid JSON object, no explanation.
""")
        
        print(f"  📝 {domain} Taxonomy 생성 중...")
        taxonomy_response = llm.invoke(taxonomy_prompt.format(domain=domain))
        taxonomy = json.loads(taxonomy_response.content)
        
        print(f"  📚 {domain} Glossary 생성 중...")
        glossary_response = llm.invoke(glossary_prompt.format(domain=domain))
        glossary = json.loads(glossary_response.content)
        
        # Question Bank 생성
        questions = generate_questions_for_domain(domain, llm)
        
        # Tool Recipes 생성
        recipes = generate_tool_recipes(domain, llm)
        
        return DomainPack(
            taxonomy=taxonomy,
            glossary=glossary,
            question_bank=questions,
            tool_recipes=recipes,
            version="1.0-dynamic"
        )
        
    except Exception as e:
        print(f"  ⚠️ LLM 생성 실패: {e}")
        print(f"  → 템플릿 모드로 전환")
        return generate_knowledge_template(domain)


def generate_questions_for_domain(domain: str, llm) -> List[Dict]:
    """도메인별 진단 문항 생성"""
    from langchain.prompts import PromptTemplate
    import json
    
    try:
        question_prompt = PromptTemplate.from_template("""
Create 5 diagnostic questions for {domain} skill assessment.

JSON format:
[
  {{
    "id": "q1",
    "concept": "concept_id",
    "difficulty": 1-3,
    "question": "질문 (한국어)",
    "options": ["선택지1", "선택지2", "선택지3", "선택지4"],
    "correct": 0
  }}
]

Domain: {domain}
Return ONLY valid JSON array.
""")
        
        response = llm.invoke(question_prompt.format(domain=domain))
        return json.loads(response.content)
    except:
        return []


def generate_tool_recipes(domain: str, llm) -> List[Dict]:
    """도메인별 도구 추천 레시피 생성"""
    from langchain.prompts import PromptTemplate
    import json
    
    try:
        recipe_prompt = PromptTemplate.from_template("""
Create 3 tech stack recommendations for {domain} (beginner, intermediate, advanced).

JSON format:
[
  {{
    "name": "basic_{domain_short}",
    "level": "beginner",
    "components": {{"component_name": "tool/library"}},
    "pros": ["장점1", "장점2"],
    "cons": ["단점1", "단점2"]
  }}
]

Domain: {domain}
Return ONLY valid JSON array.
""")
        
        response = llm.invoke(recipe_prompt.format(
            domain=domain,
            domain_short=domain.lower().replace(" ", "_")
        ))
        return json.loads(response.content)
    except:
        return []


def generate_knowledge_template(domain: str) -> DomainPack:
    """템플릿 기반 기본 지식 생성 (API 키 없을 때)"""
    
    return DomainPack(
        taxonomy=[
            {
                "id": f"{domain.lower().replace(' ', '_')}_basics",
                "name": f"{domain} 기초",
                "level": 0,
                "importance": 10,
                "prerequisites": [],
                "concepts": ["fundamentals", "core_concepts", "terminology"]
            },
            {
                "id": f"{domain.lower().replace(' ', '_')}_intermediate",
                "name": f"{domain} 중급",
                "level": 1,
                "importance": 8,
                "prerequisites": [f"{domain.lower().replace(' ', '_')}_basics"],
                "concepts": ["best_practices", "common_patterns", "tools"]
            },
            {
                "id": f"{domain.lower().replace(' ', '_')}_advanced",
                "name": f"{domain} 고급",
                "level": 2,
                "importance": 7,
                "prerequisites": [f"{domain.lower().replace(' ', '_')}_intermediate"],
                "concepts": ["optimization", "architecture", "production"]
            }
        ],
        glossary={
            f"{domain}": f"{domain}에 대한 기본 개념과 원리",
            "Best Practices": "업계에서 검증된 모범 사례",
            "Tools": f"{domain}에서 자주 사용되는 도구와 라이브러리",
            "Architecture": "시스템 설계 및 구조",
            "Optimization": "성능 및 효율성 개선 기법"
        },
        question_bank=[
            {
                "id": "q1",
                "concept": f"{domain.lower().replace(' ', '_')}_basics",
                "difficulty": 1,
                "question": f"{domain}의 주요 목적은 무엇인가요?",
                "options": [
                    "문제 해결 및 가치 창출",
                    "단순 데이터 저장",
                    "UI 디자인",
                    "하드웨어 제어"
                ],
                "correct": 0
            }
        ],
        tool_recipes=[
            {
                "name": f"basic_{domain.lower().replace(' ', '_')}",
                "level": "beginner",
                "components": {
                    "primary_tool": "입문자용 도구",
                    "learning_resource": "공식 문서 및 튜토리얼"
                },
                "pros": ["빠른 시작", "낮은 진입 장벽"],
                "cons": ["제한적 기능", "확장성 부족"]
            }
        ],
        version="1.0-template"
    )

