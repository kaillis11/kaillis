#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WhatToEat 룰렛 메뉴 이름 추출기
HTML에서 모든 메뉴 이름을 추출하여 이미지 검색용 리스트 생성
"""

import re
import json
from datetime import datetime

def extract_menu_names_from_html(html_file_path):
    """HTML 파일에서 메뉴 이름 추출"""
    with open(html_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # JavaScript의 PREMIUM_MENU_DATA 섹션 찾기
    pattern = r'const PREMIUM_MENU_DATA = \[(.*?)\];'
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        print("❌ PREMIUM_MENU_DATA를 찾을 수 없습니다.")
        return []
    
    data_section = match.group(1)
    
    # 메뉴 이름 패턴 추출
    menu_names = []
    
    # name: '메뉴명' 패턴 찾기
    name_pattern = r"name: ['\"]([^'\"]+)['\"]"
    names = re.findall(name_pattern, data_section)
    
    for name in names:
        # 특수 문자 제거 (괄호 안 내용 제거)
        clean_name = re.sub(r'\s*\([^)]*\)', '', name)
        clean_name = clean_name.strip()
        
        # 광고나 랭킹 제외
        if not any(skip in clean_name for skip in ['베스트셀러', '랭킹', '1위', '순위']):
            menu_names.append({
                'original': name,
                'cleaned': clean_name,
                'search_term': clean_name + ' food korean'  # 검색용 키워드
            })
    
    return menu_names

def categorize_menus(menu_names):
    """메뉴를 카테고리별로 분류"""
    categories = {
        'chicken': [],
        'meat': [],
        'korean': [],
        'japanese': [],
        'western': [],
        'chinese': [],
        'dessert': [],
        'drink': [],
        'snack': [],
        'icecream': [],
        'other': []
    }
    
    # 카테고리 키워드 매핑
    category_keywords = {
        'chicken': ['치킨', '닭', '후라이드', '양념', '뿌링클'],
        'meat': ['삼겹살', '갈비', '제육', '대패', '항정살', '불고기'],
        'korean': ['김치찌개', '된장찌개', '부대찌개', '순두부', '미역국', '떡볶이', '김밥', '순대'],
        'japanese': ['초밥', '돈카츠', '우동', '연어', '규동', '라면'],
        'western': ['파스타', '피자', '라자냐', '버거', '스테이크'],
        'chinese': ['짜장면', '짬뽕', '탕수육', '양장피', '마파두부'],
        'dessert': ['케이크', '마카롱', '붕어빵', '호떡'],
        'icecream': ['아이스크림', '월드콘', '메로나', '붕어싸만코', '투게더', '빵빠레', '브라보콘', '돼지바', '비비빅', '수박바', '하겐다즈'],
        'drink': ['음료', '커피', '차', '주스'],
        'snack': ['과자', '간식', '스낵']
    }
    
    for menu in menu_names:
        categorized = False
        for category, keywords in category_keywords.items():
            if any(keyword in menu['cleaned'] for keyword in keywords):
                categories[category].append(menu)
                categorized = True
                break
        
        if not categorized:
            categories['other'].append(menu)
    
    return categories

def main():
    html_file = '/mnt/d/ai/project_hub/active_projects/WhatToEat/tools/roulette_v2_premium_fusion.html'
    
    print("🔍 룰렛 HTML에서 메뉴 이름 추출 중...")
    menu_names = extract_menu_names_from_html(html_file)
    
    if not menu_names:
        print("❌ 메뉴 이름을 찾을 수 없습니다.")
        return
    
    print(f"✅ {len(menu_names)}개 메뉴 이름 추출 완료!")
    
    # 카테고리별 분류
    categories = categorize_menus(menu_names)
    
    # 결과 출력
    print("\n📊 카테고리별 메뉴 분류:")
    total_menus = 0
    for category, menus in categories.items():
        if menus:
            print(f"\n🏷️ {category.upper()} ({len(menus)}개):")
            for menu in menus:
                print(f"  - {menu['original']} → {menu['cleaned']}")
                total_menus += 1
    
    print(f"\n📈 총 메뉴 수: {total_menus}개")
    
    # JSON 파일로 저장
    output_data = {
        'timestamp': datetime.now().isoformat(),
        'total_menus': total_menus,
        'categories': categories,
        'all_menus': menu_names
    }
    
    output_file = '/mnt/d/ai/project_hub/active_projects/WhatToEat/data/menu_names_for_images.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 결과 저장: {output_file}")
    print("🎯 다음 단계: Unsplash API로 이미지 수집 준비 완료!")

if __name__ == "__main__":
    main()