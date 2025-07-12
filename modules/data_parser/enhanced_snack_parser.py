#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
과자 전용 강화 파서 v1.0
과자 데이터의 정확한 순위 파싱을 위한 전용 파서
"""

import re
import json
from datetime import datetime
from typing import List, Dict, Optional

class EnhancedSnackParser:
    def __init__(self):
        """파서 초기화"""
        self.ad_keywords = ['AD', '광고', 'Sponsored', '스폰서']
        
        # 과자 브랜드 및 제품명 키워드 (더 포괄적)
        self.snack_keywords = [
            '뉴트리오코', '마켓오', '구운김', '오리온', '스낵365', '농심', 
            '배스킨라빈스', '롯데웰푸드', '해태제과', '칙촉', '브라우니', 
            '웨이퍼', '과자', '스낵', '초코파이', '사브레', '메론킥',
            '쿠키', '비스킷', '파이', '크렘'
        ]
        
    def parse_snack_data(self, text: str) -> List[Dict]:
        """과자 데이터 파싱"""
        print(f"🍪 과자 전용 강화 파서 v1.0 실행 중...")
        
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        products = []
        i = 0
        
        while i < len(lines):
            # 제품명 라인 찾기 (과자 키워드 포함)
            if self._is_snack_product_line(lines[i]):
                product_name = lines[i]
                
                # 순위 번호 찾기 (제품 블록 끝에서)
                rank = self._find_rank_number(lines, i)
                if rank is None:
                    i += 1
                    continue
                
                # 광고 확인 (더 정확한 범위)
                if self._is_advertisement_precise(lines, i, rank):
                    print(f"🚫 광고 필터링: {rank}위 {product_name[:30]}...")
                    i += 1
                    continue
                
                # 제품 정보 추출
                product_info = self._extract_snack_info(lines, i, product_name, rank)
                if product_info:
                    products.append(product_info)
                    print(f"✅ 파싱 완료: {rank}위 {product_name[:30]}...")
                    
            i += 1
        
        # 순위별 정렬
        products.sort(key=lambda x: x.get('rank', 999))
        
        return products
    
    def _is_snack_product_line(self, line: str) -> bool:
        """과자 제품명 라인인지 확인"""
        line_lower = line.lower()
        for keyword in self.snack_keywords:
            if keyword.lower() in line_lower:
                return True
        return False
    
    def _find_rank_number(self, lines: List[str], start_idx: int) -> Optional[int]:
        """제품 블록에서 순위 번호 찾기"""
        # 제품명 이후 최대 25라인 확인
        end_idx = min(len(lines), start_idx + 25)
        
        for i in range(start_idx + 1, end_idx):
            line = lines[i].strip()
            
            # 다음 제품명이 나오면 중단
            if i != start_idx and self._is_snack_product_line(line):
                break
                
            # 순위 번호 패턴 (1~10)
            if re.match(r'^(10|[1-9])$', line):
                return int(line)
        
        return None
    
    def _is_advertisement_precise(self, lines: List[str], start_idx: int, rank: int) -> bool:
        """정확한 광고 여부 확인"""
        # 제품명 이후 순위 번호 전까지만 확인
        end_idx = min(len(lines), start_idx + 25)
        
        for i in range(start_idx + 1, end_idx):
            line = lines[i].strip()
            
            # 순위 번호에 도달하면 중단
            if line == str(rank):
                break
                
            # AD 키워드 확인
            for keyword in self.ad_keywords:
                if keyword in line:
                    return True
        
        return False
    
    def _extract_snack_info(self, lines: List[str], start_idx: int, product_name: str, rank: int) -> Optional[Dict]:
        """과자 제품 정보 추출"""
        price = None
        original_price = None
        discount = None
        rating = '0.0'
        reviews = '0'
        
        # 제품명 이후 순위 번호까지 확인
        end_idx = min(len(lines), start_idx + 25)
        
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
                for j in range(i + 1, min(i + 3, len(lines))):
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
            
            # 평점 패턴 (4.5, 5.0, 2.0 등)
            if re.match(r'^[2-5](\.\d)?$', line):
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
                'category': 'snack',
                'category_name': '간식',
                'parsed_at': datetime.now().isoformat(),
                'rank': rank
            }
        
        return None
    
    def preview_results(self, products: List[Dict]):
        """결과 미리보기"""
        if not products:
            print("❌ 파싱된 상품이 없습니다.")
            return
        
        print(f"\n📋 과자 파싱 결과 (총 {len(products)}개)")
        print("=" * 80)
        
        for product in products:
            price_str = f"{product['price']}원"
            if product.get('discount') and product.get('original_price'):
                price_str += f" ({product['discount']} 할인, 정가 {product['original_price']}원)"
            
            print(f"🍪 {product['rank']:2d}위 | {product['name'][:40]:<40}")
            print(f"     💰 {price_str}")
            print(f"     ⭐ {product['rating']}점 | 📝 {product['reviews']}개 리뷰")
            print()
    
    def save_to_json(self, products: List[Dict], filename: str = None) -> str:
        """JSON 파일로 저장"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"snack_enhanced_{timestamp}.json"
        
        data = {
            'meta': {
                'title': '쿠팡 과자 순위 (강화 파서)',
                'total_products': len(products),
                'category': 'snack',
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
    # 과자 데이터 (휘광님 제공)
    snack_data = """
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
마켓오 브라우니 제주말차 12개입, 240g, 1개
마켓오 브라우니 제주말차 12개입, 240g, 1개
5%5,280원
5,010원
로켓배송
(10g당 209원)
내일(목) 도착 보장
5
(3254)
최대 250원 적립
최대 250원 적립
3
구운김 달콤 쌀과자, 1개, 900g
구운김 달콤 쌀과자, 1개, 900g
8,770원
로켓배송
(10g당 97원)
내일(목) 도착 보장
5
(661)
최대 439원 적립
최대 439원 적립
AD
오리온 와우스낵 선물세트 16팩, 포카칩 + 꼬북칩 + 오감자 + 돌아온썬칩, 1세트
오리온 와우스낵 선물세트 16팩, 포카칩 + 꼬북칩 + 오감자 + 돌아온썬칩, 1세트
12%11,800원
10,320원
로켓배송
(1세트당 10,320원)
내일(목) 도착 보장
5
(18149)
최대 516원 적립
최대 516원 적립
4
[스낵365] 개꿀맛 10종 포카칩 꼬북칩 콘칩 꼬깔콘 치토스 스낵 과자세트, 1개
[스낵365] 개꿀맛 10종 포카칩 꼬북칩 콘칩 꼬깔콘 치토스 스낵 과자세트, 1개
13,800원
로켓배송
(1세트당 13,800원)
내일(목) 도착 보장
4.5
(2194)
최대 690원 적립
최대 690원 적립
5
농심 과자 세트, 과자 5종, 1세트
농심 과자 세트, 과자 5종, 1세트
8%15,910원
14,500원
로켓배송
(1세트당 14,500원)
내일(목) 도착 보장
5
(3334)
최대 725원 적립
최대 725원 적립
AD
배스킨라빈스 쫀떡궁합 파이, 264g, 3개
배스킨라빈스 쫀떡궁합 파이, 264g, 3개
쿠폰할인37%15,840원
9,900원
로켓배송
(10g당 125원)
내일(목) 도착 보장
5
(673)
최대 495원 적립
최대 495원 적립
6
롯데웰푸드 칙촉, 168g, 2개
롯데웰푸드 칙촉, 168g, 2개
42%9,600원
5,500원
로켓배송
(10g당 164원)
내일(목) 도착 보장
5
(43416)
최대 275원 적립
최대 275원 적립
7
오리온 콤보 초코파이 정 39g x 12p + 카스타드 23g x 12p, 744g, 1개
오리온 콤보 초코파이 정 39g x 12p + 카스타드 23g x 12p, 744g, 1개
36%12,750원
8,050원
로켓배송
(10g당 108원)
내일(목) 도착 보장
5
(29727)
최대 403원 적립
최대 403원 적립
8
해태제과 사브레 초코크렘, 204g, 1개
해태제과 사브레 초코크렘, 204g, 1개
25%4,600원
3,450원
로켓배송
(10g당 169원)
내일(목) 도착 보장
5
(973)
최대 173원 적립
최대 173원 적립
9
농심 메론킥, 60g, 1개
농심 메론킥, 60g, 1개
할인52%2,500원
1,200원
(10g당 200원)
배송비 2,500원
모레(금) 도착 예정
5
(2526)
최대 60원 적립
최대 60원 적립
10
"""

    parser = EnhancedSnackParser()
    products = parser.parse_snack_data(snack_data)
    
    if products:
        parser.preview_results(products)
        filename = parser.save_to_json(products)
        print(f"✅ 과자 데이터 파싱 완료! {len(products)}개 제품")
    else:
        print("❌ 파싱 실패")

if __name__ == "__main__":
    main()