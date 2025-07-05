#!/usr/bin/env python3
"""
간단한 검색 API 테스트
"""

import requests

client_id = "UP8PqJq_FpkcB63sEFH9"
client_secret = "B7sXznX3pP"

headers = {
    'X-Naver-Client-Id': client_id,
    'X-Naver-Client-Secret': client_secret
}

print("🔍 간단한 쇼핑 검색 테스트")
print("=" * 30)

# 가장 간단한 검색
url = "https://openapi.naver.com/v1/search/shop.json"
params = {
    'query': '아이스크림',
    'display': 1
}

response = requests.get(url, params=params, headers=headers)

print(f"상태코드: {response.status_code}")
print(f"응답: {response.text[:200]}...")

if response.status_code == 200:
    data = response.json()
    print(f"✅ 성공! 총 {data.get('total', 0)}개 상품 발견")
else:
    print("❌ 여전히 실패...")
    print("💡 네이버 개발자센터에서 '검색 > 쇼핑' API 활성화 필요")