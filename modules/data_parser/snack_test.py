#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
과자 데이터 파싱 및 카드 생성 테스트
"""

from universal_smart_parser import UniversalSmartParser
from card_generator import CardGenerator

# 휘광님이 제공한 과자 데이터
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

def main():
    """과자 데이터 파싱 및 카드 생성"""
    print("🍪 과자 데이터 파싱 및 카드 생성 테스트")
    print("=" * 60)
    
    # 1. 데이터 파싱
    parser = UniversalSmartParser()
    products = parser.parse_coupang_data(snack_data, category='snack')
    
    if not products:
        print("❌ 파싱 실패")
        return
    
    print(f"✅ {len(products)}개 과자 상품 파싱 완료!")
    
    # 2. 카드 생성
    card_generator = CardGenerator()
    
    # 임시 JSON 파일 생성
    temp_json = {
        'meta': {
            'title': '쿠팡 과자 순위',
            'total_products': len(products),
            'category': 'snack'
        },
        'products': products
    }
    
    # JSON 파일 저장
    import json
    temp_file = "temp_snack_data.json"
    with open(temp_file, 'w', encoding='utf-8') as f:
        json.dump(temp_json, f, ensure_ascii=False, indent=2)
    
    # 카드 생성
    cards = card_generator.generate_cards_from_json(temp_file)
    
    if cards:
        # 카드 미리보기
        card_generator.preview_cards(cards)
        
        # JSON 저장
        json_file = card_generator.save_cards_to_json(cards, "snack_cards_20250709.json")
        
        # HTML 미리보기 생성
        html_file = card_generator.generate_html_preview(cards, "snack_cards_preview_20250709.html")
        
        print(f"\n🎉 과자 카드 생성 완료!")
        print(f"📄 JSON 파일: {json_file}")
        print(f"🌐 HTML 미리보기: {html_file}")
        print(f"🎯 {len(cards)}개 과자 카드가 WhatToEat 룰렛에 사용 가능합니다!")
        
        # 통계 정보
        print(f"\n📊 과자 카드 통계:")
        print(f"   • 총 카드 수: {len(cards)}개")
        print(f"   • 가격 범위: {min(c.price_numeric for c in cards):,}원 ~ {max(c.price_numeric for c in cards):,}원")
        print(f"   • 할인 상품: {len([c for c in cards if c.discount])}개")
        print(f"   • 평균 평점: {sum(c.rating for c in cards) / len(cards):.1f}점")
        
        # 카테고리별 분류
        brands = {}
        for card in cards:
            brand = card.title.split()[0]
            brands[brand] = brands.get(brand, 0) + 1
        
        print(f"   • 브랜드별 분포:")
        for brand, count in sorted(brands.items(), key=lambda x: x[1], reverse=True):
            print(f"     - {brand}: {count}개")
            
    else:
        print("❌ 카드 생성 실패")

if __name__ == "__main__":
    main()