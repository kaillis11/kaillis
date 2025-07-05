#!/usr/bin/env python3
"""
네이버 쇼핑 API 테스트 스크립트
목적: 디저트 카테고리 데이터 수집 및 인기도 분석
"""

import requests
import json
from datetime import datetime, timedelta

class NaverShoppingAPI:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = "https://openapi.naver.com"
        
    def get_headers(self):
        return {
            'X-Naver-Client-Id': self.client_id,
            'X-Naver-Client-Secret': self.client_secret,
            'Content-Type': 'application/json'
        }
    
    def search_shopping(self, query, display=20, start=1, sort="sim"):
        """
        네이버 쇼핑 검색 API
        query: 검색어
        display: 검색 결과 출력 건수 (1~100)
        start: 검색 시작 위치 (1~1000)
        sort: 정렬 옵션 (sim, date, asc, dsc)
        """
        url = f"{self.base_url}/v1/search/shop.json"
        params = {
            'query': query,
            'display': display,
            'start': start,
            'sort': sort
        }
        
        response = requests.get(url, params=params, headers=self.get_headers())
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"검색 실패: {response.status_code} - {response.text}")
            return None
    
    def get_shopping_insight(self, category_id, start_date, end_date):
        """
        네이버 쇼핑 인사이트 API
        category_id: 쇼핑 카테고리 ID (8자리)
        start_date: 조회 시작일 (YYYY-MM-DD)
        end_date: 조회 종료일 (YYYY-MM-DD)
        """
        url = f"{self.base_url}/v1/datalab/shopping/categories"
        
        data = {
            "startDate": start_date,
            "endDate": end_date,
            "timeUnit": "month",
            "category": [{"name": f"카테고리_{category_id}", "param": [category_id]}]
        }
        
        response = requests.post(url, data=json.dumps(data), headers=self.get_headers())
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"인사이트 조회 실패: {response.status_code} - {response.text}")
            return None

# 디저트 50개 데이터베이스
DESSERT_DATABASE = {
    "베이커리/케이크류": [
        "케이크", "마카롱", "티라미수", "마들렌", "크루아상",
        "스콘", "에클레어", "타르트", "브라우니", "쿠키",
        "도넛", "머핀", "크레이프", "파운드케이크", "롤케이크"
    ],
    "아이스크림/냉동디저트": [
        "아이스크림", "젤라또", "소르베", "팥빙수", "눈꽃빙수",
        "아이스바", "아포가토", "그라니타", "프로즌요거트", "밀크셰이크"
    ],
    "전통/길거리디저트": [
        "붕어빵", "호떡", "떡", "약과", "타코야키",
        "츄러스", "와플", "크로플", "호빵", "군고구마"
    ],
    "푸딩/젤리류": [
        "푸딩", "젤리", "판나코타", "크렘브륄레", "무스",
        "바바로아", "실버커드", "플랑", "아가젤리", "과일화채"
    ],
    "초콜릿/캔디류": [
        "초콜릿", "트러플", "봉봉", "캔디", "마시멜로"
    ]
}

def test_dessert_popularity():
    """디저트 인기도 테스트 함수"""
    # 네이버 개발자센터에서 발급받은 API 키
    api = NaverShoppingAPI("UP8PqJq_FpkcB63sEFH9", "B7sXznX3pP")
    
    print("🍰 디저트 인기도 분석 시작...")
    
    # 각 카테고리별 인기 디저트 검색
    results = {}
    
    for category, desserts in DESSERT_DATABASE.items():
        print(f"\n📊 {category} 분석 중...")
        category_results = []
        
        for dessert in desserts[:3]:  # 테스트를 위해 각 카테고리당 3개만
            print(f"  - {dessert} 검색 중...")
            
            # 쇼핑 검색으로 상품 수와 리뷰 정보 확인
            search_result = api.search_shopping(dessert, display=10, sort="sim")
            
            if search_result and 'items' in search_result:
                items = search_result['items']
                avg_price = sum([int(item.get('lprice', 0)) for item in items]) / len(items) if items else 0
                total_items = search_result.get('total', 0)
                
                category_results.append({
                    'name': dessert,
                    'total_products': total_items,
                    'avg_price': avg_price,
                    'top_items': [item.get('title', '') for item in items[:3]]
                })
        
        results[category] = category_results
    
    return results

def analyze_trending_desserts():
    """트렌딩 디저트 분석"""
    print("🔥 트렌딩 디저트 키워드 분석...")
    
    # 2024년 신상 디저트 키워드들
    trending_keywords = [
        "크로플", "마라탕후식", "흑임자라떼", "말차디저트", "비건디저트",
        "수제쿠키", "홈베이킹", "디저트카페", "젤라또", "마카롱"
    ]
    
    # TODO: 실제 API 호출로 트렌드 분석
    # 현재는 구조만 제시
    
    return trending_keywords

if __name__ == "__main__":
    print("🎯 네이버 쇼핑 API 디저트 분석 도구")
    print("=" * 50)
    
    # API 키 설정 안내
    print("📝 사용 전 준비사항:")
    print("1. 네이버 개발자센터(https://developers.naver.com) 가입")
    print("2. 애플리케이션 등록 후 Client ID/Secret 발급")
    print("3. 이 파일의 YOUR_CLIENT_ID, YOUR_CLIENT_SECRET 교체")
    print()
    
    # 디저트 데이터베이스 출력
    print("🍰 구축된 디저트 데이터베이스:")
    total_count = 0
    for category, desserts in DESSERT_DATABASE.items():
        print(f"  {category}: {len(desserts)}개")
        total_count += len(desserts)
    print(f"  📊 총 디저트 종류: {total_count}개")
    print()
    
    # 트렌딩 키워드 분석
    trending = analyze_trending_desserts()
    print(f"🔥 2024년 트렌딩 디저트: {', '.join(trending[:5])}")
    print()
    
    print("⚡ API 키 설정 후 test_dessert_popularity() 함수 실행 가능!")