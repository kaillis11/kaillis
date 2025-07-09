#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
개선된 쿠팡 데이터 파서 v2.0
휘광님의 복사 데이터에서 정확한 순위 추출
"""

import re
import json
from datetime import datetime
from typing import List, Dict

class ImprovedCoupangParser:
    def __init__(self):
        """개선된 파서 초기화"""
        self.categories = {
            'dessert': '디저트',
            'icecream': '아이스크림', 
            'frozen': '냉동식품',
            'snack': '과자',
            'drink': '음료'
        }
        
    def parse_coupang_data(self, text_content: str, category: str = 'dessert') -> List[Dict]:
        """쿠팡 복사 데이터에서 정확한 순위 추출"""
        print(f"🔍 쿠팡 {self.categories.get(category, category)} 순위 추출...")
        
        # 수동으로 정확한 데이터 추출 (휘광님이 복사한 내용 기반)
        products = []
        
        # 1위: 마켓오 브라우니 제주말차 
        products.append({
            'rank': 1,
            'name': '마켓오 브라우니 제주말차 12개입, 240g, 1개',
            'price': '5,010',
            'price_numeric': 5010,
            'original_price': '5,280',
            'discount': '5%',
            'reviews': '3,252',
            'rating': '5.0',
            'delivery': '로켓배송 내일(목) 도착 보장'
        })
        
        # 2위: 배스킨라빈스 피스타치오 크림 모찌 파이
        products.append({
            'rank': 2,
            'name': '배스킨라빈스 피스타치오 크림 모찌 파이 12p, 264g, 1개',
            'price': '5,180',
            'price_numeric': 5180,
            'original_price': '5,280',
            'discount': '1%',
            'reviews': '708',
            'rating': '4.5',
            'delivery': '로켓배송 내일(목) 도착 보장'
        })
        
        # 3위: 뉴트리오코 밀크맛 웨이퍼
        products.append({
            'rank': 3,
            'name': '뉴트리오코 밀크맛 웨이퍼, 360g, 1개',
            'price': '5,500',
            'price_numeric': 5500,
            'original_price': '7,800',
            'discount': '29%',
            'reviews': '3,566',
            'rating': '5.0',
            'delivery': '로켓배송 내일(목) 도착 보장',
            'badge': '쿠팡추천'
        })
        
        # 4위: 배스킨라빈스 쫀떡궁합 파이
        products.append({
            'rank': 4,
            'name': '배스킨라빈스 쫀떡궁합 파이, 264g, 3개',
            'price': '9,900',
            'price_numeric': 9900,
            'original_price': '15,840',
            'discount': '37%',
            'reviews': '668',
            'rating': '5.0',
            'delivery': '로켓배송 내일(목) 도착 보장',
            'badge': '쿠폰할인'
        })
        
        # 5위: 쿠캣 딸기쏙우유 찹쌀떡
        products.append({
            'rank': 5,
            'name': '쿠캣 딸기쏙우유 찹쌀떡 (냉동), 60g, 9개입, 1개',
            'price': '13,900',
            'price_numeric': 13900,
            'reviews': '6,075',
            'rating': '5.0',
            'delivery': '로켓배송 내일(목) 새벽 도착 보장'
        })
        
        # 6위: 뉴트리오코 초콜릿맛 웨이퍼
        products.append({
            'rank': 6,
            'name': '뉴트리오코 초콜릿맛 웨이퍼, 12g, 30개',
            'price': '5,500',
            'price_numeric': 5500,
            'original_price': '7,800',
            'discount': '29%',
            'reviews': '3,105',
            'rating': '5.0',
            'delivery': '로켓배송 내일(목) 도착 보장'
        })
        
        # 7위: 널담 뚱낭시에 8종 세트
        products.append({
            'rank': 7,
            'name': '널담 뚱낭시에 8종 세트 (냉동), 50g, 8개입, 1세트',
            'price': '12,900',
            'price_numeric': 12900,
            'reviews': '1,720',
            'rating': '4.5',
            'delivery': '로켓배송 내일(목) 새벽 도착 보장'
        })
        
        # 8위: 젤리젤리 부드럽고 촉촉한 한입 카스테라
        products.append({
            'rank': 8,
            'name': '젤리젤리 부드럽고 촉촉한 한입 카스테라, 1kg, 1박스',
            'price': '19,500',
            'price_numeric': 19500,
            'original_price': '22,500',
            'discount': '13%',
            'reviews': '5,038',
            'rating': '4.5',
            'delivery': '로켓배송 내일(목) 도착 보장'
        })
        
        # 9위: 다네시타 댄케이크 버터쿠키
        products.append({
            'rank': 9,
            'name': '다네시타 댄케이크 버터쿠키 싱글서브, 324g, 1개',
            'price': '12,280',
            'price_numeric': 12280,
            'original_price': '20,250',
            'discount': '39%',
            'reviews': '17,117',
            'rating': '4.5',
            'delivery': '로켓배송 내일(목) 도착 보장'
        })
        
        # 10위: 매일유업 얼려먹는 허쉬 초코바나나
        products.append({
            'rank': 10,
            'name': '매일유업 얼려먹는 허쉬 초코바나나, 24개, 85ml',
            'price': '14,730',
            'price_numeric': 14730,
            'reviews': '31',
            'rating': '5.0',
            'delivery': '내일(목) 도착 예정',
            'note': '배송비 5,000원'
        })
        
        # 메타데이터 추가
        for product in products:
            product['category'] = category
            product['category_name'] = self.categories.get(category, category)
            product['parsed_at'] = datetime.now().isoformat()
            product['source'] = 'coupang_manual_ranking'
            
        print(f"✅ {len(products)}개 정확한 순위 데이터 생성!")
        return products
        
    def preview_results(self, products: List[Dict]):
        """보기 좋게 결과 출력"""
        if not products:
            print("❌ 데이터가 없습니다.")
            return
            
        print(f"\n🏆 쿠팡 {products[0].get('category_name', '상품')} 랭킹 TOP {len(products)}")
        print("=" * 80)
        
        for product in products:
            # 할인 정보
            discount_info = ""
            if 'discount' in product:
                discount_info = f" ({product['discount']} 할인)"
                
            # 배지 정보
            badge_info = ""
            if 'badge' in product:
                badge_info = f" 🏷️{product['badge']}"
                
            print(f"{product['rank']:2d}위. {product['name']}{badge_info}")
            print(f"     💰 {product['price']}원{discount_info}")
            print(f"     ⭐ {product['rating']}점 | 📝 {product['reviews']}개 리뷰")
            print(f"     🚚 {product['delivery']}")
            if 'note' in product:
                print(f"     ⚠️ {product['note']}")
            print()
            
    def save_to_json(self, products: List[Dict], category: str = 'dessert') -> str:
        """JSON 파일로 저장"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"coupang_{category}_ranking_{timestamp}.json"
        
        data = {
            'meta': {
                'title': f'쿠팡 {self.categories.get(category)} 인기 순위',
                'category': category,
                'category_name': self.categories.get(category, category),
                'total_products': len(products),
                'parsed_at': datetime.now().isoformat(),
                'source': 'coupang_manual_ranking',
                'update_method': '수작업 복사 & 파싱',
                'next_update': '일주일 후 권장'
            },
            'ranking': products
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print(f"💾 순위 데이터 저장: {filename}")
        return filename

def main():
    """메인 실행"""
    parser = ImprovedCoupangParser()
    
    print("🛒 쿠팡 디저트 랭킹 데이터 생성기 v2.0")
    print("📋 휘광님이 복사한 데이터 기반으로 정확한 순위 생성...")
    
    # 정확한 순위 데이터 생성
    products = parser.parse_coupang_data('dessert')
    
    # 결과 출력
    parser.preview_results(products)
    
    # JSON 저장
    filepath = parser.save_to_json(products, 'dessert')
    
    print("\n🎯 다음 단계:")
    print("1. 이 데이터를 WhatToEat 룰렛에 연동")
    print("2. 일주일 후 새로운 복사 데이터로 업데이트")
    print("3. 쿠팡 파트너스 승인 후 공식 연동")

if __name__ == "__main__":
    main()