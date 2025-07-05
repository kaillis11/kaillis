#!/usr/bin/env python3
"""
실제 디저트 API 테스트 - 바로 실행 가능!
"""

import requests
import json
import time

def test_naver_search_api():
    """네이버 쇼핑 검색 API 테스트"""
    client_id = "UP8PqJq_FpkcB63sEFH9"
    client_secret = "B7sXznX3pP"
    
    headers = {
        'X-Naver-Client-Id': client_id,
        'X-Naver-Client-Secret': client_secret
    }
    
    # 테스트할 디저트 키워드
    test_desserts = ["마카롱", "크로플", "케이크", "아이스크림", "티라미수"]
    
    results = {}
    
    print("🍰 네이버 쇼핑 API 디저트 인기도 테스트")
    print("=" * 50)
    
    for dessert in test_desserts:
        print(f"\n🔍 '{dessert}' 검색 중...")
        
        # 네이버 쇼핑 검색 API 호출
        url = "https://openapi.naver.com/v1/search/shop.json"
        params = {
            'query': dessert,
            'display': 10,
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
                
                results[dessert] = {
                    'total_products': total_count,
                    'avg_price': int(avg_price),
                    'price_range': f"{min(prices):,} ~ {max(prices):,}원" if prices else "가격 정보 없음",
                    'top_products': [item.get('title', '').replace('<b>', '').replace('</b>', '') for item in items[:3]]
                }
                
                print(f"  ✅ 상품 수: {total_count:,}개")
                print(f"  💰 평균 가격: {int(avg_price):,}원")
                print(f"  🏆 인기 상품: {results[dessert]['top_products'][0] if results[dessert]['top_products'] else '없음'}")
                
            else:
                print(f"  ❌ API 오류: {response.status_code}")
                print(f"  📄 응답: {response.text}")
                
        except Exception as e:
            print(f"  ❌ 에러 발생: {str(e)}")
        
        # API 호출 제한 고려 (초당 10회 제한)
        time.sleep(0.1)
    
    # 결과 정리
    print("\n" + "=" * 50)
    print("📊 디저트 인기도 순위 (상품 수 기준)")
    print("=" * 50)
    
    # 상품 수로 정렬
    sorted_desserts = sorted(results.items(), key=lambda x: x[1]['total_products'], reverse=True)
    
    for i, (dessert, data) in enumerate(sorted_desserts, 1):
        print(f"{i}. {dessert}")
        print(f"   📦 상품 수: {data['total_products']:,}개")
        print(f"   💰 평균 가격: {data['avg_price']:,}원")
        print(f"   💸 가격 범위: {data['price_range']}")
        print()
    
    return results

def get_trending_dessert_keywords():
    """2024년 트렌딩 디저트 키워드 추가 분석"""
    trending_keywords = [
        "크로플", "말차디저트", "비건디저트", "수제쿠키", "홈베이킹키트"
    ]
    
    client_id = "UP8PqJq_FpkcB63sEFH9"
    client_secret = "B7sXznX3pP"
    
    headers = {
        'X-Naver-Client-Id': client_id,
        'X-Naver-Client-Secret': client_secret
    }
    
    print("\n🔥 2024년 트렌딩 디저트 키워드 분석")
    print("=" * 50)
    
    trending_results = {}
    
    for keyword in trending_keywords:
        print(f"\n🚀 '{keyword}' 트렌드 분석...")
        
        url = "https://openapi.naver.com/v1/search/shop.json"
        params = {
            'query': keyword,
            'display': 5,
            'start': 1,
            'sort': 'date'  # 최신순
        }
        
        try:
            response = requests.get(url, params=params, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                total_count = data.get('total', 0)
                
                trending_results[keyword] = total_count
                print(f"  📈 상품 수: {total_count:,}개")
                
        except Exception as e:
            print(f"  ❌ 에러: {str(e)}")
        
        time.sleep(0.1)
    
    # 트렌딩 순위
    print("\n🏆 트렌딩 디저트 순위:")
    sorted_trending = sorted(trending_results.items(), key=lambda x: x[1], reverse=True)
    for i, (keyword, count) in enumerate(sorted_trending, 1):
        print(f"  {i}. {keyword}: {count:,}개 상품")
    
    return trending_results

if __name__ == "__main__":
    print("🎯 네이버 쇼핑 API 실제 테스트 시작!")
    print("📊 API 사용량: 0/1000 (데이터랩 쇼핑인사이트)")
    print()
    
    # 기본 디저트 인기도 테스트
    basic_results = test_naver_search_api()
    
    # 트렌딩 키워드 분석
    trending_results = get_trending_dessert_keywords()
    
    print("\n🎉 테스트 완료! WhatToEat 룰렛에 적용할 데이터 확보!")