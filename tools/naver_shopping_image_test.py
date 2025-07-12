#!/usr/bin/env python3
"""
네이버 쇼핑 API 이미지 추출 테스트 스크립트
목적: 상품 검색 → 이미지 URL 추출 → 실제 이미지 다운로드 가능 여부 확인
"""

import requests
import json
from datetime import datetime

class NaverShoppingImageAPI:
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
    
    def search_shopping_with_images(self, query, display=10, start=1, sort="sim"):
        """
        네이버 쇼핑 검색 API - 이미지 URL 포함
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
    
    def extract_product_images(self, search_result):
        """
        검색 결과에서 상품 이미지 정보 추출
        """
        if not search_result or 'items' not in search_result:
            return []
        
        products = []
        for item in search_result['items']:
            product = {
                'title': item.get('title', '').replace('<b>', '').replace('</b>', ''),
                'image_url': item.get('image', ''),
                'price': item.get('lprice', 0),
                'mall': item.get('mallName', ''),
                'link': item.get('link', ''),
                'brand': item.get('brand', ''),
                'maker': item.get('maker', '')
            }
            products.append(product)
        
        return products
    
    def verify_image_accessibility(self, image_url):
        """
        이미지 URL 접근 가능성 테스트
        """
        try:
            response = requests.head(image_url, timeout=10)
            return {
                'accessible': response.status_code == 200,
                'status_code': response.status_code,
                'content_type': response.headers.get('content-type', ''),
                'content_length': response.headers.get('content-length', '')
            }
        except Exception as e:
            return {
                'accessible': False,
                'error': str(e)
            }

def test_dessert_images():
    """디저트 상품 이미지 추출 테스트"""
    # 기존 API 키 사용
    api = NaverShoppingImageAPI("UP8PqJq_FpkcB63sEFH9", "B7sXznX3pP")
    
    print("🍰 네이버 쇼핑 API 이미지 추출 테스트 시작...")
    print("=" * 60)
    
    # 테스트할 디저트 상품들
    test_products = [
        "마켓오 브라우니",
        "배스킨라빈스 아이스크림",
        "던킨도넛",
        "허쉬 초콜릿",
        "오리온 초코파이"
    ]
    
    all_results = []
    
    for product in test_products:
        print(f"\n🔍 '{product}' 검색 중...")
        
        # 네이버 쇼핑 검색 실행
        search_result = api.search_shopping_with_images(product, display=5)
        
        if search_result:
            print(f"   📊 총 {search_result.get('total', 0)}개 상품 발견")
            
            # 이미지 정보 추출
            products = api.extract_product_images(search_result)
            
            print(f"   🖼️ 추출된 상품 정보:")
            for i, prod in enumerate(products, 1):
                print(f"   {i}. {prod['title'][:50]}...")
                print(f"      이미지: {prod['image_url']}")
                print(f"      가격: {prod['price']}원")
                print(f"      쇼핑몰: {prod['mall']}")
                
                # 이미지 접근 가능성 테스트
                if prod['image_url']:
                    image_check = api.verify_image_accessibility(prod['image_url'])
                    if image_check['accessible']:
                        print(f"      ✅ 이미지 접근 가능 ({image_check['content_type']})")
                    else:
                        print(f"      ❌ 이미지 접근 불가 ({image_check.get('status_code', 'Unknown')})")
                else:
                    print(f"      ⚠️ 이미지 URL 없음")
                print()
            
            all_results.extend(products)
        else:
            print(f"   ❌ '{product}' 검색 실패")
    
    return all_results

def generate_json_output(products):
    """
    WhatToEat 룰렛용 JSON 형태로 변환
    """
    output = {
        "meta": {
            "title": "네이버 쇼핑 API 디저트 이미지 데이터",
            "category": "dessert",
            "total_products": len(products),
            "extracted_at": datetime.now().isoformat(),
            "source": "naver_shopping_api"
        },
        "products": []
    }
    
    for i, product in enumerate(products, 1):
        output["products"].append({
            "rank": i,
            "name": product['title'],
            "image_url": product['image_url'],
            "price": product['price'],
            "mall": product['mall'],
            "brand": product['brand'],
            "link": product['link']
        })
    
    return output

if __name__ == "__main__":
    print("🎯 네이버 쇼핑 API 이미지 추출 테스트 도구")
    print("=" * 50)
    
    # API 키 확인
    print("🔑 API 키 정보:")
    print(f"   Client ID: UP8PqJq_FpkcB63sEFH9")
    print(f"   Client Secret: B7sXz*** (보안)")
    print()
    
    # 테스트 실행
    try:
        products = test_dessert_images()
        
        print(f"\n📊 테스트 결과 요약:")
        print(f"   총 추출된 상품: {len(products)}개")
        
        # 이미지 있는 상품 카운트
        with_images = sum(1 for p in products if p['image_url'])
        print(f"   이미지 있는 상품: {with_images}개")
        print(f"   이미지 성공률: {(with_images/len(products)*100):.1f}%")
        
        # JSON 출력 생성
        json_output = generate_json_output(products)
        
        # 파일로 저장
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"naver_shopping_images_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(json_output, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 결과 저장: {output_file}")
        print(f"🎉 테스트 완료! 네이버 쇼핑 API 이미지 추출 성공!")
        
    except Exception as e:
        print(f"❌ 테스트 중 오류 발생: {e}")
        print("   API 키나 네트워크 상태를 확인해주세요.")