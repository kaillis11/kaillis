#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
마카롱 카드 생성 테스트
"""

from card_generator import CardGenerator

def main():
    """마카롱 카드 생성 테스트"""
    generator = CardGenerator()
    
    print("🧁 마카롱 카드 생성 테스트")
    print("📋 마카롱 데이터로 카드 생성 중...")
    
    # 마카롱 JSON 파일 찾기
    macaron_file = "coupang_macaron_ultimate_20250709_165554.json"
    
    try:
        # 카드 생성
        cards = generator.generate_cards_from_json(macaron_file)
        
        if cards:
            # 카드 미리보기
            generator.preview_cards(cards)
            
            # JSON 저장
            json_file = generator.save_cards_to_json(cards, "macaron_cards_20250709.json")
            
            # HTML 미리보기 생성
            html_file = generator.generate_html_preview(cards, "macaron_cards_preview_20250709.html")
            
            print(f"\n✅ 마카롱 카드 생성 완료!")
            print(f"📄 JSON 파일: {json_file}")
            print(f"🌐 HTML 미리보기: {html_file}")
            print(f"🎯 {len(cards)}개 마카롱 카드가 WhatToEat 룰렛에 사용 가능합니다!")
        else:
            print("❌ 카드 생성에 실패했습니다.")
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    main()