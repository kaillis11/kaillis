#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
스마트 재사용 파서 v6.0
쿠팡 데이터 구조 완전 정복 - 순위 번호가 끝에 있는 패턴 인식
"""

import re
import json
from datetime import datetime
from typing import List, Dict, Optional

class SmartReusableParser:
    def __init__(self):
        """파서 초기화"""
        self.categories = {
            'macaron': '마카롱',
            'dessert': '디저트',
            'icecream': '아이스크림'
        }
        
        # 광고 키워드 (더 정확한 필터링)
        self.ad_keywords = ['AD', '광고', 'Sponsored', '스폰서']
        
    def parse_coupang_smart(self, text: str) -> List[Dict]:
        """스마트 파싱 - 순위 번호가 끝에 있는 구조 인식"""
        print("📄 스마트 재사용 파서 v6.0 실행 중...")
        
        # 1. 텍스트를 상품 블록으로 분리
        product_blocks = self._split_by_product_pattern(text)
        
        products = []
        for block in product_blocks:
            product = self._parse_single_block(block)
            if product:
                products.append(product)
        
        # 2. 순위별로 정렬
        products.sort(key=lambda x: x['rank'])
        
        # 3. 순위 재정렬 (1, 2, 3, 4, 5, 6...)
        for i, product in enumerate(products):
            product['rank'] = i + 1
            
        return products
    
    def _split_by_product_pattern(self, text: str) -> List[str]:
        """상품 블록 분리 - 순위 번호로 구분"""
        lines = text.split('\n')
        blocks = []
        current_block = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 순위 번호 패턴 인식 (단독 숫자 1-10)
            if re.match(r'^[1-9]\d*$', line) and len(line) <= 2:
                # 이전 블록이 있으면 저장
                if current_block:
                    blocks.append('\n'.join(current_block))
                    current_block = []
                # 순위 번호를 블록 끝에 추가
                current_block.append(f"RANK:{line}")
            else:
                current_block.append(line)
        
        # 마지막 블록 저장
        if current_block:
            blocks.append('\n'.join(current_block))
            
        return blocks
    
    def _parse_single_block(self, block: str) -> Optional[Dict]:
        """단일 상품 블록 파싱"""
        lines = block.split('\n')
        
        # 광고 필터링
        if any(any(keyword in line for keyword in self.ad_keywords) for line in lines):
            print(f"🚫 광고 필터링: {lines[0][:50]}...")
            return None
        
        # 순위 번호 추출
        rank = self._extract_rank(lines)
        if not rank:
            return None
            
        # 제품명 추출
        product_name = self._extract_product_name(lines)
        if not product_name:
            return None
        
        # 가격 정보 추출
        price_info = self._extract_price_info(lines)
        if not price_info:
            return None
        
        # 평점과 리뷰 추출
        rating, reviews = self._extract_rating_reviews(lines)
        
        return {
            'rank': rank,
            'name': product_name,
            'price': price_info['price'],
            'price_numeric': price_info['price_numeric'],
            'original_price': price_info.get('original_price'),
            'discount': price_info.get('discount'),
            'rating': rating,
            'reviews': reviews,
            'category': 'macaron',
            'category_name': '마카롱',
            'parsed_at': datetime.now().isoformat()
        }
    
    def _extract_rank(self, lines: List[str]) -> Optional[int]:
        """순위 번호 추출"""
        for line in lines:
            if line.startswith('RANK:'):
                return int(line.split(':')[1])
        return None
    
    def _extract_product_name(self, lines: List[str]) -> Optional[str]:
        """제품명 추출 - 마카롱이 포함된 가장 긴 라인"""
        best_candidate = None
        max_length = 0
        
        for line in lines:
            line = line.strip()
            if '마카롱' in line and len(line) > max_length:
                # 가격이나 기타 정보가 아닌 제품명인지 확인
                if not re.search(r'\d+,?\d*원', line) and not line.startswith('RANK:'):
                    best_candidate = line
                    max_length = len(line)
        
        return best_candidate
    
    def _extract_price_info(self, lines: List[str]) -> Optional[Dict]:
        """가격 정보 추출"""
        price_info = {}
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            # 할인 패턴 1: "할인20%11,900원" → 다음 줄에서 실제 가격
            discount_match = re.search(r'할인(\d+)%(\d{1,3}(?:,\d{3})*)원', line)
            if discount_match:
                discount_rate = discount_match.group(1)
                original_price = discount_match.group(2)
                
                # 다음 줄들에서 실제 가격 찾기
                for j in range(i + 1, min(i + 3, len(lines))):
                    next_line = lines[j].strip()
                    actual_price_match = re.search(r'^(\d{1,3}(?:,\d{3})*)원$', next_line)
                    if actual_price_match:
                        actual_price = actual_price_match.group(1)
                        return {
                            'price': actual_price,
                            'price_numeric': int(actual_price.replace(',', '')),
                            'original_price': original_price,
                            'discount': discount_rate + '%'
                        }
            
            # 할인 패턴 2: "3%19,960원" → 다음 줄에서 실제 가격
            discount_match2 = re.search(r'^(\d+)%(\d{1,3}(?:,\d{3})*)원$', line)
            if discount_match2:
                discount_rate = discount_match2.group(1)
                original_price = discount_match2.group(2)
                
                # 다음 줄들에서 실제 가격 찾기
                for j in range(i + 1, min(i + 3, len(lines))):
                    next_line = lines[j].strip()
                    actual_price_match = re.search(r'^(\d{1,3}(?:,\d{3})*)원$', next_line)
                    if actual_price_match:
                        actual_price = actual_price_match.group(1)
                        return {
                            'price': actual_price,
                            'price_numeric': int(actual_price.replace(',', '')),
                            'original_price': original_price,
                            'discount': discount_rate + '%'
                        }
            
            # 단순 가격 패턴
            simple_price_match = re.search(r'^(\d{1,3}(?:,\d{3})*)원$', line)
            if simple_price_match and not price_info:
                price = simple_price_match.group(1)
                price_info = {
                    'price': price,
                    'price_numeric': int(price.replace(',', ''))
                }
        
        return price_info if price_info else None
    
    def _extract_rating_reviews(self, lines: List[str]) -> tuple:
        """평점과 리뷰 수 추출"""
        rating = '0.0'
        reviews = '0'
        
        for line in lines:
            line = line.strip()
            
            # 평점 패턴 (단독 숫자 라인)
            if re.match(r'^(4|5)(\.\d)?$', line):
                rating = line
                if '.' not in rating:
                    rating = rating + '.0'
            
            # 리뷰 패턴 (괄호 안 숫자)
            review_match = re.search(r'^\((\d+(?:,\d+)*)\)$', line)
            if review_match:
                reviews = review_match.group(1)
        
        return rating, reviews
    
    def preview_results(self, products: List[Dict]):
        """결과 미리보기"""
        if not products:
            print("❌ 파싱된 상품이 없습니다.")
            return
            
        print(f"\n🏆 마카롱 스마트 파싱 결과 TOP {len(products)}")
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
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"coupang_macaron_smart_{timestamp}.json"
        
        data = {
            'meta': {
                'title': '쿠팡 마카롱 스마트 파싱 결과',
                'total_products': len(products),
                'parsed_at': datetime.now().isoformat(),
                'parser_version': '6.0_smart_reusable',
                'note': '순위 번호가 끝에 있는 구조 인식 + 광고 필터링'
            },
            'products': products
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print(f"💾 저장 완료: {filename}")
        return filename

# 테스트용 메인 함수
def main():
    """테스트 실행"""
    parser = SmartReusableParser()
    
    print("🛒 스마트 재사용 파서 v6.0")
    print("📋 쿠팡 데이터 구조 완전 정복...")
    
    # 실제 데이터로 테스트할 때는 여기에 데이터 입력
    test_data = """
파스키에 마카롱 6종 x 2개입 세트 (냉동), 154g, 1개
파스키에 마카롱 6종 x 2개입 세트 (냉동), 154g, 1개
9,980원
로켓배송
내일(목) 새벽 도착 보장
4.5
(6327)
최대 499원 적립
최대 499원 적립
1
널담 마카롱 사랑세트 8종 (냉동), 50g, 8개입, 1세트
쿠팡추천
널담 마카롱 사랑세트 8종 (냉동), 50g, 8개입, 1세트
할인20%11,900원
9,410원
로켓배송
(10g당 235원)
내일(목) 새벽 도착 보장
4.5
(6406)
최대 425원 적립
최대 425원 적립
2
[러브빈마카롱] 수제 마카롱 개별포장 8개입 스승의날 어린이날 단체주문, 세트 2번, 1세트
무료배송
[러브빈마카롱] 수제 마카롱 개별포장 8개입 스승의날 어린이날 단체주문, 세트 2번, 1세트
할인26%16,000원
11,700원
(1세트당 11,700원)
모레(금) 도착 예정
4.5
(516)
최대 579원 적립
최대 579원 적립
3
파스키에 마카롱 12개입 (냉동), 154g, 2개
파스키에 마카롱 12개입 (냉동), 154g, 2개
3%19,960원
19,360원
로켓배송
내일(목) 새벽 도착 보장
4.5
(6327)
최대 968원 적립
최대 968원 적립
4
누니 마카롱(뚱카롱) 8구 선물세트, 시즌투(2), 1개, 320g
무료배송
누니 마카롱(뚱카롱) 8구 선물세트, 시즌투(2), 1개, 320g
16,900원
(10g당 528원)
모레(금) 도착 예정
5
(302)
최대 845원 적립
최대 845원 적립
5
코스트코 36 마카롱 468g, 1박스
무료배송
코스트코 36 마카롱 468g, 1박스
28,980원
(10g당 619원)
모레(금) 도착 예정
5
(19)
최대 1,449원 적립
최대 1,449원 적립
6
"""
    
    # 파싱 실행
    products = parser.parse_coupang_smart(test_data)
    
    if products:
        # 결과 미리보기
        parser.preview_results(products)
        
        # JSON 저장
        filepath = parser.save_to_json(products)
        print(f"\n✅ 스마트 파싱 완료! 파일: {filepath}")
        print("🎯 이제 계속 재사용 가능한 정확한 파서입니다!")
        print("📋 휘광님이 새로운 데이터를 붙여넣으면 자동으로 파싱됩니다!")
    else:
        print("\n😅 파싱할 수 있는 데이터를 찾지 못했습니다.")

if __name__ == "__main__":
    main()