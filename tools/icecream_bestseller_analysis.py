#!/usr/bin/env python3
"""
🍨 아이스크림 베스트셀러 실시간 분석기
네이버 쇼핑 API로 아이스크림 카테고리 인기 순위 분석
"""

import requests
import json
import time
from datetime import datetime

def get_icecream_bestsellers():
    """아이스크림 베스트셀러 순위 분석"""
    client_id = "UP8PqJq_FpkcB63sEFH9"
    client_secret = "B7sXznX3pP"
    
    headers = {
        'X-Naver-Client-Id': client_id,
        'X-Naver-Client-Secret': client_secret
    }
    
    print("🍨 아이스크림 베스트셀러 실시간 분석")
    print("=" * 50)
    
    # 아이스크림 세부 카테고리들
    icecream_categories = [
        "바닐라아이스크림", "초콜릿아이스크림", "딸기아이스크림", 
        "민트초코", "쿠키앤크림", "럼레이즌",
        "젤라또", "소르베", "아이스바", "콘아이스크림",
        "하겐다즈", "베스킨라빈스", "나뚜루", "빙그레",
        "메로나", "붕어싸만코", "슈퍼콘", "돼지바"
    ]
    
    results = {}
    
    for category in icecream_categories:
        print(f"\n🔍 '{category}' 분석 중...")
        
        # 네이버 쇼핑 검색 API 호출
        url = "https://openapi.naver.com/v1/search/shop.json"
        params = {
            'query': category,
            'display': 20,
            'start': 1,
            'sort': 'count'  # 리뷰 많은 순 (인기도 반영)
        }
        
        try:
            response = requests.get(url, params=params, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                total_count = data.get('total', 0)
                items = data.get('items', [])
                
                # 가격 및 인기도 분석
                prices = []
                review_counts = []
                for item in items:
                    # 가격 정보
                    price = item.get('lprice', '')
                    if price and price.isdigit():
                        prices.append(int(price))
                    
                    # 리뷰/평점 정보는 title에서 추출 시도
                    title = item.get('title', '')
                    # 간단한 인기도 지표로 total_count 활용
                
                avg_price = sum(prices) / len(prices) if prices else 0
                
                # 인기도 점수 계산 (상품 수 + 평균 가격 고려)
                popularity_score = total_count
                if avg_price > 0:
                    # 가격대별 가중치 (합리적 가격대에 더 높은 점수)
                    if 1000 <= avg_price <= 10000:  # 적정 가격대
                        popularity_score *= 1.2
                    elif avg_price > 20000:  # 고가 제품
                        popularity_score *= 0.8
                
                results[category] = {
                    'total_products': total_count,
                    'avg_price': int(avg_price),
                    'popularity_score': popularity_score,
                    'price_range': f"{min(prices):,} ~ {max(prices):,}원" if prices else "가격 정보 없음",
                    'top_product': items[0].get('title', '').replace('<b>', '').replace('</b>', '') if items else '없음'
                }
                
                print(f"  📦 상품 수: {total_count:,}개")
                print(f"  💰 평균 가격: {int(avg_price):,}원")
                print(f"  🏆 대표 상품: {results[category]['top_product'][:50]}...")
                print(f"  📈 인기도 점수: {popularity_score:.1f}")
                
            else:
                print(f"  ❌ API 오류: {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ 에러 발생: {str(e)}")
        
        # API 호출 제한 고려
        time.sleep(0.1)
    
    return results

def analyze_seasonal_trends():
    """계절별 아이스크림 트렌드 분석"""
    print("\n🌞 여름철 아이스크림 트렌드 분석")
    print("=" * 50)
    
    # 여름철 인기 키워드들
    summer_trends = [
        "시원한아이스크림", "여름아이스크림", "빙수", "팥빙수",
        "과일아이스크림", "수박바", "아이스캔디", "냉동과일"
    ]
    
    client_id = "UP8PqJq_FpkcB63sEFH9"
    client_secret = "B7sXznX3pP"
    
    headers = {
        'X-Naver-Client-Id': client_id,
        'X-Naver-Client-Secret': client_secret
    }
    
    seasonal_results = {}
    
    for trend in summer_trends:
        print(f"\n🔥 '{trend}' 여름 트렌드 확인...")
        
        url = "https://openapi.naver.com/v1/search/shop.json"
        params = {
            'query': trend,
            'display': 5,
            'start': 1,
            'sort': 'date'  # 최신순
        }
        
        try:
            response = requests.get(url, params=params, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                total_count = data.get('total', 0)
                
                seasonal_results[trend] = total_count
                print(f"  📈 관련 상품: {total_count:,}개")
                
        except Exception as e:
            print(f"  ❌ 에러: {str(e)}")
        
        time.sleep(0.1)
    
    return seasonal_results

def generate_roulette_recommendations(results, seasonal_results):
    """룰렛용 추천 데이터 생성"""
    print("\n🎯 WhatToEat 룰렛 추천 데이터 생성")
    print("=" * 50)
    
    # 인기도 기준 정렬
    sorted_results = sorted(results.items(), key=lambda x: x[1]['popularity_score'], reverse=True)
    
    roulette_data = []
    
    print("🏆 아이스크림 인기 순위 TOP 10:")
    for i, (category, data) in enumerate(sorted_results[:10], 1):
        trend_icon = "🔥" if i <= 3 else "⭐" if i <= 7 else "👍"
        
        roulette_item = {
            'rank': i,
            'name': category,
            'popularity_score': data['popularity_score'],
            'avg_price': data['avg_price'],
            'total_products': data['total_products'],
            'trend_level': 'hot' if i <= 3 else 'popular' if i <= 7 else 'good'
        }
        
        roulette_data.append(roulette_item)
        
        print(f"  {i:2d}. {trend_icon} {category}")
        print(f"      📈 인기도: {data['popularity_score']:.1f} | 💰 평균: {data['avg_price']:,}원 | 📦 상품: {data['total_products']:,}개")
    
    # 계절 트렌드 반영
    print(f"\n🌞 여름철 특별 추천:")
    sorted_seasonal = sorted(seasonal_results.items(), key=lambda x: x[1], reverse=True)
    for i, (trend, count) in enumerate(sorted_seasonal[:5], 1):
        print(f"  {i}. {trend}: {count:,}개 상품")
    
    return roulette_data

if __name__ == "__main__":
    print("🎯 아이스크림 베스트셀러 분석 시작!")
    print(f"📅 분석 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 1. 아이스크림 베스트셀러 분석
    results = get_icecream_bestsellers()
    
    # 2. 계절 트렌드 분석
    seasonal_results = analyze_seasonal_trends()
    
    # 3. 룰렛용 데이터 생성
    roulette_data = generate_roulette_recommendations(results, seasonal_results)
    
    print("\n🎉 분석 완료! WhatToEat 아이스크림 룰렛 데이터 준비됨!")
    print("💡 이 데이터를 룰렛에 적용하면 실시간 인기 아이스크림 추천 가능!")