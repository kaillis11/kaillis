#!/usr/bin/env python3
"""
🏆 범용 랭킹 시스템 데모 버전
API 연결 없이 실제 구조와 결과를 보여주는 데모

실제 네이버 API 연동시 바로 작동할 수 있는 완전한 구조
"""

import argparse
from datetime import datetime
from typing import Dict, List, Tuple

class DemoRankingSystem:
    def __init__(self):
        # 실제 시장 데이터를 기반으로 한 샘플 데이터
        self.sample_data = {
            "아이스크림": {
                "메로나": {"total_products": 15420, "avg_price": 1500, "top_product": "빙그레 메로나 아이스크림"},
                "하겐다즈": {"total_products": 8750, "avg_price": 5500, "top_product": "하겐다즈 바닐라 아이스크림"},
                "붕어싸만코": {"total_products": 12300, "avg_price": 2000, "top_product": "삼립 붕어싸만코"},
                "민트초코": {"total_products": 6800, "avg_price": 3200, "top_product": "민트초콜릿 아이스크림"},
                "슈퍼콘": {"total_products": 9500, "avg_price": 2200, "top_product": "롯데 슈퍼콘"},
                "돼지바": {"total_products": 11200, "avg_price": 1400, "top_product": "롯데 돼지바"},
                "베스킨라빈스": {"total_products": 5600, "avg_price": 4800, "top_product": "베스킨라빈스 31 아이스크림"},
                "비비빅": {"total_products": 7300, "avg_price": 1800, "top_product": "롯데 비비빅"},
                "젤라또": {"total_products": 3200, "avg_price": 6500, "top_product": "이탈리안 젤라또"},
                "쿠키오": {"total_products": 8100, "avg_price": 2100, "top_product": "해태 쿠키오"}
            },
            "케이크": {
                "생크림케이크": {"total_products": 12500, "avg_price": 25000, "top_product": "생크림 생일케이크"},
                "초콜릿케이크": {"total_products": 9800, "avg_price": 28000, "top_product": "초콜릿 생일케이크"},
                "치즈케이크": {"total_products": 8900, "avg_price": 32000, "top_product": "뉴욕 치즈케이크"},
                "티라미수": {"total_products": 6700, "avg_price": 35000, "top_product": "이탈리안 티라미수"},
                "마카롱": {"total_products": 15600, "avg_price": 18000, "top_product": "프랑스 마카롱 세트"},
                "롤케이크": {"total_products": 7800, "avg_price": 22000, "top_product": "딸기 롤케이크"},
                "파운드케이크": {"total_products": 5400, "avg_price": 15000, "top_product": "버터 파운드케이크"},
                "브라우니": {"total_products": 9200, "avg_price": 12000, "top_product": "초콜릿 브라우니"},
                "타르트": {"total_products": 4600, "avg_price": 38000, "top_product": "과일 타르트"},
                "무스케이크": {"total_products": 3800, "avg_price": 42000, "top_product": "초콜릿 무스케이크"}
            },
            "음료": {
                "콜라": {"total_products": 25600, "avg_price": 1200, "top_product": "코카콜라 500ml"},
                "사이다": {"total_products": 18900, "avg_price": 1100, "top_product": "칠성사이다 500ml"},
                "커피": {"total_products": 42300, "avg_price": 3500, "top_product": "스타벅스 아메리카노"},
                "아메리카노": {"total_products": 38900, "avg_price": 3800, "top_product": "투썸 아메리카노"},
                "라떼": {"total_products": 28700, "avg_price": 4500, "top_product": "스타벅스 카페라떼"},
                "차": {"total_products": 15800, "avg_price": 2800, "top_product": "녹차 티백"},
                "주스": {"total_products": 22400, "avg_price": 2200, "top_product": "오렌지 주스"},
                "물": {"total_products": 35600, "avg_price": 800, "top_product": "삼다수 2L"},
                "이온음료": {"total_products": 12600, "avg_price": 1400, "top_product": "포카리스웨트"},
                "탄산수": {"total_products": 8900, "avg_price": 1600, "top_product": "페리에 탄산수"}
            },
            "치킨": {
                "후라이드": {"total_products": 18500, "avg_price": 18000, "top_product": "교촌치킨 후라이드"},
                "양념치킨": {"total_products": 22300, "avg_price": 20000, "top_product": "BBQ 양념치킨"},
                "간장치킨": {"total_products": 8900, "avg_price": 21000, "top_product": "교촌치킨 간장치킨"},
                "마늘치킨": {"total_products": 6700, "avg_price": 19000, "top_product": "네네치킨 마늘치킨"},
                "허니머스타드": {"total_products": 5800, "avg_price": 22000, "top_product": "허니머스타드 치킨"},
                "치킨너겟": {"total_products": 15600, "avg_price": 12000, "top_product": "맥도날드 치킨너겟"},
                "핫윙": {"total_products": 7200, "avg_price": 16000, "top_product": "KFC 핫윙"},
                "순살치킨": {"total_products": 12400, "avg_price": 23000, "top_product": "굽네치킨 순살"},
                "반반치킨": {"total_products": 9800, "avg_price": 24000, "top_product": "후라이드+양념 반반"},
                "매운치킨": {"total_products": 11200, "avg_price": 21000, "top_product": "불닭치킨"}
            }
        }
    
    def calculate_sales_ranking(self, data: Dict) -> List[Tuple[str, Dict]]:
        """판매량 기준 순위 계산"""
        # 상품 수(판매량 추정치) 기준 정렬
        sales_ranking = sorted(
            data.items(), 
            key=lambda x: x[1]['total_products'], 
            reverse=True
        )
        return sales_ranking
    
    def calculate_revenue_ranking(self, data: Dict) -> List[Tuple[str, Dict]]:
        """매출 기준 순위 계산"""
        # 추정 매출액 계산 후 정렬
        revenue_data = {}
        for product, info in data.items():
            revenue_data[product] = {
                **info,
                'estimated_revenue': info['total_products'] * info['avg_price']
            }
        
        revenue_ranking = sorted(
            revenue_data.items(), 
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
            popularity = "🔥🔥🔥" if i <= 3 else "🔥🔥" if i <= 6 else "🔥"
            
            print(f"{rank_icon} {product} {popularity}")
            print(f"    📦 상품 수: {data['total_products']:,}개")
            print(f"    💰 평균 가격: {data['avg_price']:,}원")
            print(f"    🏆 대표 상품: {data['top_product']}")
            print()
    
    def display_revenue_ranking(self, category: str, ranking: List[Tuple[str, Dict]]) -> None:
        """매출 순위 출력"""
        print(f"\n💰 {category} 매출 순위 TOP {len(ranking)}")
        print("=" * 60)
        print("📊 기준: 추정 매출액 (상품 수 × 평균 가격)")
        print()
        
        for i, (product, data) in enumerate(ranking, 1):
            rank_icon = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i:2d}."
            popularity = "💰💰💰" if i <= 3 else "💰💰" if i <= 6 else "💰"
            
            revenue = data.get('estimated_revenue', data['total_products'] * data['avg_price'])
            
            print(f"{rank_icon} {product} {popularity}")
            print(f"    💵 추정 매출: {revenue:,}원")
            print(f"    📦 상품 수: {data['total_products']:,}개 × 💰 평균 가격: {data['avg_price']:,}원")
            print(f"    🏆 대표 상품: {data['top_product']}")
            print()
    
    def analyze_category(self, category: str, mode: str = "both") -> Dict:
        """카테고리 종합 분석"""
        print(f"🎯 {category} 카테고리 종합 분석 (데모 모드)")
        print(f"📅 분석 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🔧 분석 모드: {mode}")
        print()
        
        if category not in self.sample_data:
            print(f"❌ '{category}' 카테고리 데이터가 없습니다.")
            print(f"💡 사용 가능한 카테고리: {', '.join(self.sample_data.keys())}")
            return {}
        
        data = self.sample_data[category]
        result = {
            'category': category,
            'mode': mode,
            'timestamp': datetime.now().isoformat()
        }
        
        # 모드별 분석
        if mode in ["sales", "both"]:
            sales_ranking = self.calculate_sales_ranking(data)
            result['sales_ranking'] = sales_ranking
            self.display_sales_ranking(category, sales_ranking)
        
        if mode in ["revenue", "both"]:
            revenue_ranking = self.calculate_revenue_ranking(data)
            result['revenue_ranking'] = revenue_ranking
            self.display_revenue_ranking(category, revenue_ranking)
        
        # 순위 비교 분석
        if mode == "both":
            self.compare_rankings(category, result['sales_ranking'], result['revenue_ranking'])
        
        return result
    
    def compare_rankings(self, category: str, sales_ranking: List, revenue_ranking: List) -> None:
        """판매량 vs 매출 순위 비교"""
        print(f"\n📊 {category} 판매량 vs 매출 순위 비교")
        print("=" * 60)
        
        sales_dict = {product: i+1 for i, (product, _) in enumerate(sales_ranking)}
        revenue_dict = {product: i+1 for i, (product, _) in enumerate(revenue_ranking)}
        
        print("🔍 순위 변동 분석:")
        print()
        
        for product in sales_dict.keys():
            sales_rank = sales_dict[product]
            revenue_rank = revenue_dict[product]
            rank_diff = sales_rank - revenue_rank
            
            if rank_diff > 0:
                change_icon = f"📈 +{rank_diff}"
                analysis = "매출에서 순위 상승 (고가 제품)"
            elif rank_diff < 0:
                change_icon = f"📉 {rank_diff}"
                analysis = "매출에서 순위 하락 (저가 제품)"
            else:
                change_icon = "➡️ 0"
                analysis = "순위 동일"
            
            print(f"• {product}: 판매량 {sales_rank}위 → 매출 {revenue_rank}위 {change_icon}")
            print(f"  💡 {analysis}")
            print()

def main():
    """메인 실행 함수"""
    parser = argparse.ArgumentParser(description='범용 랭킹 시스템 데모')
    parser.add_argument('category', nargs='?', default='아이스크림', 
                       help='분석할 카테고리 (아이스크림, 케이크, 음료, 치킨)')
    parser.add_argument('--mode', choices=['sales', 'revenue', 'both'], default='both', 
                       help='분석 모드: sales(판매량), revenue(매출), both(둘다)')
    
    args = parser.parse_args()
    
    # 랭킹 시스템 초기화
    ranking_system = DemoRankingSystem()
    
    # 분석 실행
    result = ranking_system.analyze_category(args.category, args.mode)
    
    print("\n🎉 데모 분석 완료!")
    print(f"💡 실제 API 연동시 동일한 구조로 실시간 데이터 분석 가능!")
    print(f"🚀 {args.category} 카테고리의 {args.mode} 모드 분석이 완료되었습니다!")

if __name__ == "__main__":
    main()