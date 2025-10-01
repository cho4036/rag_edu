"""Gradio UI - RAG 교육 챗봇 인터페이스"""
import gradio as gr
import os
from dotenv import load_dotenv
from src.graph import run_rag_education_bot, run_rag_education_bot_stream

# 환경 변수 로드
load_dotenv()

# ============ UI 함수 ============

def chat_function(message, history):
    """
    채팅 인터페이스 함수
    
    Args:
        message: 사용자 입력 메시지
        history: 채팅 히스토리 [[user_msg, bot_msg], ...]
        
    Returns:
        봇 응답
    """
    if not message.strip():
        return "메시지를 입력해주세요."
    
    try:
        # RAG 교육 챗봇 실행
        response = run_rag_education_bot(message)
        return response
        
    except Exception as e:
        return f"오류가 발생했습니다: {str(e)}\n\n환경 변수(.env)를 확인해주세요."


def example_questions():
    """예제 질문들 - 다양한 분야"""
    return [
        # RAG
        "RAG를 구축하려면 무엇을 해야 해?",
        "Hybrid Search가 뭐야?",
        # Machine Learning
        "딥러닝을 처음 시작하는데 어떻게 배워야 해?",
        "Transformer 모델의 원리가 궁금해",
        # Backend
        "FastAPI로 REST API 서버 만들고 싶어",
        "데이터베이스 인덱싱 최적화 방법 알려줘",
        # DevOps
        "Kubernetes 배포 시작하는 방법",
        "CI/CD 파이프라인 구축하고 싶어",
        # Frontend
        "React 상태 관리 어떻게 해야 해?",
        # Data Science
        "데이터 분석 시작하려면 뭐부터 배워야 해?"
    ]


# ============ Gradio 인터페이스 구성 ============

def create_ui():
    """Gradio UI 생성"""
    
    # CSS 스타일
    custom_css = """
    .gradio-container {
        max-width: 1200px !important;
    }
    .chat-container {
        height: 600px !important;
    }
    """
    
    with gr.Blocks(
        title="RAG 교육 챗봇",
        theme=gr.themes.Soft(),
        css=custom_css
    ) as demo:
        
        gr.Markdown(
            """
            # 🎓 동적 분야 학습 챗봇
            
            **어떤 분야든 당신의 학습을 단계별로 도와드립니다!**
            
            이 챗봇은:
            - 🔎 질문에서 분야를 자동으로 감지합니다 (RAG, ML, Backend 등)
            - 🧠 해당 분야의 전문가로 동적 변신합니다
            - 📊 당신의 경험 수준을 자동으로 파악합니다
            - 🎯 맞춤형 학습 경로를 제공합니다
            - 🔍 모르는 개념을 자동으로 감지하고 설명합니다
            - 🛠️ 실전에 필요한 도구와 아키텍처를 추천합니다
            
            ---
            """
        )
        
        with gr.Row():
            with gr.Column(scale=2):
                # 채팅 인터페이스
                chatbot = gr.Chatbot(
                    label="대화",
                    height=500,
                    show_copy_button=True,
                    elem_classes=["chat-container"]
                )
                
                msg_input = gr.Textbox(
                    label="질문을 입력하세요",
                    placeholder="예: RAG를 구축하려면 무엇을 해야 해?",
                    lines=2
                )
                
                with gr.Row():
                    submit_btn = gr.Button("전송", variant="primary")
                    clear_btn = gr.Button("대화 초기화")
            
            with gr.Column(scale=1):
                gr.Markdown("### 💡 예제 질문")
                
                examples = example_questions()
                for example in examples:
                    example_btn = gr.Button(example, size="sm")
                    example_btn.click(
                        lambda x=example: x,
                        outputs=msg_input
                    )
                
                gr.Markdown(
                    """
                    ---
                    ### 📚 주요 기능
                    
                    1. **🔎 분야 자동 감지**
                       - 질문 분석으로 분야 파악
                       - 10개 이상 분야 지원
                    
                    2. **🧠 동적 전문가 변신**
                       - LLM으로 지식 자동 생성
                       - 분야별 맞춤 taxonomy
                    
                    3. **📊 자동 레벨 감지**
                       - 질문을 통해 경험 수준 파악
                    
                    4. **🎯 맞춤형 답변**
                       - 초보자부터 전문가까지
                    
                    5. **🔍 개념 갭 분석**
                       - 모르는 용어 자동 설명
                    
                    6. **🛠️ 실전 가이드**
                       - 단계별 체크리스트
                       - 도구 추천
                       - 트레이드오프 설명
                    
                    ---
                    
                    ### ⚙️ 설정 방법
                    
                    `.env` 파일에 API 키 설정:
                    ```
                    OPENAI_API_KEY=your_key
                    ```
                    
                    **API 키 없이도** 기본 기능 사용 가능!
                    """
                )
        
        gr.Markdown(
            """
            ---
            
            ### 🔧 기술 스택
            
            - **LangGraph**: 복잡한 워크플로우 관리
            - **Gradio**: 사용자 인터페이스  
            - **OpenAI GPT-4**: 동적 지식 생성
            - **Dynamic Domain System**: 어떤 분야든 전문가로 변신
            
            ### 🌟 지원 분야 (예시)
            
            RAG, ML/DL, Backend, Frontend, DevOps, Data Science, 
            Blockchain, Cloud, Cybersecurity, Mobile 등
            
            ---
            
            Made with ❤️ using LangGraph | **어떤 분야든 학습하세요!**
            """
        )
        
        # 이벤트 핸들러
        def respond(message, chat_history):
            """메시지 응답 처리"""
            bot_response = chat_function(message, chat_history)
            chat_history.append((message, bot_response))
            return "", chat_history
        
        # 전송 버튼 클릭
        submit_btn.click(
            respond,
            inputs=[msg_input, chatbot],
            outputs=[msg_input, chatbot]
        )
        
        # Enter 키로 전송
        msg_input.submit(
            respond,
            inputs=[msg_input, chatbot],
            outputs=[msg_input, chatbot]
        )
        
        # 초기화 버튼
        clear_btn.click(
            lambda: [],
            outputs=chatbot
        )
    
    return demo


# ============ 메인 실행 ============

if __name__ == "__main__":
    # API 키 체크
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️ 경고: OPENAI_API_KEY가 설정되지 않았습니다.")
        print("   .env 파일을 생성하고 API 키를 설정해주세요.")
        print()
    
    # UI 생성 및 실행
    demo = create_ui()
    
    print("=" * 50)
    print("🚀 RAG 교육 챗봇 서버 시작")
    print("=" * 50)
    print()
    
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )

