#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
아이콘 매핑 디버깅 도구
현재 매핑 상태를 확인하고 문제점을 찾아내는 도구
"""

import json
import os

def debug_icon_mapping():
    """아이콘 매핑 상태 디버깅"""
    
    # 1. 매핑 데이터 확인
    mapping_file = '/mnt/d/ai/project_hub/active_projects/WhatToEat/data/image_mapping.json'
    with open(mapping_file, 'r', encoding='utf-8') as f:
        mapping_data = json.load(f)
    
    print("🔍 아이콘 매핑 디버깅 시작...")
    print(f"📊 총 매핑된 메뉴: {len(mapping_data['mapping'])}개")
    print()
    
    # 2. 일식 카테고리 실제 HTML 데이터와 비교
    japanese_menu_in_html = [
        '모듬초밥', '돈카츠', '우동', '연어덮밥', '규동'
    ]
    
    print("🍣 일식 카테고리 매핑 상태:")
    for menu in japanese_menu_in_html:
        if menu in mapping_data['mapping']:
            status = "✅ 매핑됨"
            icon_file = mapping_data['mapping'][menu]['icon_file']
            print(f"  {menu}: {status} → {icon_file}")
        else:
            print(f"  {menu}: ❌ 매핑 없음")
    print()
    
    # 3. HTML에서 실제 JavaScript 함수 확인
    print("🔧 JavaScript 함수 매핑 확인:")
    
    # foodIconMapping에서 실제 매핑 확인
    safe_mappings = {}
    for menu_name in mapping_data['mapping'].keys():
        import re
        safe_class = re.sub(r'[^a-zA-Z0-9가-힣]', '-', menu_name).lower()
        safe_mappings[menu_name] = f'icon-{safe_class}'
        print(f"  {menu_name} → {safe_class}")
    
    print()
    print("🎯 권장 해결 방안:")
    print("1. getFoodIconHTML() 함수에서 정확한 메뉴명 매칭 확인")
    print("2. 매핑되지 않은 메뉴는 이모지 폴백 사용")
    print("3. 아이콘 크기 최적화 (40x40px 정사각형)")
    
    return mapping_data

def create_debug_html():
    """디버깅용 HTML 생성"""
    
    mapping_data = debug_icon_mapping()
    
    debug_html = """
<!DOCTYPE html>
<html>
<head>
    <title>아이콘 매핑 디버깅</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .icon-test { 
            display: inline-block; 
            margin: 10px; 
            text-align: center;
            border: 1px solid #ccc;
            padding: 10px;
            border-radius: 8px;
        }
        .food-icon { 
            width: 40px; 
            height: 40px; 
            border-radius: 8px; 
            background-size: cover; 
            background-position: center;
            margin: 0 auto 8px;
        }
"""
    
    # CSS 클래스 생성
    for menu_name, data in mapping_data['mapping'].items():
        import re
        safe_class = re.sub(r'[^a-zA-Z0-9가-힣]', '-', menu_name).lower()
        debug_html += f"""
        .food-icon.icon-{safe_class} {{
            background-image: url('../images/{data["icon_file"]}');
        }}"""
    
    debug_html += """
    </style>
</head>
<body>
    <h1>🔍 아이콘 매핑 디버깅</h1>
    <div>
"""
    
    # 각 메뉴별 아이콘 테스트
    for menu_name, data in mapping_data['mapping'].items():
        import re
        safe_class = re.sub(r'[^a-zA-Z0-9가-힣]', '-', menu_name).lower()
        debug_html += f"""
        <div class="icon-test">
            <div class="food-icon icon-{safe_class}"></div>
            <div>{menu_name}</div>
            <small>{data['icon_file']}</small>
        </div>"""
    
    debug_html += """
    </div>
</body>
</html>"""
    
    # 디버깅 HTML 파일 저장
    debug_file = '/mnt/d/ai/project_hub/active_projects/WhatToEat/tools/debug_icon_mapping.html'
    with open(debug_file, 'w', encoding='utf-8') as f:
        f.write(debug_html)
    
    print(f"🔧 디버깅 HTML 생성: {debug_file}")
    return debug_file

if __name__ == "__main__":
    debug_icon_mapping()
    create_debug_html()