"""간단한 테스트 스크립트 - API 키 없이도 그래프 구조 확인 가능"""
import sys
sys.path.append('/root/rag_edu')

from src.graph import create_graph
from src.state import create_initial_state


def test_graph_structure():
    """그래프 구조 테스트"""
    print("=" * 50)
    print("그래프 구조 테스트")
    print("=" * 50)
    
    try:
        # 그래프 생성
        app = create_graph()
        print("✅ 그래프 생성 성공!")
        
        # 그래프 정보 출력
        print("\n노드 목록:")
        nodes = [
            "domain_bootstrap", "user_signals", "coldstart_probe",
            "infer_level", "adaptive_diagnostic", "intent_detect",
            "taxonomy_map", "plan_answer", "tool_advisors",
            "gap_mining", "compose_answer", "quality_gate",
            "memory_write", "deliver"
        ]
        for i, node in enumerate(nodes, 1):
            print(f"  {i:2d}. {node}")
        
        print(f"\n총 {len(nodes)}개 노드 구성")
        
        return True
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_state_creation():
    """상태 생성 테스트"""
    print("\n" + "=" * 50)
    print("상태 생성 테스트")
    print("=" * 50)
    
    try:
        # 초기 상태 생성
        state = create_initial_state("테스트 질문입니다")
        
        print("✅ 상태 생성 성공!")
        print(f"\n사용자 메시지: {state['user_message']}")
        print(f"사용자 ID: {state['user'].id}")
        print(f"언어: {state['user'].lang}")
        print(f"현재 단계: {state['current_step']}")
        
        return True
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_domain_data():
    """도메인 데이터 로드 테스트"""
    print("\n" + "=" * 50)
    print("도메인 데이터 테스트")
    print("=" * 50)
    
    try:
        from src.utils.domain_data import get_domain_pack
        
        domain_pack = get_domain_pack()
        
        print("✅ 도메인 팩 로드 성공!")
        print(f"\nTaxonomy 개념: {len(domain_pack['taxonomy'])}개")
        print(f"Glossary 용어: {len(domain_pack['glossary'])}개")
        print(f"Question Bank: {len(domain_pack['question_bank'])}개")
        print(f"Tool Recipes: {len(domain_pack['tool_recipes'])}개")
        
        print("\n주요 개념:")
        for concept in domain_pack['taxonomy'][:5]:
            print(f"  - {concept['name']} (중요도: {concept['importance']}/10)")
        
        print("\n주요 용어:")
        for i, term in enumerate(list(domain_pack['glossary'].keys())[:5], 1):
            print(f"  {i}. {term}")
        
        return True
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n🧪 RAG 교육 챗봇 시스템 테스트\n")
    
    # 테스트 실행
    results = []
    results.append(("그래프 구조", test_graph_structure()))
    results.append(("상태 생성", test_state_creation()))
    results.append(("도메인 데이터", test_domain_data()))
    
    # 결과 요약
    print("\n" + "=" * 50)
    print("테스트 결과 요약")
    print("=" * 50)
    
    for test_name, result in results:
        status = "✅ 성공" if result else "❌ 실패"
        print(f"{test_name:20s}: {status}")
    
    total = len(results)
    passed = sum(1 for _, r in results if r)
    
    print(f"\n총 {total}개 테스트 중 {passed}개 통과")
    
    if passed == total:
        print("\n🎉 모든 테스트 통과!")
        print("\n다음 명령으로 앱을 실행할 수 있습니다:")
        print("  python app.py")
    else:
        print("\n⚠️ 일부 테스트 실패. 오류를 확인해주세요.")

