#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
하이브리드 대용량과자 파서 v1.0
90% 자동 파싱 + 10% ATLAS MCP 보완 + 수동 검증
휘광님 요구사항: 실용적 효율성 극대화
"""

import re
import json
from datetime import datetime
from typing import List, Dict, Optional

class HybridSnackParser:
    def __init__(self):
        """파서 초기화"""
        self.category = '대용량과자'
        
        # 광고/노이즈 키워드 (오르벨 조언 반영)
        self.noise_keywords = [
            'AD', '광고', '할인', '%', '무료배송', '로켓배송', 
            '적립', '쿠팡추천', '최대', '보장'
        ]
        
        # 정상 제품명 패턴 (길이 15자 이상 + 브랜드명 포함)
        self.valid_product_patterns = [
            r'새우깡', r'뉴트리오코', r'팜스웰', r'카디', r'신흥', 
            r'재미스', r'롯데웰푸드', r'크라운', r'오리온', r'농심'
        ]
        
    def parse_coupang_snacks(self, text: str) -> List[Dict]:
        """90% 자동 파싱"""
        print("🚀 하이브리드 대용량과자 파서 v1.0 실행...")
        
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        products = []
        i = 0
        
        while i < len(lines):
            # 순위 숫자 찾기 (1, 2, 3, ...)
            if self._is_rank_number(lines[i]):
                rank = int(lines[i])
                print(f"🔍 {rank}위 검색 중...")
                
                # 다음 줄에서 제품명 찾기
                product_info = self._extract_ranked_product(lines, i, rank)
                if product_info:
                    products.append(product_info)
                    print(f"✅ {rank}위 파싱 완료: {product_info['name'][:30]}...")
                else:
                    print(f"❌ {rank}위 파싱 실패")
                    
            i += 1
        
        return products
    
    def _is_rank_number(self, line: str) -> bool:
        """순위 숫자인지 확인"""
        return line.isdigit() and 1 <= int(line) <= 20
    
    def _is_valid_product_name(self, line: str) -> bool:
        """유효한 제품명인지 확인"""
        # 길이 체크
        if len(line) < 15:
            return False
            
        # 노이즈 키워드 체크
        for noise in self.noise_keywords:
            if noise in line:
                return False
                
        # 브랜드명 패턴 체크
        for pattern in self.valid_product_patterns:
            if re.search(pattern, line):
                return True
                
        # 일반적인 제품명 패턴 (한글 + 숫자 + 단위)
        if re.search(r'[가-힣].*(g|개|kg|ml)', line):
            return True
            
        return False
    
    def _extract_ranked_product(self, lines: List[str], rank_idx: int, rank: int) -> Optional[Dict]:
        """순위별 제품 정보 추출"""
        product_name = None
        price = None
        
        # 순위 다음 라인들에서 제품명 찾기 (최대 5라인)
        for i in range(rank_idx + 1, min(rank_idx + 6, len(lines))):
            if self._is_valid_product_name(lines[i]):
                product_name = lines[i]
                break
        
        if not product_name:
            return None
            
        # 제품명 이후에서 가격 찾기 (최대 20라인)
        price_search_end = min(rank_idx + 25, len(lines))
        
        for i in range(rank_idx + 1, price_search_end):
            line = lines[i]
            
            # 다음 순위가 나오면 중단
            if self._is_rank_number(line) and int(line) > rank:
                break
                
            # 가격 패턴 찾기
            price_match = re.search(r'(\d{1,3}(?:,\d{3})*)원', line)
            if price_match and not price:
                # 할인 표시가 아닌 실제 가격인지 확인
                if not re.search(r'\d+%', line):  # 할인율이 없는 순수 가격
                    price = price_match.group(1)
                    break
        
        if product_name and price:
            return {
                'name': product_name,
                'price': price,
                'price_numeric': int(price.replace(',', '')),
                'rank': rank,
                'category': self.category,
                'parsed_at': datetime.now().isoformat(),
                'parse_method': 'automatic'
            }
        
        return None
    
    def find_missing_ranks(self, products: List[Dict]) -> List[int]:
        """누락된 순위 찾기"""
        found_ranks = [p['rank'] for p in products]
        expected_ranks = list(range(1, 11))  # 1-10위
        missing_ranks = [r for r in expected_ranks if r not in found_ranks]
        return missing_ranks
    
    def preview_parsing_results(self, products: List[Dict]):
        """파싱 결과 미리보기"""
        if not products:
            print("❌ 파싱된 상품이 없습니다.")
            return
            
        print(f"\n🏆 대용량과자 자동 파싱 결과 ({len(products)}개)")
        print("=" * 80)
        
        products.sort(key=lambda x: x['rank'])
        
        for product in products:
            print(f"{product['rank']:2d}위. {product['name']}")
            print(f"     💰 {product['price']}원")
            print()
        
        # 누락된 순위 확인
        missing = self.find_missing_ranks(products)
        if missing:
            print(f"⚠️ 누락된 순위: {missing}")
            print("💡 ATLAS MCP로 보완 필요")
        else:
            print("✅ 1-10위 모든 순위 파싱 완료!")
    
    def save_results(self, products: List[Dict], suffix: str = "") -> str:
        """결과 저장"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"coupang_대용량과자_hybrid_{timestamp}{suffix}.json"
        
        data = {
            'meta': {
                'title': '쿠팡 대용량과자 하이브리드 파싱',
                'total_products': len(products),
                'category': self.category,
                'parsed_at': datetime.now().isoformat(),
                'parser_version': '1.0_hybrid',
                'method': '90% 자동 + ATLAS MCP 보완'
            },
            'products': products
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print(f"💾 저장 완료: {filename}")
        return filename

# 실제 사용 함수
def parse_snack_data_hybrid(data: str) -> tuple:
    """하이브리드 파싱 실행"""
    parser = HybridSnackParser()
    
    # 1단계: 90% 자동 파싱
    products = parser.parse_coupang_snacks(data)
    
    # 2단계: 누락 순위 확인
    missing_ranks = parser.find_missing_ranks(products)
    
    return products, missing_ranks, parser

if __name__ == "__main__":
    print("🚀 하이브리드 대용량과자 파서 테스트")
    print("📋 90% 자동 + 10% ATLAS MCP 보완 방식")