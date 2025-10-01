# RAG 교육 챗봇 설치 및 실행 가이드

## 📋 프로젝트 구조

```
rag_edu/
├── README.md              # 프로젝트 설계 문서
├── SETUP.md              # 이 파일 (설치 가이드)
├── requirements.txt      # Python 의존성
├── app.py               # Gradio UI 진입점
├── .env.example         # 환경 변수 예제
├── src/
│   ├── __init__.py
│   ├── state.py         # 상태 스키마 정의
│   ├── graph.py         # LangGraph 그래프 구성
│   ├── nodes/           # 14개 노드 구현
│   │   ├── domain_bootstrap.py
│   │   ├── user_signals.py
│   │   ├── coldstart_probe.py
│   │   ├── infer_level.py
│   │   ├── adaptive_diagnostic.py
│   │   ├── intent_detect.py
│   │   ├── taxonomy_map.py
│   │   ├── plan_answer.py
│   │   ├── tool_advisors.py
│   │   ├── gap_mining.py
│   │   ├── compose_answer.py
│   │   ├── quality_gate.py
│   │   ├── memory_write.py
│   │   └── deliver.py
│   └── utils/
│       └── domain_data.py  # RAG 도메인 지식
└── data/                # (향후) 사용자 데이터 저장
```

## 🚀 설치 방법

### 1. 사전 요구사항

- Python 3.10 이상
- pip

### 2. 가상환경 생성 (권장)

```bash
cd /root/rag_edu
python -m venv venv

# 활성화
source venv/bin/activate  # Linux/Mac
# 또는
venv\Scripts\activate  # Windows
```

### 3. 의존성 설치

```bash
pip install -r requirements.txt
```

### 4. 환경 변수 설정

`.env` 파일을 생성하고 API 키를 설정하세요:

```bash
cp .env.example .env
```

`.env` 파일 내용:
```
OPENAI_API_KEY=your_openai_api_key_here
LANGCHAIN_API_KEY=your_langchain_api_key_here  # (선택사항)
LANGCHAIN_TRACING_V2=false  # 디버깅시 true로 설정
```

## ▶️ 실행 방법

### Gradio UI로 실행 (추천)

```bash
python app.py
```

브라우저에서 `http://localhost:7860` 접속

### Python 스크립트로 직접 실행

```python
from src.graph import run_rag_education_bot

response = run_rag_education_bot("RAG를 구축하려면 무엇을 해야 해?")
print(response)
```

### 스트리밍 모드 (디버깅용)

```python
from src.graph import run_rag_education_bot_stream

for output in run_rag_education_bot_stream("RAG 최적화 방법 알려줘"):
    print(output)
```

## 🧪 테스트 질문 예제

1. **초보자 질문**
   - "RAG가 뭐야?"
   - "RAG를 처음 시작하는데 어떻게 해야 해?"

2. **중급 질문**
   - "Hybrid Search를 구현하고 싶어"
   - "청킹 전략 중 어떤 걸 선택해야 할까?"

3. **고급 질문**
   - "프로덕션 RAG 시스템을 Kubernetes에 배포하고 싶어"
   - "RAG 시스템의 지연시간을 최적화하려면?"

4. **평가/비교 질문**
   - "BM25와 Dense Retrieval의 차이가 뭐야?"
   - "RAG 시스템을 어떻게 평가해?"

## 🔧 커스터마이징

### 도메인 지식 추가

`src/utils/domain_data.py` 파일을 수정하여:
- `RAG_TAXONOMY`: 개념 계층 구조 추가
- `RAG_GLOSSARY`: 용어 정의 추가
- `QUESTION_BANK`: 진단 퀴즈 추가
- `TOOL_RECIPES`: 권장 구성 추가

### 노드 동작 수정

각 노드는 `src/nodes/` 디렉토리에 독립적으로 구현되어 있어 쉽게 수정 가능합니다.

### 워크플로우 변경

`src/graph.py`의 `create_graph()` 함수에서:
- 노드 추가/제거
- 엣지 연결 변경
- 조건부 로직 수정

## 📊 시스템 아키텍처

```
사용자 입력
    ↓
DomainBootstrap (전문가 부팅)
    ↓
UserSignals (신호 추출)
    ↓
[ColdstartProbe] (선택적)
    ↓
InferLevel (숙련도 추정)
    ↓
[AdaptiveDiagnostic] (선택적)
    ↓
IntentDetect (의도 분류)
    ↓
TaxonomyMap (개념 매핑)
    ↓
PlanAnswer (플랜 생성)
    ↓
[ToolAdvisors] (선택적)
    ↓
GapMining (지식 갭 분석)
    ↓
ComposeAnswer (답변 구성)
    ↓
QualityGate (품질 검수)
    ↓
MemoryWrite (메모리 저장)
    ↓
Deliver (최종 전달)
```

## 🐛 문제 해결

### ImportError 발생

```bash
pip install --upgrade langgraph langchain gradio
```

### API 키 오류

`.env` 파일이 프로젝트 루트에 있고 올바른 형식인지 확인하세요.

### 그래프 실행 오류

디버깅을 위해 스트리밍 모드로 실행하여 어느 노드에서 오류가 발생하는지 확인:

```python
from src.graph import run_rag_education_bot_stream

for output in run_rag_education_bot_stream("테스트"):
    print(output)
```

## 📚 참고 자료

- [LangGraph 문서](https://langchain-ai.github.io/langgraph/)
- [Gradio 문서](https://www.gradio.app/docs/)
- [RAG 설계 원칙](https://python.langchain.com/docs/use_cases/question_answering/)

## 🤝 기여

이슈나 개선 제안은 언제든지 환영합니다!

## 📄 라이선스

MIT License

