#!/bin/bash

echo "=================================="
echo "RAG 교육 챗봇 설치 스크립트"
echo "=================================="
echo ""

# Python 버전 확인
echo "Python 버전 확인..."
python3 --version

echo ""
echo "의존성 패키지 설치 중..."
pip3 install -r requirements.txt

echo ""
echo "=================================="
echo "✅ 설치 완료!"
echo "=================================="
echo ""
echo "다음 단계:"
echo "1. .env 파일을 생성하고 OPENAI_API_KEY를 설정하세요"
echo "   cp .env.example .env"
echo ""
echo "2. 테스트 실행:"
echo "   python3 test_simple.py"
echo ""
echo "3. 앱 실행:"
echo "   python3 app.py"
echo ""

