#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
범용 쇼핑 데이터 파서 v3.0
쿠팡, 네이버쇼핑 등 다양한 쇼핑몰 데이터 자동 파싱
휘광님이 복사한 어떤 형태의 데이터도 처리 가능
"""

import re
import json
import pyperclip
from datetime import datetime
from typing import List, Dict, Optional, Tuple

class UniversalShoppingParser:
    def __init__(self):
        """범용 파서 초기화"""
        self.categories = {
            'dessert': '디저트',
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
        
    def parse_from_clipboard(self, category: str = 'dessert') -> List[Dict]:
        """클립보드에서 자동으로 데이터 파싱"""
        print(f"📋 클립보드에서 {self.categories.get(category, category)} 데이터 파싱 중...")
        
        try:
            clipboard_text = pyperclip.paste()
            
            if not clipboard_text:
                print("❌ 클립보드가 비어있습니다.")
                return []
                
            print(f"📄 텍스트 길이: {len(clipboard_text)} 문자")
            
            # 스마트 파싱 - 여러 패턴 시도
            products = self._smart_extract(clipboard_text)
            
            # 순위 자동 부여 및 메타데이터
            for idx, product in enumerate(products, 1):
                product['rank'] = idx
                product['category'] = category
                product['category_name'] = self.categories.get(category, category)
                product['parsed_at'] = datetime.now().isoformat()
                product['source'] = 'manual_copy'
                
            print(f"✅ {len(products)}개 상품 파싱 완료!")
            return products
            
        except Exception as e:
            print(f"❌ 파싱 오류: {e}")
            return []
    
    def _smart_extract(self, text: str) -> List[Dict]:
        """스마트 추출 - 다양한 패턴 인식"""
        products = []
        
        # 방법 1: 가격이 포함된 라인을 기준으로 파싱
        lines = text.split('\n')
        current_product = None
        product_buffer = []
        
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
            
            price_found = False
            for pattern in price_patterns:
                price_match = re.search(pattern, line)
                if price_match:
                    price_found = True
                    price_value = price_match.group(1)
                    
                    # 이전 버퍼에서 제품명 찾기
                    product_name = self._extract_product_name(product_buffer)
                    
                    if product_name:
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
                            'original_price': self._extract_original_price(line)
                        }
                        
                        # 배송 정보 찾기
                        delivery = self._extract_delivery(product_buffer + [line])
                        if delivery:
                            product['delivery'] = delivery
                            
                        products.append(product)
                        product_buffer = []  # 버퍼 초기화
                    break
            
            if not price_found:
                # 가격이 없으면 버퍼에 추가
                product_buffer.append(line)
                
        return products[:20]  # 최대 20개
    
    def _extract_product_name(self, buffer: List[str]) -> Optional[str]:
        """버퍼에서 제품명 추출"""
        # 가장 긴 라인이 보통 제품명
        if not buffer:
            return None
            
        # 제품명 패턴
        name_patterns = [
            r'^([가-힣a-zA-Z0-9\s\-\(\)\[\],\.]+)$',  # 기본 패턴
            r'^(.+?)\s*\d+개입',  # "~개입" 앞까지
            r'^(.+?)\s*\d+g',     # "~g" 앞까지
            r'^(.+?)\s*\d+ml',    # "~ml" 앞까지
        ]
        
        # 버퍼를 역순으로 검색 (가격에 가까운 것이 제품명일 확률 높음)
        for line in reversed(buffer[-3:]):  # 최근 3줄만
            for pattern in name_patterns:
                match = re.search(pattern, line)
                if match:
                    name = match.group(1).strip()
                    # 너무 짧거나 긴 이름 제외
                    if 5 < len(name) < 100:
                        return name
                        
        # 패턴 매칭 실패시 가장 긴 라인 반환
        longest = max(buffer[-3:], key=len) if buffer else ""
        return longest if len(longest) > 5 else None
    
    def _extract_reviews(self, text: str) -> str:
        """리뷰 수 추출"""
        patterns = [
            r'(\d+(?:,\d+)*)\s*개?\s*리뷰',
            r'리뷰\s*(\d+(?:,\d+)*)',
            r'\((\d+(?:,\d+)*)\)',  # (1,234) 형태
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        return "0"
    
    def _extract_rating(self, text: str) -> str:
        """평점 추출"""
        patterns = [
            r'(\d\.\d)\s*점',
            r'★\s*(\d\.\d)',
            r'평점\s*(\d\.\d)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        return "0.0"
    
    def _extract_discount(self, text: str) -> Optional[str]:
        """할인율 추출"""
        patterns = [
            r'(\d+)\s*%\s*할인',
            r'(\d+)\s*%↓',
            r'(\d+)\s*%\s*OFF',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return f"{match.group(1)}%"
        return None
    
    def _extract_original_price(self, text: str) -> Optional[str]:
        """원가 추출 (할인 전 가격)"""
        # 취소선이나 작은 글씨로 표시된 가격 찾기
        patterns = [
            r'(\d{1,3}(?:,\d{3})*)\s*원\s*→',  # 10,000원 →
            r'~~(\d{1,3}(?:,\d{3})*)\s*원~~',   # ~~10,000원~~
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        return None
    
    def _extract_delivery(self, lines: List[str]) -> Optional[str]:
        """배송 정보 추출"""
        delivery_keywords = [
            '로켓배송', '무료배송', '내일도착', '오늘도착', 
            '새벽배송', '당일배송', '즉시배송', '택배'
        ]
        
        for line in lines:
            for keyword in delivery_keywords:
                if keyword in line:
                    # 배송 관련 전체 텍스트 반환
                    return line.strip()
        return None
    
    def preview_results(self, products: List[Dict]):
        """결과 미리보기"""
        if not products:
            print("❌ 파싱된 상품이 없습니다.")
            return
            
        print(f"\n🏆 {products[0].get('category_name', '상품')} 순위 TOP {len(products)}")
        print("=" * 80)
        
        for product in products:
            # 할인 정보
            discount_info = f" ({product['discount']} 할인)" if product.get('discount') else ""
            
            print(f"{product['rank']:2d}위. {product['name']}")
            print(f"     💰 {product['price']}원{discount_info}")
            
            if product.get('original_price'):
                print(f"     💸 정가: {product['original_price']}원")
                
            print(f"     ⭐ {product['rating']}점 | 📝 {product['reviews']}개 리뷰")
            
            if product.get('delivery'):
                print(f"     🚚 {product['delivery']}")
            print()
    
    def save_to_json(self, products: List[Dict], filename: Optional[str] = None) -> str:
        """JSON 파일로 저장"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            category = products[0]['category'] if products else 'unknown'
            filename = f"shopping_{category}_{timestamp}.json"
            
        data = {
            'meta': {
                'total_products': len(products),
                'parsed_at': datetime.now().isoformat(),
                'parser_version': '3.0',
                'method': 'clipboard_smart_parsing'
            },
            'products': products
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print(f"💾 저장 완료: {filename}")
        return filename
    
    def parse_text_directly(self, text: str, category: str = 'dessert') -> List[Dict]:
        """텍스트 직접 파싱 (테스트용)"""
        products = self._smart_extract(text)
        
        for idx, product in enumerate(products, 1):
            product['rank'] = idx
            product['category'] = category
            product['category_name'] = self.categories.get(category, category)
            product['parsed_at'] = datetime.now().isoformat()
            
        return products

def main():
    """메인 실행 함수"""
    parser = UniversalShoppingParser()
    
    print("🛒 범용 쇼핑 데이터 파서 v3.0")
    print("📋 쇼핑몰에서 상품 목록을 복사해주세요 (Ctrl+A → Ctrl+C)")
    print("   지원: 쿠팡, 네이버쇼핑, 11번가 등 모든 쇼핑몰")
    
    input("\n복사 완료 후 Enter를 눌러주세요...")
    
    # 카테고리 선택
    print("\n📂 카테고리 선택:")
    categories = list(parser.categories.items())
    for i, (key, name) in enumerate(categories):
        print(f"  {i+1}. {name} ({key})")
    
    try:
        choice = int(input("\n번호 입력 (기본값: 1): ").strip() or "1") - 1
        category = categories[choice][0]
    except:
        category = 'dessert'
    
    # 파싱 실행
    products = parser.parse_from_clipboard(category)
    
    if products:
        # 결과 미리보기
        parser.preview_results(products)
        
        # 저장 여부
        save = input("\n💾 JSON으로 저장하시겠습니까? (y/n): ").strip().lower()
        if save in ['y', 'yes', '예', 'ㅇ']:
            filepath = parser.save_to_json(products)
            print(f"\n✅ 완료! 파일 위치: {filepath}")
            print("🎯 이제 WhatToEat 룰렛에 연동할 수 있습니다!")
    else:
        print("\n😅 파싱할 수 있는 데이터를 찾지 못했습니다.")
        print("💡 팁: 상품명과 가격이 포함된 부분을 복사해보세요!")

if __name__ == "__main__":
    main()