#!/usr/bin/env python3
"""
네이버 데이터랩 API 테스트 - 카테고리 트렌드 분석
"""

import requests
import json
from datetime import datetime, timedelta

def test_datalab_categories():
    """데이터랩 쇼핑 카테고리 트렌드 테스트"""
    client_id = "UP8PqJq_FpkcB63sEFH9"
    client_secret = "B7sXznX3pP"
    
    headers = {
        'X-Naver-Client-Id': client_id,
        'X-Naver-Client-Secret': client_secret,
        'Content-Type': 'application/json'
    }
    
    # 날짜 설정 (최근 3개월)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    
    print("📊 네이버 데이터랩 쇼핑 카테고리 트렌드 테스트")
    print("=" * 60)
    print(f"📅 분석 기간: {start_date.strftime('%Y-%m-%d')} ~ {end_date.strftime('%Y-%m-%d')}")
    print()
    
    # 테스트할 카테고리 ID들 (추정)
    test_categories = {
        "과자류": "50000169",  # 추정 ID
        "디저트": "50000170",  # 추정 ID  
        "아이스크림": "50000171",  # 추정 ID
        "음료": "50000172",   # 추정 ID
        "케이크": "50000173"   # 추정 ID
    }
    
    url = "https://openapi.naver.com/v1/datalab/shopping/categories"
    
    for category_name, category_id in test_categories.items():
        print(f"🔍 '{category_name}' (ID: {category_id}) 트렌드 분석...")
        
        data = {
            "startDate": start_date.strftime('%Y-%m-%d'),
            "endDate": end_date.strftime('%Y-%m-%d'),
            "timeUnit": "month",
            "category": [{"name": category_name, "param": [category_id]}]
        }
        
        try:
            response = requests.post(url, data=json.dumps(data), headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                print(f"  ✅ 성공! 데이터 수신됨")
                
                # 결과 분석
                if 'results' in result and result['results']:
                    trend_data = result['results'][0]['data']
                    latest_ratio = trend_data[-1]['ratio'] if trend_data else 0
                    print(f"  📈 최근 트렌드 지수: {latest_ratio}")
                    
                    # 트렌드 변화 계산
                    if len(trend_data) >= 2:
                        prev_ratio = trend_data[-2]['ratio']
                        change = latest_ratio - prev_ratio
                        trend_icon = "📈" if change > 0 else "📉" if change < 0 else "➡️"
                        print(f"  {trend_icon} 전월 대비 변화: {change:+.1f}")
                
            elif response.status_code == 400:
                print(f"  ❌ 잘못된 카테고리 ID: {category_id}")
                print(f"  💡 실제 카테고리 ID를 찾아야 합니다")
                
            else:
                print(f"  ❌ API 오류: {response.status_code}")
                print(f"  📄 응답: {response.text}")
                
        except Exception as e:
            print(f"  ❌ 에러 발생: {str(e)}")
        
        print()
    
    print("💡 카테고리 ID 확인 방법:")
    print("1. 네이버 쇼핑에서 원하는 카테고리 페이지 방문")
    print("2. URL에서 cat_id= 뒤의 숫자 확인")
    print("3. 예: https://shopping.naver.com/category/...?cat_id=50000123")
    print("4. 또는 네이버 쇼핑파트너센터에서 카테고리 ID 엑셀 다운로드")

if __name__ == "__main__":
    test_datalab_categories()