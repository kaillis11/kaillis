#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unsplash API 이미지 수집기
WhatToEat 룰렛 메뉴용 고품질 이미지 자동 수집
"""

import requests
import json
import os
import time
from datetime import datetime
from urllib.parse import urlparse
from PIL import Image
import io

class UnsplashImageCollector:
    def __init__(self, access_key=None):
        """
        Unsplash API 초기화
        
        무료 API 키 발급: https://unsplash.com/developers
        월 1000회 요청 제한 (충분함)
        """
        self.access_key = access_key or "YOUR_UNSPLASH_ACCESS_KEY_HERE"
        self.base_url = "https://api.unsplash.com"
        self.headers = {
            "Authorization": f"Client-ID {self.access_key}",
            "User-Agent": "WhatToEat-Roulette/1.0"
        }
        
        # 이미지 저장 디렉토리
        self.image_dir = "/mnt/d/ai/project_hub/active_projects/WhatToEat/images"
        os.makedirs(self.image_dir, exist_ok=True)
        
        # 결과 로그
        self.results = {
            'success': [],
            'failed': [],
            'skipped': []
        }
    
    def search_image(self, query, per_page=1):
        """Unsplash에서 이미지 검색"""
        url = f"{self.base_url}/search/photos"
        params = {
            'query': query,
            'per_page': per_page,
            'orientation': 'landscape',  # 가로형 이미지 선호
            'order_by': 'relevance'
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            if data['results']:
                return data['results'][0]  # 첫 번째(가장 관련성 높은) 결과
            return None
            
        except requests.exceptions.RequestException as e:
            print(f"❌ API 요청 실패: {e}")
            return None
    
    def download_image(self, image_data, filename):
        """이미지 다운로드 및 최적화 (아이콘 + 배경용 2가지 크기)"""
        try:
            # 고품질 이미지 URL 선택
            image_url = image_data['urls'].get('regular', image_data['urls']['raw'])
            
            # 이미지 다운로드
            response = requests.get(image_url, stream=True)
            response.raise_for_status()
            
            # PIL로 이미지 처리
            original_img = Image.open(io.BytesIO(response.content))
            
            # 1. 아이콘용 이미지 (55x55px 정사각형)
            icon_img = original_img.copy()
            icon_img.thumbnail((200, 200), Image.Resampling.LANCZOS)
            
            # 정사각형으로 크롭
            width, height = icon_img.size
            if width != height:
                size = min(width, height)
                left = (width - size) // 2
                top = (height - size) // 2
                icon_img = icon_img.crop((left, top, left + size, top + size))
            
            # 최종 아이콘 크기로 리사이징
            icon_img = icon_img.resize((55, 55), Image.Resampling.LANCZOS)
            
            # 아이콘 저장
            icon_path = os.path.join(self.image_dir, f"icon_{filename}")
            if icon_img.mode in ('RGBA', 'LA'):
                icon_img.save(icon_path.replace('.jpg', '.png'), 'PNG', optimize=True)
            else:
                icon_img = icon_img.convert('RGB')
                icon_img.save(icon_path, 'JPEG', quality=90, optimize=True)
            
            # 2. 배경용 이미지 (450x120px 가로형)
            bg_img = original_img.copy()
            bg_img.thumbnail((600, 400), Image.Resampling.LANCZOS)
            
            # 가로형으로 크롭 (450:120 비율)
            width, height = bg_img.size
            target_ratio = 450 / 120  # 3.75:1
            current_ratio = width / height
            
            if current_ratio > target_ratio:
                # 너무 가로로 길면 높이에 맞춰서 자르기
                new_width = int(height * target_ratio)
                left = (width - new_width) // 2
                bg_img = bg_img.crop((left, 0, left + new_width, height))
            else:
                # 너무 세로로 길면 가로에 맞춰서 자르기
                new_height = int(width / target_ratio)
                top = (height - new_height) // 2
                bg_img = bg_img.crop((0, top, width, top + new_height))
            
            # 최종 배경 크기로 리사이징
            bg_img = bg_img.resize((450, 120), Image.Resampling.LANCZOS)
            
            # 배경 저장
            bg_path = os.path.join(self.image_dir, f"bg_{filename}")
            bg_img = bg_img.convert('RGB')
            bg_img.save(bg_path, 'JPEG', quality=85, optimize=True)
            
            return {
                'icon_path': icon_path,
                'bg_path': bg_path,
                'icon_size': '55x55',
                'bg_size': '450x120'
            }
            
        except Exception as e:
            print(f"❌ 이미지 다운로드 실패: {e}")
            return None
    
    def collect_images_for_menus(self, menu_data_file, limit=None):
        """메뉴 데이터 파일에서 이미지 수집"""
        
        # 메뉴 데이터 로드
        with open(menu_data_file, 'r', encoding='utf-8') as f:
            menu_data = json.load(f)
        
        all_menus = menu_data['all_menus']
        if limit:
            all_menus = all_menus[:limit]
        
        print(f"🚀 {len(all_menus)}개 메뉴 이미지 수집 시작...")
        
        for i, menu in enumerate(all_menus, 1):
            print(f"\n🔍 [{i}/{len(all_menus)}] {menu['original']} 검색 중...")
            
            # 파일명 생성 (한글 → 영문)
            safe_filename = self.generate_safe_filename(menu['original'])
            file_path = os.path.join(self.image_dir, safe_filename)
            
            # 이미 다운로드된 이미지 스킵
            if os.path.exists(file_path):
                print(f"⏭️ 이미 존재함: {safe_filename}")
                self.results['skipped'].append({
                    'menu': menu['original'],
                    'filename': safe_filename,
                    'reason': 'already_exists'
                })
                continue
            
            # 이미지 검색
            search_query = menu['search_term']
            image_data = self.search_image(search_query)
            
            if image_data:
                # 이미지 다운로드 (아이콘 + 배경)
                downloaded_result = self.download_image(image_data, safe_filename)
                
                if downloaded_result:
                    print(f"✅ 성공: {safe_filename} (아이콘 + 배경)")
                    self.results['success'].append({
                        'menu': menu['original'],
                        'filename': safe_filename,
                        'icon_path': downloaded_result['icon_path'],
                        'bg_path': downloaded_result['bg_path'],
                        'icon_size': downloaded_result['icon_size'],
                        'bg_size': downloaded_result['bg_size'],
                        'unsplash_id': image_data['id'],
                        'author': image_data['user']['name'],
                        'download_url': image_data['links']['download_location']
                    })
                else:
                    print(f"❌ 다운로드 실패: {menu['original']}")
                    self.results['failed'].append({
                        'menu': menu['original'],
                        'reason': 'download_failed'
                    })
            else:
                print(f"❌ 검색 실패: {menu['original']}")
                self.results['failed'].append({
                    'menu': menu['original'],
                    'reason': 'search_failed'
                })
            
            # API 제한 고려 (1초 대기)
            time.sleep(1)
        
        return self.results
    
    def generate_safe_filename(self, menu_name):
        """안전한 파일명 생성"""
        # 한글 메뉴명을 영문으로 매핑
        name_mapping = {
            '후라이드치킨': 'fried_chicken.jpg',
            '양념치킨': 'seasoned_chicken.jpg',
            '짜장면': 'jajangmyeon.jpg',
            '짬뽕': 'jjamppong.jpg',
            '탕수육': 'sweet_sour_pork.jpg',
            '김치찌개': 'kimchi_stew.jpg',
            '된장찌개': 'doenjang_stew.jpg',
            '삼겹살': 'pork_belly.jpg',
            '갈비': 'galbi.jpg',
            '피자': 'pizza.jpg',
            '파스타': 'pasta.jpg',
            '초밥': 'sushi.jpg',
            '라면': 'ramen.jpg',
            '떡볶이': 'tteokbokki.jpg',
            '김밥': 'kimbap.jpg',
            '월드콘': 'world_cone.jpg',
            '메로나': 'melona.jpg',
            '붕어싸만코': 'bungeoppang_samanco.jpg'
        }
        
        # 직접 매핑이 있으면 사용
        if menu_name in name_mapping:
            return name_mapping[menu_name]
        
        # 없으면 자동 생성
        import re
        safe_name = re.sub(r'[^a-zA-Z0-9가-힣]', '_', menu_name)
        safe_name = safe_name.lower().replace(' ', '_')
        return f"{safe_name}.jpg"
    
    def save_results(self, output_file):
        """결과 저장"""
        result_data = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_processed': len(self.results['success']) + len(self.results['failed']) + len(self.results['skipped']),
                'success_count': len(self.results['success']),
                'failed_count': len(self.results['failed']),
                'skipped_count': len(self.results['skipped'])
            },
            'results': self.results
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 결과 저장: {output_file}")

def main():
    # 사용법 안내
    print("🖼️ Unsplash 이미지 수집기")
    print("=" * 50)
    print("⚠️  주의: Unsplash API 키가 필요합니다!")
    print("🔗 무료 키 발급: https://unsplash.com/developers")
    print("📝 월 1000회 제한 (103개 메뉴 + 여유분)")
    print()
    
    # API 키 확인
    api_key = input("Unsplash API 키를 입력하세요 (Enter로 스킵): ").strip()
    if not api_key:
        print("⚠️ API 키 없이 데모 모드로 실행 (실제 다운로드 불가)")
        api_key = "DEMO_KEY"
    
    # 수집기 초기화
    collector = UnsplashImageCollector(api_key)
    
    # 메뉴 데이터 파일
    menu_data_file = '/mnt/d/ai/project_hub/active_projects/WhatToEat/data/menu_names_for_images.json'
    
    # 테스트 실행 (처음 5개만)
    test_mode = input("테스트 모드 (5개만)? (y/N): ").strip().lower()
    limit = 5 if test_mode == 'y' else None
    
    # 이미지 수집 실행
    results = collector.collect_images_for_menus(menu_data_file, limit=limit)
    
    # 결과 저장
    output_file = '/mnt/d/ai/project_hub/active_projects/WhatToEat/data/image_collection_results.json'
    collector.save_results(output_file)
    
    # 결과 요약
    print("\n📊 수집 결과:")
    print(f"✅ 성공: {len(results['success'])}개")
    print(f"❌ 실패: {len(results['failed'])}개")
    print(f"⏭️ 스킵: {len(results['skipped'])}개")
    
    if results['failed']:
        print("\n🔄 실패한 메뉴들 (수동 보완 필요):")
        for failed in results['failed']:
            print(f"  - {failed['menu']} ({failed['reason']})")
    
    print("\n🎯 다음 단계: 이미지 품질 검토 및 HTML 업데이트")

if __name__ == "__main__":
    main()