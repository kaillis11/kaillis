#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
쿠팡 데이터 클립보드 파싱 시스템
휘광님이 복사한 텍스트에서 순위 데이터 자동 추출
"""

import re
import json
import pyperclip
from datetime import datetime
from typing import List, Dict, Optional

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
            '광고', 'AD', 'Sponsored', '스폰서', 
            '프로모션', '특가', '쿠팡초이스'
        ]
        
    def parse_clipboard_data(self, category: str = 'dessert') -> List[Dict]:
        """클립보드 데이터를 파싱하여 순위 추출"""
        print(f"📋 클립보드에서 {self.categories.get(category, category)} 데이터 파싱...")
        
        try:
            # 클립보드에서 텍스트 가져오기
            clipboard_text = pyperclip.paste()
            
            if not clipboard_text:
                print("❌ 클립보드가 비어있습니다.")
                return []
                
            print(f"📄 클립보드 텍스트 길이: {len(clipboard_text)} 문자")
            
            # 파싱 실행
            products = self._extract_products(clipboard_text)
            
            # 카테고리 정보 추가
            for product in products:
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
        
        current_product = {}
        rank_counter = 1
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # 광고 필터링
            if self._is_advertisement(line):
                continue
                
            # 가격 패턴 찾기 (숫자,숫자원 또는 숫자원)
            price_match = re.search(r'(\d{1,3}(?:,\d{3})*)\s*원', line)
            
            # 제품명 후보 찾기 (한글, 영문, 숫자 조합)
            product_name_match = re.search(r'([가-힣a-zA-Z0-9\s\-\(\)]+)', line)
            
            # 리뷰/평점 패턴
            review_match = re.search(r'(\d+(?:,\d+)*)\s*개?\s*리뷰', line)
            rating_match = re.search(r'(\d\.\d)\s*점', line)
            
            if price_match and product_name_match:
                # 새 상품 발견
                if current_product and 'name' in current_product:
                    products.append(current_product)
                    rank_counter += 1
                
                current_product = {
                    'rank': rank_counter,
                    'name': product_name_match.group(1).strip(),
                    'price': price_match.group(1),
                    'price_numeric': int(price_match.group(1).replace(',', '')),
                    'reviews': review_match.group(1) if review_match else '0',
                    'rating': rating_match.group(1) if rating_match else '0.0'
                }
                
        # 마지막 상품 추가
        if current_product and 'name' in current_product:
            products.append(current_product)
            
        return products[:20]  # 최대 20개만
    
    def _is_advertisement(self, text: str) -> bool:
        """광고성 텍스트인지 확인"""
        for keyword in self.ad_keywords:
            if keyword in text:
                return True
        return False
    
    def save_to_json(self, products: List[Dict], category: str = 'dessert') -> str:
        """JSON 파일로 저장"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"coupang_{category}_{timestamp}.json"
        filepath = f"/mnt/d/ai/project_hub/active_projects/WhatToEat/data/{filename}"
        
        data = {
            'meta': {
                'category': category,
                'category_name': self.categories.get(category, category),
                'total_products': len(products),
                'parsed_at': datetime.now().isoformat(),
                'source': 'coupang_manual_copy'
            },
            'products': products
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print(f"💾 데이터 저장: {filepath}")
        return filepath
    
    def preview_results(self, products: List[Dict]):
        """결과 미리보기"""
        if not products:
            print("❌ 파싱된 상품이 없습니다.")
            return
            
        print(f"\n🏆 {products[0].get('category_name', '상품')} 순위 TOP {len(products)}")
        print("=" * 60)
        
        for product in products:
            print(f"{product['rank']:2d}. {product['name']}")
            print(f"    💰 {product['price']}원 | ⭐ {product['rating']}점 | 📝 {product['reviews']}개 리뷰")
            print()

def main():
    """메인 함수 - 테스트 및 실행"""
    parser = CoupangDataParser()
    
    print("🛒 쿠팡 데이터 파서 시작")
    print("📋 먼저 쿠팡에서 상품 데이터를 복사해주세요 (Ctrl+A → Ctrl+C)")
    
    input("복사 완료 후 Enter를 눌러주세요...")
    
    # 카테고리 선택
    print("\n📂 카테고리를 선택해주세요:")
    for key, name in parser.categories.items():
        print(f"  {key}: {name}")
    
    category = input("\n카테고리 입력 (기본값: dessert): ").strip() or 'dessert'
    
    # 파싱 실행
    products = parser.parse_clipboard_data(category)
    
    if products:
        # 결과 미리보기
        parser.preview_results(products)
        
        # 저장 확인
        save_confirm = input("💾 JSON 파일로 저장하시겠습니까? (y/n): ").strip().lower()
        if save_confirm in ['y', 'yes', '예', 'ㅇ']:
            filepath = parser.save_to_json(products, category)
            print(f"✅ 저장 완료: {filepath}")
        else:
            print("💨 저장하지 않고 종료합니다.")
    else:
        print("😞 파싱할 수 있는 상품 데이터가 없습니다.")

if __name__ == "__main__":
    main()