#!/usr/bin/env python3
"""
🏆 범용 랭킹 시스템 (Universal Ranking System)
모든 카테고리에 대해 판매량/매출 순위를 분석하는 범용 도구

사용법:
python3 universal_ranking_system.py "아이스크림" --mode sales
python3 universal_ranking_system.py "케이크" --mode revenue
python3 universal_ranking_system.py "음료" --mode both
"""

import requests
import json
import time
import argparse
from datetime import datetime
from typing import Dict, List, Tuple, Optional

class UniversalRankingSystem:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = "https://openapi.naver.com"
        
        # 카테고리별 기본 키워드 데이터베이스
        self.category_keywords = {
            "아이스크림": ["메로나", "하겐다즈", "붕어싸만코", "민트초코", "슈퍼콘", "돼지바", "베스킨라빈스", "비비빅", "젤라또", "쿠키오"],
            "케이크": ["생크림케이크", "초콜릿케이크", "치즈케이크", "티라미수", "마카롱", "롤케이크", "파운드케이크", "브라우니", "타르트", "무스케이크"],
            "음료": ["콜라", "사이다", "커피", "아메리카노", "라떼", "차", "주스", "물", "이온음료", "탄산수"],
            "피자": ["페퍼로니", "불고기피자", "마르게리타", "하와이안", "콤비네이션", "고구마피자", "치킨피자", "씨푸드피자", "베이컨피자", "채식피자"],
            "치킨": ["후라이드", "양념치킨", "간장치킨", "마늘치킨", "허니머스타드", "치킨너겟", "핫윙", "순살치킨", "반반치킨", "매운치킨"],
            "햄버거": ["빅맥", "와퍼", "치즈버거", "불고기버거", "치킨버거", "베이컨버거", "새우버거", "피쉬버거", "더블버거", "채식버거"],
            "라면": ["신라면", "진라면", "너구리", "짜파게티", "불닭볶음면", "안성탕면", "삼양라면", "오징어짬뽕", "컵라면", "쌀국수"]
        }
    
    def get_headers(self) -> Dict[str, str]:
        """API 헤더 생성"""
        return {
            'X-Naver-Client-Id': self.client_id,
            'X-Naver-Client-Secret': self.client_secret
        }
    
    def search_category_products(self, category: str, keywords: List[str] = None) -> Dict:
        """카테고리별 상품 검색"""
        if keywords is None:
            keywords = self.category_keywords.get(category, [category])
        
        print(f"🔍 '{category}' 카테고리 분석 시작...")
        print(f"📝 검색 키워드: {len(keywords)}개")
        
        results = {}
        
        for keyword in keywords:
            print(f"  🔎 '{keyword}' 검색 중...")
            
            url = f"{self.base_url}/v1/search/shop.json"
            params = {
                'query': keyword,
                'display': 20,
                'start': 1,
                'sort': 'sim'  # 정확도순
            }
            
            try:
                response = requests.get(url, params=params, headers=self.get_headers())
                
                if response.status_code == 200:
                    data = response.json()
                    
                    total_count = data.get('total', 0)
                    items = data.get('items', [])
                    
                    # 가격 데이터 수집
                    prices = []
                    for item in items:
                        price = item.get('lprice', '')
                        if price and price.isdigit():
                            prices.append(int(price))
                    
                    avg_price = sum(prices) / len(prices) if prices else 0
                    min_price = min(prices) if prices else 0
                    max_price = max(prices) if prices else 0
                    
                    results[keyword] = {
                        'total_products': total_count,
                        'avg_price': int(avg_price),
                        'min_price': min_price,
                        'max_price': max_price,
                        'price_range': f"{min_price:,}~{max_price:,}원" if prices else "가격 정보 없음",
                        'estimated_revenue': total_count * avg_price if avg_price > 0 else 0,
                        'top_product': items[0].get('title', '').replace('<b>', '').replace('</b>', '') if items else '없음'
                    }
                    
                    print(f"    ✅ 상품 수: {total_count:,}개 | 평균 가격: {int(avg_price):,}원")
                    
                else:
                    print(f"    ❌ API 오류: {response.status_code}")
                    results[keyword] = {'error': f"API 오류: {response.status_code}"}
                    
            except Exception as e:
                print(f"    ❌ 에러: {str(e)}")
                results[keyword] = {'error': str(e)}
            
            # API 호출 제한 고려
            time.sleep(0.1)
        
        return results
    
    def calculate_sales_ranking(self, results: Dict) -> List[Tuple[str, Dict]]:
        """판매량 기준 순위 계산"""
        valid_results = {k: v for k, v in results.items() if 'error' not in v}
        
        # 상품 수(판매량 추정치) 기준 정렬
        sales_ranking = sorted(
            valid_results.items(), 
            key=lambda x: x[1]['total_products'], 
            reverse=True
        )
        
        return sales_ranking
    
    def calculate_revenue_ranking(self, results: Dict) -> List[Tuple[str, Dict]]:
        """매출 기준 순위 계산"""
        valid_results = {k: v for k, v in results.items() if 'error' not in v and v['estimated_revenue'] > 0}
        
        # 추정 매출액 기준 정렬
        revenue_ranking = sorted(
            valid_results.items(), 
            key=lambda x: x[1]['estimated_revenue'], 
            reverse=True
        )
        
        return revenue_ranking
    
    def display_sales_ranking(self, category: str, ranking: List[Tuple[str, Dict]]) -> None:
        """판매량 순위 출력"""
        print(f"\n🏆 {category} 판매량 순위 TOP {len(ranking)}")
        print("=" * 60)
        print("📊 기준: 네이버 쇼핑 검색 결과 상품 수 (판매량 추정)")
        print()
        
        for i, (product, data) in enumerate(ranking, 1):
            rank_icon = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i:2d}."
            
            print(f"{rank_icon} {product}")
            print(f"    📦 상품 수: {data['total_products']:,}개")
            print(f"    💰 평균 가격: {data['avg_price']:,}원")
            print(f"    💸 가격 범위: {data['price_range']}")
            print(f"    🏆 대표 상품: {data['top_product'][:50]}...")
            print()
    
    def display_revenue_ranking(self, category: str, ranking: List[Tuple[str, Dict]]) -> None:
        """매출 순위 출력"""
        print(f"\n💰 {category} 매출 순위 TOP {len(ranking)}")
        print("=" * 60)
        print("📊 기준: 추정 매출액 (상품 수 × 평균 가격)")
        print()
        
        for i, (product, data) in enumerate(ranking, 1):
            rank_icon = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i:2d}."
            
            print(f"{rank_icon} {product}")
            print(f"    💵 추정 매출: {data['estimated_revenue']:,}원")
            print(f"    📦 상품 수: {data['total_products']:,}개")
            print(f"    💰 평균 가격: {data['avg_price']:,}원")
            print(f"    🏆 대표 상품: {data['top_product'][:50]}...")
            print()
    
    def analyze_category(self, category: str, mode: str = "both", custom_keywords: List[str] = None) -> Dict:
        """카테고리 종합 분석"""
        print(f"🎯 {category} 카테고리 종합 분석")
        print(f"📅 분석 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🔧 분석 모드: {mode}")
        print()
        
        # 1. 상품 검색
        keywords = custom_keywords if custom_keywords else self.category_keywords.get(category, [category])
        results = self.search_category_products(category, keywords)
        
        analysis_result = {
            'category': category,
            'mode': mode,
            'raw_data': results,
            'timestamp': datetime.now().isoformat()
        }
        
        # 2. 모드별 분석
        if mode in ["sales", "both"]:
            sales_ranking = self.calculate_sales_ranking(results)
            analysis_result['sales_ranking'] = sales_ranking
            self.display_sales_ranking(category, sales_ranking)
        
        if mode in ["revenue", "both"]:
            revenue_ranking = self.calculate_revenue_ranking(results)
            analysis_result['revenue_ranking'] = revenue_ranking
            self.display_revenue_ranking(category, revenue_ranking)
        
        # 3. 요약 통계
        self.display_category_summary(category, results)
        
        return analysis_result
    
    def display_category_summary(self, category: str, results: Dict) -> None:
        """카테고리 요약 통계"""
        valid_results = {k: v for k, v in results.items() if 'error' not in v}
        
        if not valid_results:
            print(f"❌ {category} 카테고리 분석 실패: 유효한 데이터 없음")
            return
        
        total_products = sum(data['total_products'] for data in valid_results.values())
        total_revenue = sum(data['estimated_revenue'] for data in valid_results.values())
        avg_price = sum(data['avg_price'] for data in valid_results.values()) / len(valid_results)
        
        print(f"\n📊 {category} 카테고리 요약 통계")
        print("=" * 60)
        print(f"📝 분석 대상: {len(valid_results)}개 상품")
        print(f"📦 총 상품 수: {total_products:,}개")
        print(f"💰 총 추정 매출: {total_revenue:,}원")
        print(f"💵 평균 단가: {int(avg_price):,}원")
        print(f"🏪 상품 다양성: {'높음' if len(valid_results) >= 8 else '보통' if len(valid_results) >= 5 else '낮음'}")

def main():
    """메인 실행 함수"""
    parser = argparse.ArgumentParser(description='범용 랭킹 시스템')
    parser.add_argument('category', help='분석할 카테고리 (예: 아이스크림, 케이크, 음료)')
    parser.add_argument('--mode', choices=['sales', 'revenue', 'both'], default='both', 
                       help='분석 모드: sales(판매량), revenue(매출), both(둘다)')
    parser.add_argument('--keywords', nargs='*', help='사용자 정의 키워드 목록')
    
    args = parser.parse_args()
    
    # API 키 설정
    client_id = "UP8PqJq_FpkcB63sEFH9"
    client_secret = "B7sXznX3pP"
    
    # 랭킹 시스템 초기화
    ranking_system = UniversalRankingSystem(client_id, client_secret)
    
    # 분석 실행
    result = ranking_system.analyze_category(
        category=args.category,
        mode=args.mode,
        custom_keywords=args.keywords
    )
    
    print("\n🎉 분석 완료!")
    print(f"💡 {args.category} 카테고리의 {args.mode} 순위 분석이 완료되었습니다!")

if __name__ == "__main__":
    # 기본 테스트 (인수 없이 실행시)
    import sys
    if len(sys.argv) == 1:
        print("🎯 범용 랭킹 시스템 테스트 모드")
        print()
        
        client_id = "UP8PqJq_FpkcB63sEFH9"
        client_secret = "B7sXznX3pP"
        ranking_system = UniversalRankingSystem(client_id, client_secret)
        
        # 아이스크림 테스트
        ranking_system.analyze_category("아이스크림", "both")
    else:
        main()