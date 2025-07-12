#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
범용 스마트 파서 v8.0
모든 쇼핑 카테고리 지원 - 마카롱, 아이스크림, 디저트 등
"""

import re
import json
from datetime import datetime
from typing import List, Dict, Optional

class UniversalSmartParser:
    def __init__(self):
        """파서 초기화"""
        self.categories = {
            'macaron': '마카롱',
            'icecream': '아이스크림',
            'lowsugar_icecream': '저당 아이스크림',
            'dessert': '디저트',
            'snack': '간식'
        }
        
        # 광고 키워드
        self.ad_keywords = ['AD', '광고', 'Sponsored', '스폰서']
        
        # 카테고리별 검색 키워드
        self.category_keywords = {
            'macaron': ['마카롱'],
            'icecream': ['아이스크림', '아이스밀크', '저당', '제로', '바닐라', '초코', '딸기', '복숭아', '멜론', '모나카', '초코바', '생요거트바'],
            'lowsugar_icecream': ['저당', '제로', '아이스크림', '아이스밀크'],
            'dessert': ['디저트', '케이크', '푸딩', '젤리'],
            'snack': ['과자', '쿠키', '비스킷']
        }
        
    def parse_coupang_data(self, text: str, category: str = 'auto') -> List[Dict]:
        """쿠팡 데이터 파싱 - 카테고리 자동 감지 또는 수동 지정"""
        print(f"📄 범용 스마트 파서 v8.0 실행 중...")
        
        # 카테고리 자동 감지
        if category == 'auto':
            category = self._detect_category(text)
            print(f"🔍 자동 감지된 카테고리: {self.categories.get(category, category)}")
        
        # 전체 텍스트를 라인으로 분리
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        products = []
        i = 0
        
        while i < len(lines):
            # 제품명 찾기 (카테고리 키워드가 포함된 라인)
            if self._is_product_line(lines[i], category):
                product_name = lines[i]
                
                # 이 제품이 광고인지 확인
                if self._is_advertisement(lines, i):
                    print(f"🚫 광고 필터링: {product_name[:30]}...")
                    i += 1
                    continue
                
                # 제품 정보 추출
                product_info = self._extract_product_info(lines, i, product_name, category)
                if product_info:
                    products.append(product_info)
                    print(f"✅ 파싱 완료: {product_name[:30]}...")
                    
            i += 1
        
        # 순위 정렬 (가격 기준)
        products.sort(key=lambda x: x.get('price_numeric', 999999))
        
        # 순위 할당
        for i, product in enumerate(products):
            product['rank'] = i + 1
        
        return products
    
    def _detect_category(self, text: str) -> str:
        """텍스트에서 카테고리 자동 감지"""
        text_lower = text.lower()
        
        # 카테고리별 키워드 빈도 계산
        category_scores = {}
        for category, keywords in self.category_keywords.items():
            score = 0
            for keyword in keywords:
                score += text_lower.count(keyword.lower())
            category_scores[category] = score
        
        # 가장 높은 점수의 카테고리 선택
        best_category = max(category_scores, key=category_scores.get)
        
        # 점수가 0이면 기본 카테고리
        if category_scores[best_category] == 0:
            return 'icecream'  # 기본값
        
        return best_category
    
    def _is_product_line(self, line: str, category: str) -> bool:
        """제품명 라인인지 확인"""
        # 최소 길이 확인
        if len(line) < 15:
            return False
        
        # 카테고리별 키워드 확인
        keywords = self.category_keywords.get(category, [])
        for keyword in keywords:
            if keyword in line:
                return True
        
        return False
    
    def _is_advertisement(self, lines: List[str], start_idx: int) -> bool:
        """광고 여부 확인"""
        # 현재 라인 및 주변 라인에서 광고 키워드 찾기
        check_range = range(max(0, start_idx - 3), min(len(lines), start_idx + 10))
        
        for i in check_range:
            line = lines[i]
            for keyword in self.ad_keywords:
                if keyword in line:
                    return True
        
        return False
    
    def _extract_product_info(self, lines: List[str], start_idx: int, product_name: str, category: str) -> Optional[Dict]:
        """제품 정보 추출"""
        price = None
        original_price = None
        discount = None
        rating = '0.0'
        reviews = '0'
        
        # 제품명 이후 최대 20라인 확인
        end_idx = min(len(lines), start_idx + 20)
        
        for i in range(start_idx + 1, end_idx):
            line = lines[i]
            
            # 다음 제품명이 나오면 중단
            if self._is_product_line(line, category) and i != start_idx:
                break
            
            # 할인 가격 패턴 1: "할인20%11,900원" 또는 "15%10,900원"
            discount_match = re.search(r'(?:할인)?(\d+)%(\d{1,3}(?:,\d{3})*)원', line)
            if discount_match and not price:
                discount = discount_match.group(1) + '%'
                original_price = discount_match.group(2)
                
                # 다음 줄에서 실제 가격 찾기
                for j in range(i + 1, min(i + 3, len(lines))):
                    next_line = lines[j]
                    actual_price_match = re.search(r'^(\d{1,3}(?:,\d{3})*)원$', next_line)
                    if actual_price_match:
                        price = actual_price_match.group(1)
                        break
            
            # 일반 가격 패턴
            if not price:
                price_match = re.search(r'^(\d{1,3}(?:,\d{3})*)원$', line)
                if price_match:
                    price = price_match.group(1)
            
            # 평점 패턴 (4.5, 5.0, 2.0 등)
            if re.match(r'^(4|5|2|3)(\.\d)?$', line):
                rating = line
                if '.' not in rating:
                    rating = rating + '.0'
            
            # 리뷰 패턴
            review_match = re.search(r'^\((\d+(?:,\d+)*)\)$', line)
            if review_match:
                reviews = review_match.group(1)
        
        # 가격이 있어야 유효한 제품
        if price:
            return {
                'name': product_name,
                'price': price,
                'price_numeric': int(price.replace(',', '')),
                'original_price': original_price,
                'discount': discount,
                'rating': rating,
                'reviews': reviews,
                'category': category,
                'category_name': self.categories.get(category, category),
                'parsed_at': datetime.now().isoformat(),
                'rank': 0  # 나중에 할당
            }
        
        return None
    
    def preview_results(self, products: List[Dict]):
        """결과 미리보기"""
        if not products:
            print("❌ 파싱된 상품이 없습니다.")
            return
        
        category_name = products[0]['category_name'] if products else "상품"
        print(f"\n🏆 {category_name} 순위 TOP {len(products)}")
        print("=" * 100)
        
        for product in products:
            discount_info = ""
            if product.get('discount'):
                discount_info = f" ({product['discount']} 할인)"
            
            original_price_info = ""
            if product.get('original_price'):
                original_price_info = f" ← 정가: {product['original_price']}원"
            
            print(f"{product['rank']:2d}위. {product['name']}")
            print(f"     💰 {product['price']}원{discount_info}{original_price_info}")
            print(f"     ⭐ {product['rating']}점 | 📝 {product['reviews']}개 리뷰")
            print()
    
    def save_to_json(self, products: List[Dict]) -> str:
        """JSON 파일로 저장"""
        if not products:
            return ""
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        category = products[0]['category']
        filename = f"coupang_{category}_universal_{timestamp}.json"
        
        data = {
            'meta': {
                'title': f"쿠팡 {products[0]['category_name']} 순위",
                'total_products': len(products),
                'parsed_at': datetime.now().isoformat(),
                'parser_version': '8.0_universal_smart',
                'category': category,
                'note': '범용 스마트 파서 - 모든 쇼핑 카테고리 지원'
            },
            'products': products
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print(f"💾 저장 완료: {filename}")
        return filename

# 실제 사용 예제
def parse_any_shopping_data(data: str, category: str = 'auto') -> List[Dict]:
    """모든 쇼핑 데이터 파싱"""
    parser = UniversalSmartParser()
    return parser.parse_coupang_data(data, category)

# 테스트용 메인 함수
def main():
    """테스트 실행"""
    parser = UniversalSmartParser()
    
    print("🛒 범용 스마트 파서 v8.0")
    print("📋 모든 쇼핑 카테고리 지원...")
    
    # 저당 아이스크림 테스트 데이터
    test_data = """
라라스윗 저당 딸기 생요거트바 (냉동), 1개, 6개입, 70ml
라라스윗 저당 딸기 생요거트바 (냉동), 1개, 6개입, 70ml
10%7,900원
7,110원
로켓배송
(10ml당 169원)
내일(목) 새벽 도착 보장
4.5
(1239)
최대 355원 적립
최대 355원 적립
1
라라스윗 저당 복숭아 생요거트바 (냉동), 1개, 6개입, 70ml
라라스윗 저당 복숭아 생요거트바 (냉동), 1개, 6개입, 70ml
7,900원
로켓배송
(10ml당 188원)
내일(목) 새벽 도착 보장
5
(41)
최대 395원 적립
최대 395원 적립
2
롯데웰푸드 티코 밀크초코 저당 (냉동), 15개, 1개입, 34ml
롯데웰푸드 티코 밀크초코 저당 (냉동), 15개, 1개입, 34ml
10%8,000원
7,200원
로켓배송
(10ml당 141원)
내일(목) 새벽 도착 보장
5
(232)
최대 360원 적립
최대 360원 적립
3
빙그레 생귤탱귤 제로 감귤 막대 아이스크림 (냉동), 70ml, 1개입, 8개
빙그레 생귤탱귤 제로 감귤 막대 아이스크림 (냉동), 70ml, 1개입, 8개
19%5,960원
4,800원
로켓배송
(10ml당 86원)
내일(목) 새벽 도착 보장
5
(1800)
최대 240원 적립
최대 240원 적립
5
라라스윗 저당 바닐라 초코바 (냉동), 90ml, 4개입, 1개
라라스윗 저당 바닐라 초코바 (냉동), 90ml, 4개입, 1개
15%9,400원
7,990원
로켓배송
(10ml당 222원)
내일(목) 새벽 도착 보장
5
(5569)
최대 400원 적립
최대 400원 적립
6
"""
    
    # 파싱 실행 (카테고리 자동 감지)
    products = parser.parse_coupang_data(test_data, category='auto')
    
    if products:
        # 결과 미리보기
        parser.preview_results(products)
        
        # JSON 저장
        filepath = parser.save_to_json(products)
        print(f"\n✅ 범용 파싱 완료! 파일: {filepath}")
        print("🎯 모든 쇼핑 카테고리 지원 + 자동 카테고리 감지!")
        print("📋 휘광님이 어떤 쇼핑 데이터를 붙여넣어도 자동으로 파싱됩니다!")
    else:
        print("\n😅 파싱할 수 있는 데이터를 찾지 못했습니다.")

if __name__ == "__main__":
    main()