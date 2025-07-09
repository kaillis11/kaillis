#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
이미지 매핑 데이터 생성기
성공적으로 다운로드된 이미지들을 HTML 업데이트용 매핑 데이터로 변환
"""

import os
import json
from datetime import datetime

def create_image_mapping():
    """성공한 이미지들의 매핑 데이터 생성"""
    
    image_dir = '/mnt/d/ai/project_hub/active_projects/WhatToEat/images'
    
    # 아이콘 파일 목록
    icon_files = []
    bg_files = []
    
    for filename in os.listdir(image_dir):
        if filename.startswith('icon_') and filename.endswith('.jpg'):
            icon_files.append(filename)
        elif filename.startswith('bg_') and filename.endswith('.jpg'):
            bg_files.append(filename)
    
    print(f"📁 아이콘 파일: {len(icon_files)}개")
    print(f"📁 배경 파일: {len(bg_files)}개")
    
    # 매핑 데이터 생성
    image_mapping = {
        'timestamp': datetime.now().isoformat(),
        'total_icons': len(icon_files),
        'total_backgrounds': len(bg_files),
        'mapping': {}
    }
    
    # 메뉴명 → 파일명 매핑
    menu_to_file_mapping = {
        # 치킨류
        '후라이드치킨': 'fried_chicken.jpg',
        '양념치킨': 'seasoned_chicken.jpg',
        '뿌링클치킨': '뿌링클치킨.jpg',
        '허니콤보치킨': '허니콤보치킨.jpg',
        '황금올리브치킨': '황금올리브치킨.jpg',
        '치킨': '치킨.jpg',
        '치킨마요덮밥': '치킨마요덮밥.jpg',
        '치킨버거': '치킨버거.jpg',
        
        # 고기류
        '삼겹살구이': '삼겹살구이.jpg',
        '갈비구이': '갈비구이.jpg',
        '제육볶음': '제육볶음.jpg',
        '대패삼겹살': '대패삼겹살.jpg',
        '항정살구이': '항정살구이.jpg',
        '불고기덮밥': '불고기덮밥.jpg',
        '불고기버거': '불고기버거.jpg',
        
        # 한식
        '떡볶이': 'tteokbokki.jpg',
        '김밥': 'kimbap.jpg',
        '라면': 'ramen.jpg',
        '순대': '순대.jpg',
        '어묵': '어묵.jpg',
        '김치찌개': 'kimchi_stew.jpg',
        '비빔밥': '비빔밥.jpg',
        
        # 일식
        '모듬초밥': '모듬초밥.jpg',
        '돈카츠': '돈카츠.jpg',
        '우동': '우동.jpg',
        '연어덮밥': '연어덮밥.jpg',
        '규동': '규동.jpg',
        
        # 양식
        '크림파스타': '크림파스타.jpg',
        '토마토파스타': '토마토파스타.jpg',
        '피자': 'pizza.jpg',
        '오일파스타': '오일파스타.jpg',
        '라자냐': '라자냐.jpg',
        
        # 중식
        '짜장면': 'jajangmyeon.jpg',
        '짬뽕': 'jjamppong.jpg',
        '탕수육': 'sweet_sour_pork.jpg',
        '양장피': '양장피.jpg',
        '마파두부': '마파두부.jpg',
        
        # 패스트푸드
        '더블치즈버거': '더블치즈버거.jpg',
        '새우버거': '새우버거.jpg',
        '베이컨버거': '베이컨버거.jpg',
        
        # 도시락
        '돈까스덮밥': '돈까스덮밥.jpg',
        '스팸마요덮밥': '스팸마요덮밥.jpg',
        
        # 야식
        '족발': '족발.jpg',
        '보쌈': '보쌈.jpg',
        '곱창': '곱창.jpg',
        
        # 디저트
        '아이스크림': '아이스크림.jpg',
        '케이크': '케이크.jpg',
        '마카롱': '마카롱.jpg',
        '붕어빵': '붕어빵.jpg',
        '호떡': '호떡.jpg'
    }
    
    # 실제 파일 존재 확인 및 매핑 생성
    for menu_name, filename in menu_to_file_mapping.items():
        icon_path = f"icon_{filename}"
        bg_path = f"bg_{filename}"
        
        if icon_path in icon_files and bg_path in bg_files:
            image_mapping['mapping'][menu_name] = {
                'icon_file': icon_path,
                'bg_file': bg_path,
                'icon_path': f"./images/{icon_path}",
                'bg_path': f"./images/{bg_path}",
                'status': 'available'
            }
            print(f"✅ {menu_name} → {filename}")
        else:
            print(f"❌ {menu_name} → {filename} (파일 없음)")
    
    return image_mapping

def generate_css_for_backgrounds(image_mapping):
    """카드 배경 이미지용 CSS 생성"""
    
    css_rules = []
    
    # 카테고리별 배경 이미지 CSS
    category_mapping = {
        'chicken': ['후라이드치킨', '양념치킨', '뿌링클치킨', '허니콤보치킨', '황금올리브치킨', '치킨', '치킨마요덮밥', '치킨버거'],
        'meat': ['삼겹살구이', '갈비구이', '제육볶음', '대패삼겹살', '항정살구이', '불고기덮밥', '불고기버거'],
        'bunsik': ['떡볶이', '김밥', '순대', '어묵'],
        'lunchbox': ['치킨마요덮밥', '불고기덮밥', '비빔밥', '돈까스덮밥', '스팸마요덮밥'],
        'japanese': ['모듬초밥', '돈카츠', '우동', '연어덮밥', '규동'],
        'western': ['크림파스타', '토마토파스타', '피자', '오일파스타', '라자냐'],
        'chinese': ['짜장면', '짬뽕', '탕수육', '양장피', '마파두부'],
        'dessert': ['아이스크림', '케이크', '마카롱', '붕어빵', '호떡'],
        'soup': ['김치찌개'],
        'latenight': ['족발', '보쌈', '곱창']
    }
    
    # 각 카테고리의 대표 이미지 선택
    for category, menus in category_mapping.items():
        for menu in menus:
            if menu in image_mapping['mapping']:
                bg_path = image_mapping['mapping'][menu]['bg_path']
                css_rule = f"""
.menu-category-card.category-{category}::before {{
    background-image: url('{bg_path}');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    opacity: 0.3;
    filter: blur(1px);
}}"""
                css_rules.append(css_rule)
                break  # 첫 번째 사용 가능한 이미지만 사용
    
    return '\n'.join(css_rules)

def main():
    print("🖼️ 이미지 매핑 데이터 생성 중...")
    
    # 매핑 데이터 생성
    image_mapping = create_image_mapping()
    
    # JSON 파일로 저장
    output_file = '/mnt/d/ai/project_hub/active_projects/WhatToEat/data/image_mapping.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(image_mapping, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 매핑 데이터 저장: {output_file}")
    
    # 카드 배경용 CSS 생성
    bg_css = generate_css_for_backgrounds(image_mapping)
    
    css_file = '/mnt/d/ai/project_hub/active_projects/WhatToEat/data/card_backgrounds.css'
    with open(css_file, 'w', encoding='utf-8') as f:
        f.write(bg_css)
    
    print(f"🎨 배경 CSS 저장: {css_file}")
    
    print(f"\n📊 매핑 결과:")
    print(f"✅ 사용 가능한 메뉴: {len(image_mapping['mapping'])}개")
    print(f"📁 아이콘 파일: {image_mapping['total_icons']}개")
    print(f"📁 배경 파일: {image_mapping['total_backgrounds']}개")
    
    print("\n🎯 다음 단계: HTML 업데이트")

if __name__ == "__main__":
    main()