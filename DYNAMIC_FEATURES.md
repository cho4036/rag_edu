# 🌟 동적 분야 학습 시스템

## 핵심 변경사항

기존 RAG 전용 챗봇에서 **어떤 분야든 학습 가능한 동적 시스템**으로 업그레이드되었습니다!

## 🎯 주요 특징

### 1. 자동 분야 감지 (DomainDetect)

질문을 분석하여 자동으로 분야를 감지합니다:

```python
"RAG 구축하고 싶어" → RAG 분야 감지
"딥러닝 시작하려면?" → Machine Learning 감지
"FastAPI 배우고 싶어" → Backend Development 감지
"React 상태 관리" → Frontend Development 감지
```

**지원 분야 (확장 가능):**
- RAG (Retrieval-Augmented Generation)
- Machine Learning / Deep Learning
- Backend Development
- Frontend Development
- DevOps
- Data Science
- Blockchain
- Cloud Computing
- Cybersecurity
- Mobile Development
- ... 및 기타 모든 분야

### 2. 동적 전문 지식 생성 (DynamicKnowledge)

감지된 분야에 대해 LLM을 활용하여 **실시간으로 전문 지식 생성**:

```python
# OpenAI API를 사용하여 자동 생성
- Taxonomy: 8-10개 핵심 개념 계층 구조
- Glossary: 15-20개 필수 용어 정의
- Question Bank: 5개 진단 문항
- Tool Recipes: 3개 레벨별 추천 구성
```

**API 키 없을 때**: 템플릿 기반 기본 지식 자동 생성

### 3. 동적 전문가 페르소나 (DomainBootstrap)

감지된 분야의 전문가로 **동적 변신**:

```
당신은 이제 {분야} 분야의 최고 전문가입니다.

역할:
- 사용자의 {분야} 학습을 단계별로 지원
- 사용자 수준에 맞는 맞춤형 설명 제공
- 실전에 필요한 도구와 기법 추천
- 지식 갭을 자동으로 감지하고 보완
```

## 📊 새로운 워크플로우

```
사용자 질문
    ↓
🔎 DomainDetect
    ↓ (분야 감지: RAG / ML / Backend 등)
🧠 DynamicKnowledge
    ↓ (LLM으로 Taxonomy/Glossary 생성)
🚀 DomainBootstrap
    ↓ (해당 분야 전문가로 변신)
[기존 14개 노드와 동일]
    ↓
최종 답변
```

## 🆕 추가된 노드

### 1. DomainDetect 노드

**위치**: 그래프 시작점  
**역할**: 사용자 질문 분석 → 분야 자동 감지  
**출력**: `detected_domain`, `domain_confidence`

**특징:**
- 키워드 패턴 매칭으로 분야 감지
- 10개 이상 분야 미리 정의
- 신뢰도 점수 계산
- 새 분야 쉽게 추가 가능

### 2. DynamicKnowledge 노드

**위치**: DomainDetect 직후  
**역할**: LLM으로 분야별 전문 지식 생성  
**출력**: `domain_pack` (동적 생성)

**특징:**
- OpenAI GPT-4 활용
- Taxonomy 자동 생성
- Glossary 자동 생성
- Question Bank 자동 생성
- API 키 없으면 템플릿 모드

## 💡 사용 예시

### 예시 1: RAG 분야

```
질문: "RAG를 구축하려면 무엇을 해야 해?"

→ 분야 감지: RAG
→ 지식 생성: RAG Taxonomy (인덱싱, 검색, 생성, 평가 등)
→ 전문가 모드: RAG 전문가
→ 답변: RAG 구축 단계별 가이드
```

### 예시 2: Machine Learning 분야

```
질문: "딥러닝을 처음 시작하는데 어떻게 배워야 해?"

→ 분야 감지: Machine Learning
→ 지식 생성: ML Taxonomy (신경망, CNN, RNN, 최적화 등)
→ 전문가 모드: ML 전문가
→ 답변: 딥러닝 입문 로드맵 + 도구 추천
```

### 예시 3: Backend Development 분야

```
질문: "FastAPI로 REST API 서버 만들고 싶어"

→ 분야 감지: Backend Development
→ 지식 생성: Backend Taxonomy (API, DB, 인증, 배포 등)
→ 전문가 모드: Backend 전문가
→ 답변: FastAPI 프로젝트 시작 가이드
```

## 🔧 코드 구조

### 새 파일

```
src/nodes/
├── domain_detect.py          # 분야 감지
└── dynamic_knowledge.py      # 동적 지식 생성
```

### 수정된 파일

```
src/
├── state.py                  # detected_domain 필드 추가
├── graph.py                  # 새 노드 통합
└── nodes/
    └── domain_bootstrap.py   # 동적 페르소나 지원
```

## 📈 확장 방법

### 1. 새 분야 추가

`src/nodes/domain_detect.py`에서:

```python
domain_patterns = {
    "Your New Domain": [
        "keyword1", "keyword2", "keyword3",
        # ... 관련 키워드 추가
    ],
    # ...
}
```

### 2. LLM 프롬프트 커스터마이징

`src/nodes/dynamic_knowledge.py`에서:

```python
taxonomy_prompt = PromptTemplate.from_template("""
# 원하는 형식으로 수정
""")
```

### 3. 템플릿 모드 개선

API 키 없을 때 사용되는 기본 템플릿 개선:

```python
def generate_knowledge_template(domain: str):
    # 더 풍부한 기본 지식 추가
```

## 🎓 교육적 효과

### Before (RAG 전용)
- ❌ RAG 분야만 지원
- ❌ 고정된 지식 베이스
- ❌ 다른 분야 질문 시 부적합한 답변

### After (동적 분야)
- ✅ 어떤 분야든 지원
- ✅ 동적 지식 생성
- ✅ 분야 맞춤 전문가
- ✅ 확장 가능한 구조

## 🚀 성능

- **분야 감지**: ~100ms
- **지식 생성 (LLM)**: ~5-10초
- **지식 생성 (템플릿)**: ~10ms
- **전체 처리**: 기존 대비 +5-10초 (초기 1회만)

## 🔮 향후 계획

1. **캐싱 시스템**
   - 분야별 지식 캐시
   - 재질문 시 즉시 응답

2. **멀티모달 지원**
   - 코드 예제 생성
   - 다이어그램 자동 생성

3. **분야 자동 학습**
   - 사용자 질문으로 분야 패턴 자동 업데이트
   - 새 분야 자동 추가

4. **협업 학습**
   - 여러 분야 연결 (예: RAG + Backend)
   - 통합 프로젝트 가이드

## 📝 마이그레이션 가이드

### 기존 사용자

기존 RAG 전용 기능은 그대로 유지됩니다:

```python
# 기존과 동일하게 작동
response = run_rag_education_bot("RAG 구축 방법")
```

### 새 기능 사용

다양한 분야 질문 가능:

```python
# ML 질문
run_rag_education_bot("딥러닝 시작하기")

# Backend 질문
run_rag_education_bot("FastAPI 배우기")

# DevOps 질문
run_rag_education_bot("Kubernetes 배포")
```

## 🎉 결론

**이제 하나의 챗봇으로 모든 기술 분야를 학습할 수 있습니다!**

---

**질문이나 제안**: 이슈를 생성해주세요.

