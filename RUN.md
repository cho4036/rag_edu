# ⚡ 즉시 실행 가이드

## 가장 빠른 방법

```bash
cd /root/rag_edu
./install.sh
python3 app.py
```

브라우저에서 `http://localhost:7860` 접속

## 단계별 실행

### 1️⃣ 테스트 (API 키 불필요)

```bash
python3 test_simple.py
```

**예상 출력:**
```
🧪 RAG 교육 챗봇 시스템 테스트

그래프 구조 테스트 ✅
상태 생성 테스트 ✅
도메인 데이터 테스트 ✅

🎉 모든 테스트 통과!
```

### 2️⃣ 앱 실행

```bash
python3 app.py
```

**예상 출력:**
```
==================================================
🚀 RAG 교육 챗봇 서버 시작
==================================================

Running on local URL:  http://127.0.0.1:7860
```

### 3️⃣ 질문하기

UI에서 시도:
- "RAG가 뭐야?"
- "Hybrid Search 구현하고 싶어"
- "프로덕션 배포 방법 알려줘"

## 🔍 디버깅 모드

Python 스크립트로 직접 실행:

```python
from src.graph import run_rag_education_bot

response = run_rag_education_bot("RAG 최적화 방법")
print(response)
```

## 📊 각 노드 출력 확인

```python
from src.graph import run_rag_education_bot_stream

for output in run_rag_education_bot_stream("질문"):
    print(f"\n{'='*50}")
    print(output)
```

## 🛠️ 문제 해결

### 문제: 모듈을 찾을 수 없음
```bash
pip3 install -r requirements.txt
```

### 문제: 포트 충돌
`app.py` 파일에서 `server_port=7860`을 다른 포트로 변경

### 문제: 권한 오류
```bash
chmod +x install.sh
```

## 📚 더 알아보기

- 빠른 시작: [QUICKSTART.md](QUICKSTART.md)
- 상세 설치: [SETUP.md](SETUP.md)
- 프로젝트 요약: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
- 설계 문서: [README.md](README.md)

## 💡 주요 파일

| 파일 | 설명 |
|------|------|
| `app.py` | Gradio UI 진입점 |
| `test_simple.py` | 구조 테스트 |
| `src/graph.py` | LangGraph 워크플로우 |
| `src/state.py` | 상태 정의 |
| `src/nodes/*.py` | 14개 처리 노드 |
| `src/utils/domain_data.py` | RAG 도메인 지식 |

---

**질문이나 문제가 있나요?** 이슈를 생성해주세요!

