#!/usr/bin/env python3
"""
진짜 API 상태 확인 - 정확한 문제 파악
"""

import requests

def test_real_apis():
    """실제 API 상태 확인"""
    client_id = "UP8PqJq_FpkcB63sEFH9"
    client_secret = "B7sXznX3pP"
    
    headers = {
        'X-Naver-Client-Id': client_id,
        'X-Naver-Client-Secret': client_secret
    }
    
    print("🔍 네이버 API 실제 상태 확인")
    print("=" * 50)
    
    # 1. 쇼핑 검색 API 테스트
    print("1. 쇼핑 검색 API 테스트:")
    url = "https://openapi.naver.com/v1/search/shop.json"
    params = {'query': '메로나', 'display': 5}
    
    try:
        response = requests.get(url, params=params, headers=headers)
        print(f"   상태코드: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 성공: {data.get('total', 0)}개 상품 검색됨")
        else:
            print(f"   ❌ 실패: {response.text}")
    except Exception as e:
        print(f"   ❌ 에러: {e}")
    
    print()
    
    # 2. 데이터랩 API 테스트  
    print("2. 데이터랩 API 테스트:")
    from datetime import datetime, timedelta
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    
    headers_datalab = {
        'X-Naver-Client-Id': client_id,
        'X-Naver-Client-Secret': client_secret,
        'Content-Type': 'application/json'
    }
    
    url = "https://openapi.naver.com/v1/datalab/shopping/categories"
    data = {
        "startDate": start_date.strftime('%Y-%m-%d'),
        "endDate": end_date.strftime('%Y-%m-%d'),
        "timeUnit": "month",
        "category": [{"name": "아이스크림", "param": ["50000171"]}]
    }
    
    try:
        response = requests.post(url, json=data, headers=headers_datalab)
        print(f"   상태코드: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            if 'results' in result:
                latest = result['results'][0]['data'][-1]['ratio']
                print(f"   ✅ 성공: 아이스크림 트렌드 {latest}점")
            else:
                print(f"   ❌ 데이터 없음: {result}")
        else:
            print(f"   ❌ 실패: {response.text}")
    except Exception as e:
        print(f"   ❌ 에러: {e}")

if __name__ == "__main__":
    test_real_apis()