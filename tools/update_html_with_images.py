#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML 룰렛 이미지 업데이트 시스템
다운로드된 실제 이미지를 HTML에 적용
"""

import json
import os
import re

def load_image_mapping():
    """이미지 매핑 데이터 로드"""
    mapping_file = '/mnt/d/ai/project_hub/active_projects/WhatToEat/data/image_mapping.json'
    with open(mapping_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_background_css():
    """배경 이미지 CSS 로드"""
    css_file = '/mnt/d/ai/project_hub/active_projects/WhatToEat/data/card_backgrounds.css'
    with open(css_file, 'r', encoding='utf-8') as f:
        return f.read()

def create_icon_css(image_mapping):
    """아이콘 이미지용 CSS 생성"""
    css_rules = []
    
    for menu_name, data in image_mapping['mapping'].items():
        icon_path = data['icon_path']
        safe_class = re.sub(r'[^a-zA-Z0-9가-힣]', '-', menu_name).lower()
        
        css_rule = f"""
.menu-icon.icon-{safe_class} {{
    background-image: url('{icon_path}');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    width: 55px;
    height: 55px;
    border-radius: 8px;
    display: inline-block;
    vertical-align: middle;
    margin-right: 8px;
}}"""
        css_rules.append(css_rule)
    
    return '\n'.join(css_rules)

def create_javascript_icon_mapping(image_mapping):
    """JavaScript용 아이콘 매핑 데이터 생성"""
    js_mapping = {}
    
    for menu_name, data in image_mapping['mapping'].items():
        icon_path = data['icon_path']
        safe_class = re.sub(r'[^a-zA-Z0-9가-힣]', '-', menu_name).lower()
        js_mapping[menu_name] = {
            'icon_path': icon_path,
            'css_class': f'icon-{safe_class}'
        }
    
    return js_mapping

def update_html_file():
    """HTML 파일에 이미지 시스템 통합"""
    
    # 데이터 로드
    image_mapping = load_image_mapping()
    background_css = load_background_css()
    icon_css = create_icon_css(image_mapping)
    js_icon_mapping = create_javascript_icon_mapping(image_mapping)
    
    # HTML 파일 읽기
    html_file = '/mnt/d/ai/project_hub/active_projects/WhatToEat/tools/roulette_v2_premium_fusion.html'
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 1. CSS 스타일 섹션에 이미지 CSS 추가
    css_insertion_point = html_content.find('</style>')
    if css_insertion_point == -1:
        print("❌ CSS 스타일 섹션을 찾을 수 없습니다.")
        return False
    
    # 새로운 CSS 블록 생성
    new_css = f"""
        
        /* 카드 배경 이미지 스타일 */
        .menu-category-card {{
            position: relative;
            overflow: hidden;
        }}
        
        .menu-category-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            z-index: -1;
        }}
        
        {background_css}
        
        /* 메뉴 아이콘 이미지 스타일 */
        .menu-icon {{
            display: inline-block;
            vertical-align: middle;
            margin-right: 8px;
            border-radius: 6px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        {icon_css}
        
        /* 휠 세그먼트 이미지 스타일 */
        .wheel-segment .menu-visual {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 5px;
        }}
        
        .wheel-segment .segment-icon {{
            width: 32px;
            height: 32px;
            border-radius: 4px;
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            box-shadow: 0 1px 3px rgba(0,0,0,0.3);
        }}
        
        .wheel-segment .segment-text {{
            font-size: 0.8em;
            text-align: center;
            line-height: 1.2;
        }}
"""
    
    # CSS 삽입
    html_content = html_content[:css_insertion_point] + new_css + html_content[css_insertion_point:]
    
    # 2. JavaScript에 이미지 매핑 데이터 추가
    js_insertion_point = html_content.find('// 메뉴 데이터')
    if js_insertion_point == -1:
        # 적절한 위치 찾기
        js_insertion_point = html_content.find('let currentMenuData = [];')
    
    if js_insertion_point != -1:
        # JavaScript 매핑 데이터 삽입
        js_mapping_code = f"""
        // 이미지 매핑 데이터
        const imageMapping = {json.dumps(js_icon_mapping, ensure_ascii=False, indent=8)};
        
        function getMenuImageHTML(menuName) {{
            if (imageMapping[menuName]) {{
                const mapping = imageMapping[menuName];
                return `<div class="menu-icon ${{mapping.css_class}}"></div>`;
            }}
            return getMenuIcon(menuName); // 기본 이모지로 폴백
        }}
        
        function getSegmentImageHTML(menuName) {{
            if (imageMapping[menuName]) {{
                const mapping = imageMapping[menuName];
                return `<div class="segment-icon" style="background-image: url('${{mapping.icon_path}}');"></div>`;
            }}
            return `<div style="font-size: 1.5em;">${{getMenuIcon(menuName)}}</div>`; // 기본 이모지로 폴백
        }}
        
"""
        
        # JavaScript 삽입
        html_content = html_content[:js_insertion_point] + js_mapping_code + html_content[js_insertion_point:]
    
    # 3. getMenuIcon 함수 업데이트하여 이미지 우선 사용
    old_getmenuicon_pattern = r'function getMenuIcon\(menuName\) \{[^}]*\}'
    new_getmenuicon = '''function getMenuIcon(menuName) {
            // 실제 이미지가 있으면 HTML 반환, 없으면 이모지 폴백
            if (imageMapping[menuName]) {
                return getMenuImageHTML(menuName);
            }
            
            // 기본 이모지 매핑
            const icons = {
                '후라이드치킨': '🍗', '양념치킨': '🍗', '뿌링클치킨': '🍗',
                '짜장면': '🍜', '짬뽕': '🍜', '탕수육': '🥢',
                '삼겹살구이': '🥩', '갈비구이': '🥩', '제육볶음': '🥩',
                '떡볶이': '🍢', '김밥': '🍙', '라면': '🍜',
                '피자': '🍕', '파스타': '🍝', '돈카츠': '🍖',
                '초밥': '🍣', '우동': '🍜', '족발': '🦶',
                '보쌈': '🥩', '곱창': '🦴'
            };
            return icons[menuName] || '🍽️';
        }'''
    
    html_content = re.sub(old_getmenuicon_pattern, new_getmenuicon, html_content, flags=re.DOTALL)
    
    # 4. 휠 세그먼트 생성 부분 업데이트
    old_segment_pattern = r'segment\.innerHTML = `<div>\$\{getMenuIcon\(menu\)\}<br>\$\{menu\}</div>`;'
    new_segment_code = '''segment.innerHTML = `
                        <div class="menu-visual">
                            ${getSegmentImageHTML(menu)}
                            <div class="segment-text">${menu}</div>
                        </div>
                    `;'''
    
    html_content = re.sub(old_segment_pattern, new_segment_code, html_content)
    
    # 업데이트된 HTML 저장
    output_file = '/mnt/d/ai/project_hub/active_projects/WhatToEat/tools/roulette_v2_premium_fusion_with_images.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return output_file

def main():
    print("🖼️ HTML 이미지 통합 시스템 시작...")
    
    # 이미지 매핑 확인
    image_mapping = load_image_mapping()
    print(f"📊 사용 가능한 이미지: {len(image_mapping['mapping'])}개")
    
    # HTML 업데이트
    output_file = update_html_file()
    
    if output_file:
        print(f"✅ 이미지가 적용된 HTML 생성: {output_file}")
        print(f"🎯 파일 크기: {os.path.getsize(output_file):,} bytes")
        
        # 웹 주소 형식으로 출력
        web_path = output_file.replace('/mnt/d/', 'file:///d:/')
        print(f"🌐 브라우저에서 열기: {web_path}")
        
        print("\n📋 적용된 기능:")
        print("✅ 카드 배경 이미지 (50% 투명도)")
        print("✅ 메뉴 아이콘 이미지 (55x55px)")
        print("✅ 휠 세그먼트 이미지")
        print("✅ 이모지 폴백 시스템")
        
    else:
        print("❌ HTML 업데이트 실패")

if __name__ == "__main__":
    main()