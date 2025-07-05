#!/usr/bin/env python3
"""
진짜 아이스크림 TOP 10 순위 분석
실제 네이버 쇼핑 API 사용
"""

import requests
import time

def get_real_icecream_ranking():
    """실제 아이스크림 순위 분석"""
    client_id = "UP8PqJq_FpkcB63sEFH9"
    client_secret = "B7sXznX3pP"
    
    headers = {
        'X-Naver-Client-Id': client_id,
        'X-Naver-Client-Secret': client_secret
    }
    
    # 아이스크림 키워드들
    icecream_keywords = [
        "메로나", "하겐다즈", "붕어싸만코", "민트초코", "슈퍼콘", 
        "돼지바", "베스킨라빈스", "비비빅", "젤라또", "쿠키오",
        "빵또아", "디핀다트", "설레임", "와일드바디", "누가바"
    ]
    
    print("🍨 실제 아이스크림 TOP 순위 분석")
    print("=" * 50)
    
    results = {}
    
    for keyword in icecream_keywords:
        print(f"🔍 '{keyword}' 분석 중...")
        
        url = "https://openapi.naver.com/v1/search/shop.json"
        params = {
            'query': keyword,
            'display': 20,
            'start': 1,
            'sort': 'sim'  # 정확도순
        }
        
        try:
            response = requests.get(url, params=params, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                total_count = data.get('total', 0)
                items = data.get('items', [])
                
                # 가격 분석
                prices = []
                for item in items:
                    price = item.get('lprice', '')
                    if price and price.isdigit():
                        prices.append(int(price))
                
                avg_price = sum(prices) / len(prices) if prices else 0
                estimated_revenue = total_count * avg_price if avg_price > 0 else 0
                
                results[keyword] = {
                    'total_products': total_count,
                    'avg_price': int(avg_price),
                    'estimated_revenue': estimated_revenue,
                    'top_product': items[0].get('title', '').replace('<b>', '').replace('</b>', '') if items else '없음'
                }
                
                print(f"  ✅ 상품 수: {total_count:,}개 | 평균 가격: {int(avg_price):,}원")
                
            else:
                print(f"  ❌ API 오류: {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ 에러: {str(e)}")
        
        # API 호출 제한 고려
        time.sleep(0.1)
    
    return results

def display_rankings(results):
    """순위 표시"""
    valid_results = {k: v for k, v in results.items() if v.get('total_products', 0) > 0}
    
    # 판매량 순위
    sales_ranking = sorted(valid_results.items(), key=lambda x: x[1]['total_products'], reverse=True)
    
    print(f"\n🏆 아이스크림 판매량 순위 TOP {len(sales_ranking)}")
    print("=" * 60)
    
    for i, (product, data) in enumerate(sales_ranking, 1):
        rank_icon = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i:2d}."
        
        print(f"{rank_icon} {product}")
        print(f"    📦 상품 수: {data['total_products']:,}개")
        print(f"    💰 평균 가격: {data['avg_price']:,}원")
        print(f"    🏆 대표 상품: {data['top_product'][:50]}...")
        print()
    
    # 매출 순위
    revenue_ranking = sorted(valid_results.items(), key=lambda x: x[1]['estimated_revenue'], reverse=True)
    
    print(f"\n💰 아이스크림 매출 순위 TOP {len(revenue_ranking)}")
    print("=" * 60)
    
    for i, (product, data) in enumerate(revenue_ranking, 1):
        rank_icon = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i:2d}."
        
        print(f"{rank_icon} {product}")
        print(f"    💵 추정 매출: {data['estimated_revenue']:,.0f}원")
        print(f"    📦 상품 수: {data['total_products']:,}개 × 💰 평균 가격: {data['avg_price']:,}원")
        print(f"    🏆 대표 상품: {data['top_product'][:50]}...")
        print()
    
    return sales_ranking, revenue_ranking

if __name__ == "__main__":
    print("🎯 진짜 아이스크림 순위 분석 시작!")
    print("📊 실제 네이버 쇼핑 API 데이터 사용")
    print()
    
    # 실제 데이터 수집
    results = get_real_icecream_ranking()
    
    # 순위 표시
    sales_ranking, revenue_ranking = display_rankings(results)
    
    print("\n🎉 실제 데이터 분석 완료!")
    print("💡 이제 진짜 순위를 WhatToEat 룰렛에 적용 가능!")