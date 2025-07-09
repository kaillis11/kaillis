#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
심플 범용 파서 v1.0
모든 쿠팡 쇼핑 데이터를 처리하는 단일 파서
사용법: parser.parse(data, category='과자')
"""

import re
import json
from datetime import datetime
from typing import List, Dict, Optional

class SimpleUniversalParser:
    def __init__(self):
        """파서 초기화"""
        self.ad_keywords = ['AD', '광고', 'Sponsored', '스폰서']
        
    def parse(self, text: str, category: str = '상품') -> List[Dict]:
        """범용 쿠팡 데이터 파싱"""
        print(f"🔍 심플 범용 파서 v1.0 - [{category}] 카테고리 파싱 중...")
        
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        products = []
        i = 0
        
        while i < len(lines):
            # 제품명 라인 찾기 (한글 + 브랜드명 + 상품정보 패턴)
            if self._looks_like_product_name(lines[i]):
                product_name = lines[i]
                
                # 순위 번호 찾기
                rank = self._find_rank_in_block(lines, i)
                if rank is None:
                    i += 1
                    continue
                
                # 광고 확인 (해당 제품 블록에서만)
                if self._is_ad_in_block(lines, i, rank):
                    print(f"🚫 광고 필터링: {rank}위 {product_name[:30]}...")
                    i += 1
                    continue
                
                # 이미 같은 순위의 제품이 있는지 확인 (중복 제품명 처리)
                if any(p.get('rank') == rank for p in products):
                    i += 1
                    continue
                
                # 제품 정보 추출
                product_info = self._extract_info(lines, i, product_name, rank, category)
                if product_info:
                    products.append(product_info)
                    print(f"✅ 파싱 완료: {rank}위 {product_name[:30]}...")
                    
            i += 1
        
        # 순위별 정렬
        products.sort(key=lambda x: x.get('rank', 999))
        
        return products
    
    def _looks_like_product_name(self, line: str) -> bool:
        """제품명 라인인지 판단 - 오르벨 조언 반영"""
        # 기본 조건: 한글 포함 + 적당한 길이
        if not re.search(r'[가-힣]', line) or len(line) < 5:
            return False
        
        # 제외 패턴: 숫자만, 단순 텍스트, 배송 정보 등
        exclude_patterns = [
            r'^\d+$',                    # 숫자만
            r'^[0-9,]+원$',             # 가격만
            r'^\d+%[0-9,]+원$',         # 할인가격
            r'^할인\d+%[0-9,]+원$',      # 할인23%20,900원 패턴 (오르벨 조언)
            r'^쿠폰할인\d+%[0-9,]+원$',  # 쿠폰할인37%15,840원 패턴
            r'^로켓배송$|^배송$|^무료배송$',    # 배송 정보
            r'^\([^)]+\)$',             # 괄호 안 텍스트
            r'^[0-5](\.\d)?$',          # 평점
            r'^내일.*도착|^모레.*도착',      # 도착 정보
            r'^최대.*적립',               # 적립 정보
            r'^쿠팡추천$|^추천$',          # 추천 표시
        ]
        
        for pattern in exclude_patterns:
            if re.match(pattern, line):
                return False
        
        # 오르벨 조언: 제품명 형태 필터링
        # 할인/가격 관련 키워드가 포함된 짧은 텍스트 제외
        price_noise_keywords = ['할인', '원', '%', '쿠폰', '적립', '무료', '배송']
        if len(line) < 15 and any(keyword in line for keyword in price_noise_keywords):
            return False
        
        return True
    
    def _find_rank_in_block(self, lines: List[str], start_idx: int) -> Optional[int]:
        """제품 블록에서 순위 번호 찾기 - 리뷰 번호 이후의 순위 찾기"""
        # 제품명 이후 최대 30라인 확인
        end_idx = min(len(lines), start_idx + 30)
        
        found_review = False
        
        for i in range(start_idx + 1, end_idx):
            line = lines[i].strip()
            
            # 다음 제품명이 나오면 중단
            if i != start_idx and self._looks_like_product_name(line):
                break
            
            # 리뷰 번호 패턴 확인 (12345) 형태
            if re.match(r'^\(\d+(?:,\d+)*\)$', line):
                found_review = True
                continue
            
            # 리뷰 번호를 찾은 후에만 순위 번호 찾기
            if found_review and re.match(r'^(20|1\d|[1-9])$', line):
                return int(line)
        
        return None
    
    def _is_ad_in_block(self, lines: List[str], start_idx: int, rank: int) -> bool:
        """해당 제품 블록에서만 광고 여부 확인"""
        # 제품명 이후 순위 번호까지만 확인
        end_idx = min(len(lines), start_idx + 30)
        
        for i in range(start_idx + 1, end_idx):
            line = lines[i].strip()
            
            # 순위 번호에 도달하면 중단
            if line == str(rank):
                break
                
            # AD 키워드 확인
            if any(keyword in line for keyword in self.ad_keywords):
                return True
        
        return False
    
    def _extract_info(self, lines: List[str], start_idx: int, product_name: str, rank: int, category: str) -> Optional[Dict]:
        """제품 정보 추출"""
        price = None
        original_price = None
        discount = None
        rating = '0.0'
        reviews = '0'
        
        # 제품명 이후 순위 번호까지 확인
        end_idx = min(len(lines), start_idx + 30)
        
        for i in range(start_idx + 1, end_idx):
            line = lines[i].strip()
            
            # 순위 번호에 도달하면 중단
            if line == str(rank):
                break
            
            # 할인율 + 원가 패턴 (예: 29%7,800원)
            discount_price_match = re.search(r'^(\d+)%(\d{1,3}(?:,\d{3})*)원$', line)
            if discount_price_match:
                discount = discount_price_match.group(1) + '%'
                original_price = discount_price_match.group(2)
                
                # 다음 줄에서 실제 가격 찾기
                for j in range(i + 1, min(i + 4, len(lines))):
                    next_line = lines[j].strip()
                    actual_price_match = re.search(r'^(\d{1,3}(?:,\d{3})*)원$', next_line)
                    if actual_price_match:
                        price = actual_price_match.group(1)
                        break
            
            # 쿠폰할인 패턴 (예: 쿠폰할인37%15,840원)
            coupon_match = re.search(r'^쿠폰할인(\d+)%(\d{1,3}(?:,\d{3})*)원$', line)
            if coupon_match:
                discount = coupon_match.group(1) + '%'
                original_price = coupon_match.group(2)
                
                # 다음 줄에서 실제 가격 찾기
                for j in range(i + 1, min(i + 4, len(lines))):
                    next_line = lines[j].strip()
                    actual_price_match = re.search(r'^(\d{1,3}(?:,\d{3})*)원$', next_line)
                    if actual_price_match:
                        price = actual_price_match.group(1)
                        break
            
            # 일반 가격 패턴
            if not price:
                price_match = re.search(r'^(\d{1,3}(?:,\d{3})*)원$', line)
                if price_match:
                    price = price_match.group(1)
            
            # 평점 패턴 (0.0 ~ 5.0)
            if re.match(r'^[0-5](\.\d)?$', line):
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
                'parsed_at': datetime.now().isoformat(),
                'rank': rank
            }
        
        return None
    
    def preview_results(self, products: List[Dict]):
        """결과 미리보기"""
        if not products:
            print("❌ 파싱된 상품이 없습니다.")
            return
        
        category = products[0].get('category', '상품') if products else '상품'
        print(f"\n📋 {category} 파싱 결과 (총 {len(products)}개)")
        print("=" * 80)
        
        for product in products:
            price_str = f"{product['price']}원"
            if product.get('discount') and product.get('original_price'):
                price_str += f" ({product['discount']} 할인, 정가 {product['original_price']}원)"
            
            print(f"🛒 {product['rank']:2d}위 | {product['name'][:40]:<40}")
            print(f"     💰 {price_str}")
            print(f"     ⭐ {product['rating']}점 | 📝 {product['reviews']}개 리뷰")
            print()
    
    def save_to_json(self, products: List[Dict], filename: str = None) -> str:
        """JSON 파일로 저장"""
        if not products:
            return ""
            
        category = products[0].get('category', '상품')
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"coupang_{category}_{timestamp}.json"
        
        data = {
            'meta': {
                'title': f'쿠팡 {category} 순위',
                'total_products': len(products),
                'category': category,
                'parsed_at': datetime.now().isoformat()
            },
            'products': products
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 JSON 저장 완료: {filename}")
        return filename

def main():
    """테스트 실행"""
    # 테스트 데이터 (과자)
    test_data = """
뉴트리오코 초콜릿맛 웨이퍼, 12g, 30개
뉴트리오코 초콜릿맛 웨이퍼, 12g, 30개
29%7,800원
5,500원
로켓배송
(10g당 153원)
내일(목) 도착 보장
5
(3109)
최대 275원 적립
최대 275원 적립
1
뉴트리오코 밀크맛 웨이퍼, 360g, 1개
쿠팡추천
뉴트리오코 밀크맛 웨이퍼, 360g, 1개
29%7,800원
5,500원
로켓배송
(10g당 153원)
내일(목) 도착 보장
5
(3568)
최대 275원 적립
최대 275원 적립
2
"""

    parser = SimpleUniversalParser()
    
    # 과자 카테고리로 테스트
    products = parser.parse(test_data, category='과자')
    
    if products:
        parser.preview_results(products)
        filename = parser.save_to_json(products)
        print(f"✅ 파싱 완료! {len(products)}개 상품")
    else:
        print("❌ 파싱 실패")

if __name__ == "__main__":
    main()