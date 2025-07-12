#\!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
범용 쇼핑 데이터 파서 테스트 (pyperclip 없이)
"""

import re
import json
from datetime import datetime
from typing import List, Dict, Optional

class UniversalShoppingParser:
    def __init__(self):
        """범용 파서 초기화"""
        self.categories = {
            'dessert': '디저트',
            'macaron': '마카롱',
            'icecream': '아이스크림', 
            'frozen': '냉동식품',
            'snack': '과자',
            'drink': '음료',
            'chicken': '치킨',
            'pizza': '피자',
            'coffee': '커피',
            'bread': '빵'
        }
        
        # 광고/스폰서 키워드
        self.ad_keywords = [
            '광고', 'AD', 'Sponsored', '스폰서', 
            '프로모션', '파워클릭', '쇼핑검색광고'
        ]
        
    def parse_text_directly(self, text: str, category: str = 'macaron') -> List[Dict]:
        """텍스트 직접 파싱"""
        print(f"📄 텍스트 파싱 중... 카테고리: {self.categories.get(category, category)}")
        
        products = self._smart_extract(text)
        
        for idx, product in enumerate(products, 1):
            product['rank'] = idx
            product['category'] = category
            product['category_name'] = self.categories.get(category, category)
            product['parsed_at'] = datetime.now().isoformat()
            
        return products
    
    def _smart_extract(self, text: str) -> List[Dict]:
        """스마트 추출 - 다양한 패턴 인식"""
        products = []
        
        # 줄 단위로 분할
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # 광고 스킵
            if any(keyword in line for keyword in self.ad_keywords):
                continue
                
            # 가격 패턴 찾기
            price_patterns = [
                r'(\d{1,3}(?:,\d{3})*)\s*원',  # 1,234원
                r'₩\s*(\d{1,3}(?:,\d{3})*)',   # ₩1,234
                r'(\d+(?:,\d+)*)\s*KRW',       # 1,234 KRW
            ]
            
            for pattern in price_patterns:
                price_match = re.search(pattern, line)
                if price_match:
                    price_value = price_match.group(1)
                    
                    # 제품명 추출 (가격 앞부분에서)
                    product_name = self._extract_product_name_from_line(line, price_match.start())
                    
                    if product_name and len(product_name) > 5:
                        # 추가 정보 추출
                        reviews = self._extract_reviews(line)
                        rating = self._extract_rating(line)
                        discount = self._extract_discount(line)
                        
                        product = {
                            'name': product_name,
                            'price': price_value,
                            'price_numeric': int(price_value.replace(',', '')),
                            'reviews': reviews,
                            'rating': rating,
                            'discount': discount,
                        }
                        
                        # 중복 제거 (같은 제품명 제외)
                        if not any(p['name'] == product_name for p in products):
                            products.append(product)
                    break
                    
        return products[:20]  # 최대 20개
    
    def _extract_product_name_from_line(self, line: str, price_start: int) -> Optional[str]:
        """라인에서 제품명 추출 (가격 앞부분)"""
        # 가격 앞부분 텍스트 추출
        text_before_price = line[:price_start].strip()
        
        # 제품명 패턴들
        name_patterns = [
            r'([가-힣a-zA-Z0-9\s\-\(\)\[\],\.]+?)\s*할인?\d*%?$',  # 할인 앞까지
            r'([가-힣a-zA-Z0-9\s\-\(\)\[\],\.]+?)\s*무료배송',      # 무료배송 앞까지
            r'([가-힣a-zA-Z0-9\s\-\(\)\[\],\.]+?)\s*로켓배송',      # 로켓배송 앞까지
            r'([가-힣a-zA-Z0-9\s\-\(\)\[\],\.]+)',                   # 전체
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, text_before_price)
            if match:
                name = match.group(1).strip()
                
                # 너무 짧거나 긴 이름 제외
                if 5 < len(name) < 100:
                    # 불필요한 키워드 제거
                    unwanted = ['쿠팡추천', '베스트셀러', '최근', '다른', '고객이', '많이', '구매한']
                    if not any(word in name for word in unwanted):
                        return name
                        
        return None
    
    def _extract_reviews(self, text: str) -> str:
        """리뷰 수 추출"""
        patterns = [
            r'\((\d+(?:,\d+)*)\)',  # (1,234) 형태
            r'(\d+(?:,\d+)*)\s*개?\s*리뷰',
            r'리뷰\s*(\d+(?:,\d+)*)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        return "0"
    
    def _extract_rating(self, text: str) -> str:
        """평점 추출"""
        patterns = [
            r'(\d\.\d)\s*점?',
            r'★\s*(\d\.\d)',
            r'평점\s*(\d\.\d)',
            r'^(\d)\s*$',  # 단독 숫자
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        return "0.0"
    
    def _extract_discount(self, text: str) -> Optional[str]:
        """할인율 추출"""
        patterns = [
            r'할인(\d+)\s*%',
            r'(\d+)\s*%\s*할인',
            r'(\d+)\s*%↓',
            r'(\d+)\s*%\s*OFF',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return f"{match.group(1)}%"
        return None
    
    def preview_results(self, products: List[Dict]):
        """결과 미리보기"""
        if not products:
            print("❌ 파싱된 상품이 없습니다.")
            return
            
        print(f"\n🏆 {products[0].get('category_name', '상품')} 순위 TOP {len(products)}")
        print("=" * 80)
        
        for product in products:
            discount_info = f" ({product['discount']} 할인)" if product.get('discount') else ""
            
            print(f"{product['rank']:2d}위. {product['name']}")
            print(f"     💰 {product['price']}원{discount_info}")
            print(f"     ⭐ {product['rating']}점  < /dev/null |  📝 {product['reviews']}개 리뷰")
            print()
    
    def save_to_json(self, products: List[Dict], filename: str = None) -> str:
        """JSON 파일로 저장"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            category = products[0]['category'] if products else 'unknown'
            filename = f"coupang_{category}_{timestamp}.json"
            
        data = {
            'meta': {
                'total_products': len(products),
                'parsed_at': datetime.now().isoformat(),
                'parser_version': '3.0_test',
                'method': 'text_direct_parsing'
            },
            'products': products
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print(f"💾 저장 완료: {filename}")
        return filename

# 테스트 데이터 (휘광님이 붙여넣은 쿠팡 마카롱 데이터)
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
    parser = UniversalShoppingParser()
    
    print("🛒 범용 쇼핑 데이터 파서 테스트")
    print("📋 쿠팡 마카롱 데이터 파싱 테스트...")
    
    # 파싱 실행
    products = parser.parse_text_directly(test_data, 'macaron')
    
    if products:
        # 결과 미리보기
        parser.preview_results(products)
        
        # JSON 저장
        filepath = parser.save_to_json(products)
        print(f"\n✅ 테스트 완료\! 파일: {filepath}")
        print("🎯 이제 WhatToEat 룰렛에 연동할 수 있습니다\!")
    else:
        print("\n😅 파싱할 수 있는 데이터를 찾지 못했습니다.")

if __name__ == "__main__":
    main()
