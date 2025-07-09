#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
쿠팡 데이터 파싱 테스트
"""

import re
import json
from datetime import datetime
from typing import List, Dict

class CoupangDataParser:
    def __init__(self):
        """쿠팡 데이터 파서 초기화"""
        self.categories = {
            'dessert': '디저트',
            'icecream': '아이스크림', 
            'frozen': '냉동식품',
            'snack': '과자',
            'drink': '음료'
        }
        
        # 광고 키워드 (제외할 항목들)
        self.ad_keywords = [
            'AD', '광고', 'Sponsored', '스폰서', 
            '프로모션', '특가', '쿠팡추천'
        ]
        
    def parse_text_data(self, text_content: str, category: str = 'dessert') -> List[Dict]:
        """텍스트 데이터를 파싱하여 순위 추출"""
        print(f"📋 {self.categories.get(category, category)} 데이터 파싱...")
        
        try:
            print(f"📄 텍스트 길이: {len(text_content)} 문자")
            
            # 파싱 실행
            products = self._extract_products(text_content)
            
            # 카테고리 정보 추가
            for i, product in enumerate(products):
                product['rank'] = i + 1  # 순위 재정렬
                product['category'] = category
                product['category_name'] = self.categories.get(category, category)
                product['parsed_at'] = datetime.now().isoformat()
                
            print(f"✅ {len(products)}개 상품 파싱 완료!")
            return products
            
        except Exception as e:
            print(f"❌ 파싱 중 오류: {e}")
            return []
    
    def _extract_products(self, text: str) -> List[Dict]:
        """텍스트에서 상품 정보 추출"""
        products = []
        
        # 텍스트를 줄 단위로 분할
        lines = text.split('\n')
        
        # 상품 패턴 찾기
        # 패턴: 상품명이 포함된 줄 다음에 가격이 오는 구조
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # 광고 필터링
            if self._is_advertisement(line):
                continue
            
            # 순위 번호가 명시적으로 적힌 라인 찾기 (1, 2, 3... 등)
            rank_match = re.search(r'^(\d+)$', line)
            if rank_match:
                rank_num = int(rank_match.group(1))
                
                # 이전 몇 줄에서 상품명과 가격 찾기
                product_info = self._find_product_info_around(lines, i, rank_num)
                if product_info:
                    products.append(product_info)
                    
        # 순위가 명시적이지 않은 경우 다른 방법으로 추출
        if len(products) < 5:
            print("🔄 순위 번호가 적어서 패턴 매칭으로 재시도...")
            products = self._extract_by_pattern(text)
            
        return products[:15]  # 최대 15개만
    
    def _find_product_info_around(self, lines: List[str], rank_line_idx: int, rank: int) -> Dict:
        """순위 번호 주변에서 상품 정보 찾기"""
        # 순위 번호 앞뒤 5줄 정도에서 상품명과 가격 찾기
        start_idx = max(0, rank_line_idx - 10)
        end_idx = min(len(lines), rank_line_idx + 5)
        
        product_name = None
        product_price = None
        reviews = "0"
        rating = "0.0"
        
        for i in range(start_idx, end_idx):
            line = lines[i].strip()
            if not line:
                continue
                
            # 가격 패턴 찾기
            price_match = re.search(r'(\d{1,3}(?:,\d{3})*)\s*원', line)
            if price_match and not product_price:
                product_price = price_match.group(1)
                
            # 리뷰 수 패턴
            review_match = re.search(r'\((\d{1,3}(?:,\d{3})*)\)', line)
            if review_match:
                reviews = review_match.group(1)
                
            # 평점 패턴
            rating_match = re.search(r'^(\d\.\d)$', line)
            if rating_match:
                rating = rating_match.group(1)
                
            # 상품명 후보 (한글, 영문 포함하고 충분히 긴 텍스트)
            if len(line) > 10 and not product_name:
                # 특정 키워드가 포함된 라인을 상품명으로 간주
                if any(keyword in line for keyword in ['케이크', '초콜릿', '쿠키', '파이', '떡', '도넛', '아이스크림', '젤리', '브라우니']):
                    # 불필요한 정보 제거
                    clean_name = re.sub(r'\(\d+g당.*?\)', '', line)  # (10g당 XXX원) 제거
                    clean_name = re.sub(r'로켓배송', '', clean_name)
                    clean_name = re.sub(r'무료배송', '', clean_name)
                    clean_name = re.sub(r'내일.*?도착.*?', '', clean_name)
                    clean_name = clean_name.strip()
                    
                    if len(clean_name) > 5:
                        product_name = clean_name
        
        if product_name and product_price:
            return {
                'rank': rank,
                'name': product_name,
                'price': product_price,
                'price_numeric': int(product_price.replace(',', '')),
                'reviews': reviews,
                'rating': rating
            }
        return None
    
    def _extract_by_pattern(self, text: str) -> List[Dict]:
        """패턴 매칭으로 상품 추출"""
        products = []
        
        # 명확한 상품 패턴들
        product_patterns = [
            r'마켓오 브라우니.*?(\d{1,3}(?:,\d{3})*)\s*원',
            r'배스킨라빈스.*?(\d{1,3}(?:,\d{3})*)\s*원',
            r'뉴트리오코.*?(\d{1,3}(?:,\d{3})*)\s*원',
            r'널담.*?(\d{1,3}(?:,\d{3})*)\s*원',
            r'쿠캣.*?(\d{1,3}(?:,\d{3})*)\s*원',
            r'던킨.*?(\d{1,3}(?:,\d{3})*)\s*원',
            r'젤리젤리.*?(\d{1,3}(?:,\d{3})*)\s*원',
            r'다네시타.*?(\d{1,3}(?:,\d{3})*)\s*원',
            r'오리온.*?(\d{1,3}(?:,\d{3})*)\s*원'
        ]
        
        for pattern in product_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                price = match.group(1)
                # 상품명 추출 시도
                name_start = max(0, match.start() - 100)
                name_text = text[name_start:match.start()]
                
                # 줄바꿈으로 분할해서 마지막 유의미한 줄 가져오기
                name_lines = [line.strip() for line in name_text.split('\n') if line.strip()]
                if name_lines:
                    product_name = name_lines[-1]
                    if len(product_name) > 5:
                        products.append({
                            'rank': len(products) + 1,
                            'name': product_name,
                            'price': price,
                            'price_numeric': int(price.replace(',', '')),
                            'reviews': '0',
                            'rating': '0.0'
                        })
                        
        return products
    
    def _is_advertisement(self, text: str) -> bool:
        """광고성 텍스트인지 확인"""
        for keyword in self.ad_keywords:
            if keyword in text:
                return True
        return False
    
    def preview_results(self, products: List[Dict]):
        """결과 미리보기"""
        if not products:
            print("❌ 파싱된 상품이 없습니다.")
            return
            
        print(f"\n🏆 {products[0].get('category_name', '상품')} 순위 TOP {len(products)}")
        print("=" * 70)
        
        for product in products:
            print(f"{product['rank']:2d}. {product['name']}")
            print(f"    💰 {product['price']}원 | ⭐ {product['rating']}점 | 📝 {product['reviews']}개 리뷰")
            print()

def test_with_file():
    """파일에서 데이터 읽어서 테스트"""
    parser = CoupangDataParser()
    
    print("🛒 쿠팡 데이터 파서 테스트 시작")
    
    # 파일에서 텍스트 읽기
    try:
        with open('test_coupang_data.txt', 'r', encoding='utf-8') as f:
            text_content = f.read()
    except FileNotFoundError:
        print("❌ test_coupang_data.txt 파일이 없습니다.")
        return
    
    # 파싱 실행
    products = parser.parse_text_data(text_content, 'dessert')
    
    if products:
        # 결과 미리보기
        parser.preview_results(products)
        
        # JSON으로 저장
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"coupang_dessert_{timestamp}.json"
        
        data = {
            'meta': {
                'category': 'dessert',
                'category_name': '디저트',
                'total_products': len(products),
                'parsed_at': datetime.now().isoformat(),
                'source': 'coupang_manual_copy'
            },
            'products': products
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print(f"💾 데이터 저장: {output_file}")
    else:
        print("😞 파싱할 수 있는 상품 데이터가 없습니다.")

if __name__ == "__main__":
    test_with_file()