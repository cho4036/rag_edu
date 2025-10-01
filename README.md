# 🎓 동적 분야 학습 챗봇

사용자와 인터랙션 하며 **사용자의 질문에서 자동으로 분야를 감지**하고, 해당 분야의 **전문가로 동적 변신**하여 사용자의 지식이 최신 트렌드까지 스탭 바이 스탭으로 배우며 도달할 수 있도록 도와주는 챗봇.

**핵심 특징:**
- 🔎 **분야 자동 감지**: RAG, ML, Backend, DevOps 등 10개 이상 분야
- 🧠 **동적 전문가 변신**: LLM으로 분야별 전문 지식 자동 생성
- 📊 **적응형 학습**: 사용자 수준 파악 및 맞춤 가이드
- 🛠️ **실전 중심**: 도구 추천, 체크리스트, 트레이드오프 분석

> ⚠️ **중요 변경**: 기존 RAG 전용에서 **범용 학습 시스템**으로 진화했습니다!  
> 자세한 내용은 [DYNAMIC_FEATURES.md](DYNAMIC_FEATURES.md) 참고

venv를 활용.

## 🚀 빠른 시작

```bash
# 설치
pip3 install -r requirements.txt

# 환경 변수 설정 (선택사항)
cp .env.example .env
# .env 파일에 OPENAI_API_KEY 추가 (동적 지식 생성용)

# 실행
python3 app.py
```

**API 키 없이도** 템플릿 모드로 동작합니다!

자세한 설치 방법은 [SETUP.md](SETUP.md)를 참고하세요.

## 🌟 새로운 기능

- **분야 자동 감지**: 질문만으로 분야 파악
- **동적 지식 생성**: LLM이 전문 지식 자동 생성
- **범용 학습**: RAG뿐 아니라 모든 기술 분야 지원

자세한 내용: [DYNAMIC_FEATURES.md](DYNAMIC_FEATURES.md)

## 🛠️ 기술 스택

- **LangGraph**: 복잡한 워크플로우 관리
- **Gradio**: 사용자 인터페이스 제공  
- **OpenAI**: LLM (dotenv를 통해 OPENAI_API_KEY 환경변수 사용)
- **Pydantic**: 타입 안전성

## 📁 프로젝트 구조

```
rag_edu/
├── app.py              # Gradio UI
├── requirements.txt    # 의존성
├── src/
│   ├── state.py       # 상태 스키마
│   ├── graph.py       # LangGraph 그래프
│   ├── nodes/         # 14개 노드
│   └── utils/         # 도메인 데이터
└── test_simple.py     # 테스트 스크립트
```

---

## 📖 상세 설계 문서

### 0) 공통: 그래프 전반 설계

전역 상태(State) 스키마

user: { id, lang, prefs, constraints(budget, latency_ms, deploy_env, code_langs[]) }

domain_pack: { taxonomy[], glossary[], question_bank[], tool_recipes[], version }

signals: { terms[], skills[], code_fragments[], logs[] }

mastery: { concept_id: 0.0~1.0 } // 사용자 숙련도 확률

intent: { type, sub_type, confidence }

task: { question, context_docs_meta[], required_outputs[] }

plan: { steps[], options[], tradeoffs[] }

answer: { outline, content_blocks[], snippets[], citations[] }

gaps: { unknown_terms_ranked[], prereq_recos[] }

eval: { confidence, risks[], next_actions[] }

memory: { seen_terms[], history[], quiz_records[] }

상태 전이 규칙

각 노드는 state를 읽고 필요한 필드만 갱신.

실패/불확실 시 eval.confidence/eval.risks를 낮추고, 재시도/대안 경로로 분기.

어떤 분야에 대해 궁금해? 라는 챗봇의 질문으로 시작

사용자가 답변을 하면 답변을 통해 어떤 분야인지 파악.

파악한 후에는 해당 분야에 대해 전문가 부팅부터 시작. 

1) DomainBootstrap (전문가 부팅)

목표: “RAG 전문가 페르소나” 준비 & 도메인 자료 로딩
입력: 초기 사용자 질문/명령
출력: domain_pack 로딩, tool_recipes 활성화
세부 작업

domain_pack 로드: taxonomy(개념/선수지식/중요도), glossary, question_bank, 모범 설계 레시피

신뢰도 가드 설정: self-consistency 샘플 횟수, 반례 탐색 체크리스트

도구 슬롯 선언(필요시): 인덱싱 설계 도우미, 임베딩 선택기, 재랭킹 카탈로그, 평가 파이프라인 템플릿

Edges

→ UserSignals (항상)

실패 처리

pack 일부 누락 시 축소 모드로 실행(핵심 taxonomy만) + eval.risks += ["reduced_knowledge_base"]

2) UserSignals (대화 신호 추출)

목표: 사용자의 관심/숙련 단서 추출
입력: 사용자의 현재 메시지(예: “RAG를 구축하려면 무엇을 해야 해?”)
출력: signals.terms, signals.skills
세부 작업

용어/엔티티 추출 → taxonomy/glossary 매칭

코드/로그 패턴 감지(예: “BM25”, “bge-m3”, “RAGAS”, “vLLM”, “Gateway API” 등)

도메인 맥락 벡터화(선택)로 하위 카테고리 후보 산출

Edges

(콜드스타트 신호 부족) → ColdstartProbe

(신호 충분) → InferLevel

실패 처리

추출 결과 빈약 → eval.risks += ["low_signal"] 후 ColdstartProbe 강제

3) ColdstartProbe (초기 진단&선호 수집, 최대 60초 흐름)

목표: 최소 질문으로 제약/선호/경험 수집
입력: 없음(내부 질문)
출력: user.prefs, user.constraints, 우선순위 도출키
세부 작업

짧은 자가진술: 경험(0~3), 사용 언어(Go/Py), 배포환경(K8s/서버리스), 목표 지연/비용, 데이터 유형/언어

예/아니오 3~5문항(“벡터DB 직접 운영 경험?” 등)

Edges

→ InferLevel

실패 처리

응답 불충분 → 보수적 기본값 세팅 + eval.risks += ["assumed_defaults"]

4) InferLevel (숙련도 추정)

목표: concept 단위 P(mastery) 초기화/업데이트
입력: signals, user.prefs, 콜드스타트 응답
출력: mastery(초기 분포), memory.seen_terms 갱신
세부 작업

신호 기반 prior 보정(전문 용어/도구 언급 → 관련 노드 prior↑)

부족한 영역 태그 수집 → weak_candidates

AdaptiveDiagnostic 필요 여부 결정

Edges

(불확실↑ or 약점 다수) → AdaptiveDiagnostic

(충분) → IntentDetect

실패 처리

태깅 모호 → 보수적 추정(0.4~0.6) + 이후 노드에서 보강

5) AdaptiveDiagnostic (맞춤 진단 퀴즈 3~5문항)

목표: 약한 개념의 변별도 높은 문항으로 mastery 업데이트
입력: weak_candidates
출력: 갱신된 mastery, quiz_records
세부 작업

개념 태그별 난이도/변별도 고려해 문항 구성(객관/시나리오/짧은 서술 혼합)

정답/오답에 따라 α/β 규칙으로 mastery 업데이트

과적합 방지: 동일 개념 반복 출제 제한

Edges

→ IntentDetect

실패 처리

응답 미완 → 미답 문항 제외, eval.risks += ["partial_diagnostic"]

6) IntentDetect (의도/태스크 분류)

목표: 질문 성격 파악(설계/디버깅/비교/최적화/코드생성/평가 등)
입력: 사용자 질문 + signals
출력: intent
세부 작업

구조화된 의도:

design(아키텍처/선택지), implementation(코드/설정),

evaluation(RAGAS/AB), optimization(latency/cost),

troubleshoot, compare, explain, learn_path

의도별 필수 산출물 템플릿 지정

Edges

→ TaxonomyMap

실패 처리

다중 의도 → 우선순위 가정(가장 상위) + 대안 경로 제시

7) TaxonomyMap (개념 매핑)

목표: 질문을 taxonomy의 관련 노드들에 매핑
입력: intent, signals
출력: 관련 개념 리스트(핵심/보조), 선후관계(Prereq Chain)
세부 작업

핵심 개념 식별(예: Chunking, Embedding Selection, Hybrid Retrieval, Reranking, Prompting, Evaluation)

선수지식 자동 확장(부족 mastery면 강조)

Edges

→ PlanAnswer

실패 처리

매핑 애매 → 넓은 상위 노드로 승격 후 PlanAnswer에서 분기

8) PlanAnswer (솔루션 플랜 생성)

목표: 사용자 제약/숙련도에 맞춘 답변 계획
입력: taxonomy_map, user.constraints, mastery
출력: plan.steps[], plan.options[], plan.tradeoffs[]
세부 작업

레벨별 설명 스타일 결정(L0~L4)

체크리스트 구성:

목표/제약 수립

인덱싱(청킹/메타/ACL)

검색전략(BM25/Dense/Hybrid, k, expand)

재랭킹(언제/어떻게/비용)

생성(프롬프트/출처/가드레일/툴콜)

평가(RAGAS/LLM-judge/AB)

배포/관찰(K8s/Autoscale/캐시/비용)

대안/트레이드오프: 간단/표준/고급 3안

Edges

→ (필요시) ToolAdvisors

→ GapMining

실패 처리

제약 충돌(예: 초저지연 vs 고정밀) → 트레이드오프 명시 및 분기 제안

9) ToolAdvisors (선택적: 도구 조언 모듈)

목표: 설정/모델/재랭커/평가 템플릿 추천
입력: plan, user.constraints
출력: 후보 옵션 표(장단점/비용/지연)
세부 작업

임베딩: 언어/도메인/비용 기반 후보

재랭킹: cross-encoder vs LLM rerank 기준

평가: 데이터 가용/타깃 지표에 따른 파이프라인 선택

Edges

→ GapMining

실패 처리

근거 부족 → 복수 옵션을 비용/지연/품질 매트릭스와 함께 제시

10) GapMining (지식 갭/모르는 용어 추천)

목표: UnknownScore로 Top-N 용어/개념 추천
입력: signals, mastery, taxonomy_map
출력: gaps.unknown_terms_ranked, gaps.prereq_recos
세부 작업

UnknownScore = 빈도 × 중요도 × (1 - P_mastery) × 참신성

각 용어에 2~3줄 요약 + 선수지식 링크 + 1분 미니퀴즈(옵션)

Edges

→ ComposeAnswer

실패 처리

후보 과다 → 카테고리별 1~2개로 컷

11) ComposeAnswer (최종 응답 구성)

목표: 레벨 적응형 답변/체크리스트/아티팩트 요약
입력: plan, tool_advice, gaps
출력: answer(구조화된 섹션), eval(자신감/리스크/다음 행동)
세부 작업

구조:

(1) 너의 목표/제약 요약

(2) 권장 아키텍처(선택지+트레이드오프)

(3) 단계별 체크리스트

(4) 초기 설정값/주의점

(5) 평가와 다음 실험

(6) 모르는 용어 Top-5 + 선수지식

(7) 다음 액션 2~3개

신뢰도 마킹: 출처/불확실 구간/실패 모드

Edges

→ QualityGate

실패 처리

내용 과장/확신 편향 감지 시 self-critique 루프 1회

12) QualityGate (품질/가드레일 검수)

목표: 응답의 일관성/안전성/유용성 확인
입력: answer, eval
출력: 보정된 answer, 업데이트된 eval
세부 작업

self-consistency(요지 3회 요약 비교)

반례 탐색(언제 실패하는가?)

중복/장황 제거, 실행 가능 항목 강조

Edges

→ MemoryWrite → Deliver

실패 처리

자신감 낮음 → eval.next_actions에 “추가 정보 요청/짧은 퀴즈/샘플 데이터 업로드” 제안

13) MemoryWrite (장기 개인화)

목표: 사용자 프로필/숙련도/용어 히스토리 기록
입력: mastery, gaps, 상호작용 로그
출력: 갱신된 memory
세부 작업

mastery 스냅샷, seen_terms 추가

다음 세션용 콜드스타트 단축키 생성(선호/제약 캐시)

Edges

→ Deliver

실패 처리

저장 실패 시 최소한 mastery만 스냅샷

14) Deliver (응답 출력)

목표: 사용자에게 최종 결과 제공
입력: answer, eval
출력: 메시지(섹션/체크리스트/다음 액션)
세부 작업

레벨 맞춤 톤 & 길이

“다음으로 눌러서 할 일” 2~3개 버튼/옵션(예: “미니퀴즈 시작”, “인덱싱 설계 마법사 열기”)

그래프 연결(요약)

DomainBootstrap → UserSignals → (ColdstartProbe?) → InferLevel → (AdaptiveDiagnostic?) → IntentDetect → TaxonomyMap → PlanAnswer → (ToolAdvisors?) → GapMining → ComposeAnswer → QualityGate → MemoryWrite → Deliver

운영/평가 지표

정확/유용: 사용자 재질문 감소율, 체크리스트 완료율, 추천 용어 클릭/학습율

학습 진전: mastery 향상 추세, 미니퀴즈 정답률

성능/비용: 응답지연 p95, 토큰/콜 수, 재시도율

안전: 과신(허위확신) 경고 발생률↓, 반례 명시율↑

실패/모호성 대응 규칙

정보 부족: PlanAnswer에서 선택지+트레이드오프로 설계, next_actions에 구체 입력 요청

충돌 제약: “목표 재정의”를 첫 단계로 제안(예: 품질 우선/지연 우선 모드)

숙련 불일치: AdaptiveDiagnostic 재호출 또는 L1↔L3 설명 레벨 조정

바로 적용 팁 (너에게 최적화)

K8s 배포 모드: Plan 단계에서 템플릿 산출물 타입만 바꿔 끼우기(Helm values, Ingress/Gateway, vLLM/TEI, reranker svc)

성능/비용 컨트롤러: ToolAdvisors에서 k, rerank depth, token budget을 “슬라이더” 매개변수로 노출

지식 갭 루프: 매 세션 종료 시 Top-3 용어 + 1분 퀴즈 노출 → mastery 자동 업데이트