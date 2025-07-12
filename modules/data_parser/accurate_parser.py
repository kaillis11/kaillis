#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
정확한 순위 인식 파서 v3.0
광고 필터링 + 실제 순위 번호 인식
"""

import re
import json
from datetime import datetime
from typing import List, Dict, Optional

class AccurateRankingParser:
    def __init__(self):
        """파서 초기화"""
        self.categories = {
            'macaron': '마카롱',
            'dessert': '디저트',
            'icecream': '아이스크림'
        }
        
        # 광고 키워드 (더 정확한 필터링)
        self.ad_keywords = [
            'AD', '광고', 'Sponsored', '스폰서', 
            '파워클릭', '쇼핑검색광고', '프로모션'
        ]
        
    def parse_with_ranking(self, text: str) -> List[Dict]:
        """실제 순위 번호를 인식하여 파싱"""
        print("📄 정확한 순위 인식 파싱 중...")
        
        products = []
        lines = text.split('\n')
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # 순위 번호 찾기 (단독 숫자)
            rank_match = re.match(r'^(\d+)$', line)
            if rank_match:
                rank_num = int(rank_match.group(1))
                
                # 순위 번호 다음에 나오는 상품 정보 찾기
                product_info = self._find_product_after_rank(lines, i, rank_num)
                if product_info:
                    products.append(product_info)
                    
            i += 1
            
        # 순위 번호가 없는 상품들도 찾기 (광고 아닌 것만)
        additional_products = self._find_products_without_rank(lines)
        
        # 순위 번호가 있는 상품을 우선하고, 나머지는 뒤에 추가
        all_products = products + additional_products
        
        # 중복 제거 (같은 제품명)
        unique_products = []
        seen_names = set()
        for product in all_products:
            if product['name'] not in seen_names:
                unique_products.append(product)
                seen_names.add(product['name'])
        
        return unique_products
    
    def _find_product_after_rank(self, lines: List[str], rank_line_idx: int, rank_num: int) -> Optional[Dict]:
        """순위 번호 다음에 나오는 상품 정보 찾기"""
        
        # 순위 번호 다음 줄부터 최대 10줄까지 확인
        for i in range(rank_line_idx + 1, min(rank_line_idx + 11, len(lines))):
            line = lines[i].strip()
            
            # 광고 스킵
            if any(keyword in line for keyword in self.ad_keywords):
                continue
                
            # 마카롱이 포함된 긴 제품명 찾기
            if '마카롱' in line and len(line) > 20:
                product_name = line
                
                # 이 제품의 가격과 기타 정보 찾기
                product_info = self._extract_product_details(lines, i, product_name, rank_num)
                if product_info:
                    return product_info
                    
        return None
    
    def _extract_product_details(self, lines: List[str], product_line_idx: int, product_name: str, rank: int) -> Optional[Dict]:
        """상품 세부 정보 추출"""
        
        price = None
        original_price = None
        rating = None
        reviews = None
        discount = None
        
        # 상품명 다음 줄부터 최대 8줄까지 확인
        for i in range(product_line_idx + 1, min(product_line_idx + 9, len(lines))):
            line = lines[i].strip()
            
            # 할인된 가격 패턴 (19,960원 -> 19,360원)
            discount_price_match = re.search(r'(\d{1,3}(?:,\d{3})*)\s*원\s*\n?.*?(\d{1,3}(?:,\d{3})*)\s*원', line)
            if discount_price_match and not price:
                original_price = discount_price_match.group(1)
                price = discount_price_match.group(2)
                # 할인율 계산
                if original_price and price:
                    orig = int(original_price.replace(',', ''))
                    curr = int(price.replace(',', ''))
                    discount_rate = round((orig - curr) / orig * 100)
                    discount = f"{discount_rate}%"
            
            # 단일 가격 패턴
            if not price:
                price_match = re.search(r'(\d{1,3}(?:,\d{3})*)\s*원', line)
                if price_match:
                    price = price_match.group(1)
            
            # 할인율 패턴 (할인20%)
            if not discount:
                discount_match = re.search(r'할인(\d+)%', line)
                if discount_match:
                    discount = discount_match.group(1) + '%'
            
            # 평점 패턴 (4.5 또는 5)
            rating_match = re.search(r'^(\d(?:\.\d)?)\s*$', line)
            if rating_match and not rating:
                rating = rating_match.group(1)
                if '.' not in rating:
                    rating = rating + '.0'
            
            # 리뷰 수 패턴 (6327)
            review_match = re.search(r'^\((\d+(?:,\d+)*)\)\s*$', line)
            if review_match and not reviews:
                reviews = review_match.group(1)
        
        if price:  # 가격이 있어야 유효한 상품
            return {
                'name': product_name,
                'price': price,
                'price_numeric': int(price.replace(',', '')),
                'original_price': original_price,
                'rating': rating or '0.0',
                'reviews': reviews or '0',
                'discount': discount,
                'rank': rank,
                'category': 'macaron',
                'category_name': '마카롱',
                'parsed_at': datetime.now().isoformat()
            }
        
        return None
    
    def _find_products_without_rank(self, lines: List[str]) -> List[Dict]:
        """순위 번호가 없는 상품들 찾기 (광고 제외)"""
        products = []
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            # 광고 스킵
            if any(keyword in line for keyword in self.ad_keywords):
                continue
                
            # 마카롱이 포함된 긴 제품명이지만 앞에 순위 번호가 없는 경우
            if '마카롱' in line and len(line) > 20:
                # 이전 줄이 순위 번호가 아닌지 확인
                prev_line = lines[i-1].strip() if i > 0 else ""
                if not re.match(r'^\d+$', prev_line):
                    
                    product_info = self._extract_product_details(lines, i, line, len(products) + 100)  # 임시 순위
                    if product_info:
                        products.append(product_info)
        
        return products
    
    def preview_results(self, products: List[Dict]):
        """결과 미리보기"""
        if not products:
            print("❌ 파싱된 상품이 없습니다.")
            return
            
        print(f"\n🏆 마카롱 실제 순위 TOP {len(products)}")
        print("=" * 100)
        
        for product in products:
            discount_info = ""
            if product.get('discount'):
                discount_info = f" ({product['discount']} 할인)"
            
            original_price_info = ""
            if product.get('original_price'):
                original_price_info = f" (정가: {product['original_price']}원)"
            
            print(f"{product['rank']:2d}위. {product['name']}")
            print(f"     💰 {product['price']}원{discount_info}{original_price_info}")
            print(f"     ⭐ {product['rating']}점 | 📝 {product['reviews']}개 리뷰")
            print()
    
    def save_to_json(self, products: List[Dict]) -> str:
        """JSON 파일로 저장"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"coupang_macaron_accurate_{timestamp}.json"
        
        data = {
            'meta': {
                'title': '쿠팡 마카롱 정확한 순위',
                'total_products': len(products),
                'parsed_at': datetime.now().isoformat(),
                'parser_version': '3.0_accurate_ranking'
            },
            'products': products
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print(f"💾 저장 완료: {filename}")
        return filename

# 휘광님이 제공한 정확한 테스트 데이터
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
14년동안 마카롱만 만들어온 전문점의 정통 프랑스 무색소 수제 마카롱 16구상자 선물세트, 16개, 25g
14년동안 마카롱만 만들어온 전문점의 정통 프랑스 무색소 수제 마카롱 16구상자 선물세트, 16개, 25g
10%28,200원
25,200원
(10g당 630원)
배송비 3,800원
모레(금) 도착 예정
5
(34)
최대 1,260원 적립
최대 1,260원 적립
AD
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
하겐다즈 아이스크림 마카롱 5입 세트 (냉동), 35g, 5개입, 1세트
하겐다즈 아이스크림 마카롱 5입 세트 (냉동), 35g, 5개입, 1세트
26,900원
로켓배송
(10g당 1,537원)
내일(목) 새벽 도착 보장
4.5
(71)
최대 1,345원 적립
최대 1,345원 적립
AD
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

def main():
    """메인 테스트"""
    parser = AccurateRankingParser()
    
    print("🛒 정확한 순위 인식 파서 v3.0")
    print("📋 쿠팡 마카롱 실제 순위 파싱 (광고 필터링 포함)...")
    
    # 파싱 실행
    products = parser.parse_with_ranking(test_data)
    
    if products:
        # 결과 미리보기
        parser.preview_results(products)
        
        # JSON 저장
        filepath = parser.save_to_json(products)
        print(f"\n✅ 테스트 완료! 파일: {filepath}")
        print("🎯 이제 정확한 순위로 WhatToEat 룰렛에 연동할 수 있습니다!")
    else:
        print("\n😅 파싱할 수 있는 데이터를 찾지 못했습니다.")

if __name__ == "__main__":
    main()