#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
실제 음식 아이콘 시스템 구축
이모지를 실제 음식 사진으로 교체
"""

import json
import os
import re

def create_food_icon_system():
    """HTML에 실제 음식 아이콘 시스템 추가"""
    
    # 현재 사용 가능한 이미지 확인
    image_mapping_file = '/mnt/d/ai/project_hub/active_projects/WhatToEat/data/image_mapping.json'
    with open(image_mapping_file, 'r', encoding='utf-8') as f:
        image_mapping = json.load(f)
    
    # 아이콘 CSS 생성
    icon_css = """
        /* 실제 음식 아이콘 스타일 */
        .food-icon {
            width: 24px;
            height: 24px;
            border-radius: 4px;
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            display: inline-block;
            vertical-align: middle;
            margin-right: 6px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.2);
        }
        
        /* 카드 헤더의 큰 아이콘 */
        .category-header .food-icon {
            width: 40px;
            height: 40px;
            margin-right: 12px;
            border-radius: 8px;
        }
        
        /* 메뉴 항목의 작은 아이콘 */
        .menu-item-rank .food-icon {
            width: 20px;
            height: 20px;
            margin-right: 8px;
        }
"""
    
    # 각 음식별 아이콘 CSS 생성
    food_icon_classes = []
    for food_name, data in image_mapping['mapping'].items():
        safe_class = re.sub(r'[^a-zA-Z0-9가-힣]', '-', food_name).lower()
        icon_css += f"""
        .food-icon.icon-{safe_class} {{
            background-image: url('../images/{data["icon_file"]}');
        }}"""
        food_icon_classes.append({
            'name': food_name,
            'class': f'icon-{safe_class}',
            'available': True
        })
    
    # JavaScript 매핑 생성
    js_mapping = """
    // 실제 음식 아이콘 매핑
    const foodIconMapping = {
"""
    
    for food_name, data in image_mapping['mapping'].items():
        safe_class = re.sub(r'[^a-zA-Z0-9가-힣]', '-', food_name).lower()
        js_mapping += f'        "{food_name}": "icon-{safe_class}",\n'
    
    js_mapping += """    };
    
    // 음식 아이콘 HTML 생성 함수
    function getFoodIconHTML(foodName, size = 'small') {
        const iconClass = foodIconMapping[foodName];
        if (iconClass) {
            return `<span class="food-icon ${iconClass} ${size}"></span>`;
        }
        // 폴백: 기존 이모지 사용
        return getOriginalEmoji(foodName);
    }
    
    // 기존 이모지 매핑 (폴백용)
    function getOriginalEmoji(foodName) {
        const emojiMap = {
            '후라이드치킨': '🍗', '양념치킨': '🍗', '뿌링클치킨': '🍗',
            '짜장면': '🍜', '짬뽕': '🍜', '탕수육': '🥢',
            '삼겹살구이': '🥩', '갈비구이': '🥩', '제육볶음': '🥩',
            '떡볶이': '🍢', '김밥': '🍙', '라면': '🍜',
            '피자': '🍕', '파스타': '🍝', '돈카츠': '🍖',
            '초밥': '🍣', '우동': '🍜', '족발': '🦶',
            '보쌈': '🥩', '곱창': '🦴'
        };
        return emojiMap[foodName] || '🍽️';
    }
"""
    
    return {
        'css': icon_css,
        'javascript': js_mapping,
        'mapping': food_icon_classes
    }

def update_html_with_food_icons():
    """HTML 파일에 실제 음식 아이콘 시스템 적용"""
    
    html_file = '/mnt/d/ai/project_hub/active_projects/WhatToEat/tools/roulette_v2_with_background_images.html'
    
    # HTML 파일 읽기
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 아이콘 시스템 생성
    icon_system = create_food_icon_system()
    
    # CSS 추가
    css_insertion_point = html_content.find('.menu-category-card.category-latenight::after {')
    if css_insertion_point != -1:
        # 마지막 배경 이미지 CSS 다음에 추가
        end_point = html_content.find('}', css_insertion_point) + 1
        html_content = html_content[:end_point] + icon_system['css'] + html_content[end_point:]
    
    # JavaScript 추가
    js_insertion_point = html_content.find('// 물리엔진 상수')
    if js_insertion_point != -1:
        html_content = html_content[:js_insertion_point] + icon_system['javascript'] + '\n        ' + html_content[js_insertion_point:]
    
    # 아이콘 사용 예시 추가 (메뉴 항목에 실제 이미지 적용)
    # 이 부분은 실제 메뉴 데이터 구조에 맞게 나중에 추가
    
    # 업데이트된 HTML 저장
    output_file = '/mnt/d/ai/project_hub/active_projects/WhatToEat/tools/roulette_v2_with_real_food_icons.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return output_file

def main():
    print("🍽️ 실제 음식 아이콘 시스템 구축 중...")
    
    # 아이콘 시스템 생성
    icon_system = create_food_icon_system()
    
    print(f"✅ 사용 가능한 음식 아이콘: {len(icon_system['mapping'])}개")
    
    # HTML 업데이트
    output_file = update_html_with_food_icons()
    
    print(f"✅ 실제 음식 아이콘이 적용된 HTML 생성: {output_file}")
    
    # 사용법 안내
    print("\n📋 사용법:")
    print("1. 이모지 대신 실제 음식 사진 사용")
    print("2. 3가지 크기: small(20px), medium(24px), large(40px)")
    print("3. 자동 폴백: 이미지 없으면 기존 이모지 사용")
    
    print("\n🎯 다음 단계:")
    print("1. 메뉴 항목에 실제 이미지 적용")
    print("2. 카테고리 헤더에 대표 이미지 적용")
    print("3. 부족한 음식 이미지 추가 수집")

if __name__ == "__main__":
    main()