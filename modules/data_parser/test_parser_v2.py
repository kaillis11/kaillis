#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
개선된 쇼핑 데이터 파서 v2
"""

import re
import json
from datetime import datetime
from typing import List, Dict, Optional

class ImprovedParser:
    def __init__(self):
        """파서 초기화"""
        self.categories = {
            'macaron': '마카롱',
            'dessert': '디저트',
            'icecream': '아이스크림'
        }
        
    def parse_coupang_text(self, text: str) -> List[Dict]:
        """쿠팡 텍스트 파싱"""
        print("📄 쿠팡 데이터 파싱 중...")
        
        products = []
        lines = text.split('\n')
        
        # 여러 줄에 걸쳐 있는 상품 정보 처리
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # 제품명 패턴 찾기 (마카롱이 포함된 긴 텍스트)
            if '마카롱' in line and len(line) > 20:
                product_name = line
                
                # 다음 줄들에서 가격 찾기
                price = None
                rating = None
                reviews = None
                discount = None
                
                # 최대 5줄까지 확인
                for j in range(i+1, min(i+6, len(lines))):
                    next_line = lines[j].strip()
                    
                    # 가격 패턴
                    price_match = re.search(r'(\d{1,3}(?:,\d{3})*)\s*원', next_line)
                    if price_match and not price:
                        price = price_match.group(1)
                    
                    # 평점 패턴
                    rating_match = re.search(r'(\d\.\d)', next_line)
                    if rating_match and not rating:
                        rating = rating_match.group(1)
                    
                    # 리뷰 패턴
                    review_match = re.search(r'\((\d+(?:,\d+)*)\)', next_line)
                    if review_match and not reviews:
                        reviews = review_match.group(1)
                    
                    # 할인 패턴
                    discount_match = re.search(r'할인(\d+)%', next_line)
                    if discount_match and not discount:
                        discount = discount_match.group(1) + '%'
                
                if price:  # 가격이 있으면 상품으로 인정
                    product = {
                        'name': product_name,
                        'price': price,
                        'price_numeric': int(price.replace(',', '')),
                        'rating': rating or '0.0',
                        'reviews': reviews or '0',
                        'discount': discount
                    }
                    products.append(product)
                    
                i = j  # 처리한 줄까지 건너뛰기
            else:
                i += 1
        
        # 순위 부여
        for idx, product in enumerate(products, 1):
            product['rank'] = idx
            product['category'] = 'macaron'
            product['category_name'] = '마카롱'
            product['parsed_at'] = datetime.now().isoformat()
            
        return products
    
    def preview_results(self, products: List[Dict]):
        """결과 미리보기"""
        if not products:
            print("❌ 파싱된 상품이 없습니다.")
            return
            
        print(f"\n🏆 마카롱 순위 TOP {len(products)}")
        print("=" * 80)
        
        for product in products:
            discount_info = f" ({product['discount']} 할인)" if product.get('discount') else ""
            
            print(f"{product['rank']:2d}위. {product['name']}")
            print(f"     💰 {product['price']}원{discount_info}")
            print(f"     ⭐ {product['rating']}점 | 📝 {product['reviews']}개 리뷰")
            print()
    
    def save_to_json(self, products: List[Dict]) -> str:
        """JSON 파일로 저장"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"coupang_macaron_{timestamp}.json"
        
        data = {
            'meta': {
                'title': '쿠팡 마카롱 순위',
                'total_products': len(products),
                'parsed_at': datetime.now().isoformat(),
                'parser_version': '2.0_improved'
            },
            'products': products
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print(f"💾 저장 완료: {filename}")
        return filename

# 테스트 데이터
test_data = """
파스키에 마카롱 6종 x 2개입 세트 (냉동), 154g, 1개
9,980원
로켓배송
내일(목) 새벽 도착 보장
4.5
(6327)

널담 마카롱 사랑세트 8종 (냉동), 50g, 8개입, 1세트
할인20%11,900원
9,410원
로켓배송
내일(목) 새벽 도착 보장
4.5
(6406)

[러브빈마카롱] 수제 마카롱 개별포장 8개입 스승의날 어린이날 단체주문, 세트 2번, 1세트
할인26%16,000원
11,700원
모레(금) 도착 예정
4.5
(516)

14년동안 마카롱만 만들어온 전문점의 정통 프랑스 무색소 수제 마카롱 16구상자 선물세트, 16개, 25g
10%28,200원
25,200원
배송비 3,800원
모레(금) 도착 예정
5
(34)

파스키에 마카롱 12개입 (냉동), 154g, 2개
3%19,960원
19,360원
로켓배송
내일(목) 새벽 도착 보장
4.5
(6327)

누니 마카롱(뚱카롱) 8구 선물세트, 시즌투(2), 1개, 320g
16,900원
모레(금) 도착 예정
5
(302)

하겐다즈 아이스크림 마카롱 5입 세트 (냉동), 35g, 5개입, 1세트
26,900원
로켓배송
내일(목) 새벽 도착 보장
4.5
(71)

코스트코 36 마카롱 468g, 1박스
28,980원
모레(금) 도착 예정
5
(19)

"건강하고 뚱뚱한 맛의 향연"수제마카롱 12가지맛 x 10구12구 선물세트/ 개별밀봉포장 / 본점직영 / 랜덤배송, 10개, 35g
할인45%25,000원
13,520원
모레(금) 도착 예정
4.5
(203)

신성베이커리 수박마카롱 (냉동), 25g, 1개, 6개입
6,770원
로켓배송
내일(목) 새벽 도착 보장
(339)
"""

def main():
    """메인 테스트"""
    parser = ImprovedParser()
    
    print("🛒 개선된 쇼핑 데이터 파서 v2")
    print("📋 쿠팡 마카롱 데이터 파싱 테스트...")
    
    # 파싱 실행
    products = parser.parse_coupang_text(test_data)
    
    if products:
        # 결과 미리보기
        parser.preview_results(products)
        
        # JSON 저장
        filepath = parser.save_to_json(products)
        print(f"\n✅ 테스트 완료! 파일: {filepath}")
        print("🎯 이제 WhatToEat 룰렛에 연동할 수 있습니다!")
    else:
        print("\n😅 파싱할 수 있는 데이터를 찾지 못했습니다.")

if __name__ == "__main__":
    main()