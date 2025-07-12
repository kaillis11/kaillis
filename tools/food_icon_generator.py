#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎨 음식 아이콘 자동 생성 시스템
다양한 방법으로 40x40px 음식 아이콘을 생성하는 도구
"""

import requests
import json
import os
from PIL import Image, ImageDraw, ImageFont
import io
import time
from datetime import datetime

class FoodIconGenerator:
    def __init__(self):
        self.output_dir = "/mnt/d/ai/project_hub/active_projects/WhatToEat/images/generated_icons"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 한국 음식 목록
        self.korean_foods = [
            "후라이드치킨", "양념치킨", "뿌링클치킨", "허니콤보치킨", "황금올리브치킨",
            "삼겹살구이", "갈비구이", "제육볶음", "대패삼겹살", "항정살구이",
            "떡볶이", "김밥", "라면", "순대", "어묵",
            "모듬초밥", "돈카츠", "우동", "연어덮밥", "규동",
            "크림파스타", "토마토파스타", "피자", "오일파스타", "라자냐",
            "짜장면", "짬뽕", "탕수육", "양장피", "마파두부",
            "더블치즈버거", "새우버거", "베이컨버거",
            "족발", "보쌈", "곱창",
            "아이스크림", "케이크", "마카롱", "붕어빵", "호떡"
        ]
    
    def method_1_icon_libraries(self):
        """방법 1: 무료 아이콘 라이브러리 활용"""
        print("📚 방법 1: 아이콘 라이브러리에서 수집")
        
        # Flaticon, Icons8 등의 무료 아이콘 검색
        # 실제로는 웹 스크래핑이나 API 필요
        icon_sources = {
            "flaticon": "https://www.flaticon.com/search?word=",
            "icons8": "https://icons8.com/icons/set/",
            "feather": "https://feathericons.com/"
        }
        
        print("💡 아이콘 라이브러리 활용 방법:")
        print("1. Flaticon에서 '{food_name} food icon' 검색")
        print("2. SVG 형태로 다운로드")
        print("3. 40x40px로 리사이징")
        print("4. 일관된 스타일 적용")
        
        return "icon_library_method"
    
    def method_2_unsplash_crop(self, unsplash_api_key=None):
        """방법 2: Unsplash + 자동 크롭"""
        print("📸 방법 2: Unsplash 이미지 + 자동 크롭")
        
        if not unsplash_api_key:
            print("⚠️ Unsplash API 키가 필요합니다")
            return None
        
        generated_icons = {}
        
        for food in self.korean_foods[:5]:  # 테스트용으로 5개만
            try:
                # Unsplash에서 이미지 검색
                image_url = self.search_unsplash(food, unsplash_api_key)
                if image_url:
                    # 이미지 다운로드 및 처리
                    icon = self.create_icon_from_image(image_url, food)
                    generated_icons[food] = icon
                    print(f"✅ {food} 아이콘 생성 완료")
                else:
                    print(f"❌ {food} 이미지 검색 실패")
                    
                time.sleep(1)  # API 제한 고려
                
            except Exception as e:
                print(f"❌ {food} 생성 오류: {e}")
        
        return generated_icons
    
    def method_3_dalle_generation(self, openai_api_key=None):
        """방법 3: DALL-E 3 AI 생성"""
        print("🤖 방법 3: DALL-E 3 AI 이미지 생성")
        
        if not openai_api_key:
            print("⚠️ OpenAI API 키가 필요합니다")
            print("💡 API 키 발급: https://platform.openai.com/")
            return None
        
        # OpenAI API 사용 예시
        dalle_prompt_template = """
        A clean, minimalist icon of {food_name} (Korean food).
        - Square format, centered composition
        - High contrast, clear details  
        - White background
        - Perfect for mobile app icon
        - Professional food photography style
        - Easily recognizable at small sizes
        """
        
        print("🎨 DALL-E 3 프롬프트 최적화:")
        print(f"템플릿: {dalle_prompt_template}")
        
        return "dalle_method"
    
    def method_4_simple_text_icons(self):
        """방법 4: 간단한 텍스트 아이콘 생성"""
        print("✍️ 방법 4: 텍스트 기반 아이콘 생성")
        
        generated_icons = {}
        
        for food in self.korean_foods:
            try:
                icon = self.create_text_icon(food)
                output_path = os.path.join(self.output_dir, f"text_icon_{food}.png")
                icon.save(output_path)
                generated_icons[food] = output_path
                print(f"✅ {food} 텍스트 아이콘 생성")
                
            except Exception as e:
                print(f"❌ {food} 텍스트 아이콘 생성 실패: {e}")
        
        return generated_icons
    
    def create_text_icon(self, food_name):
        """텍스트 기반 아이콘 생성"""
        # 40x40px 이미지 생성
        img = Image.new('RGB', (40, 40), color='white')
        draw = ImageDraw.Draw(img)
        
        # 음식 이름의 첫 글자만 사용
        first_char = food_name[0]
        
        # 텍스트 중앙 정렬
        try:
            # 시스템 폰트 사용
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
        except:
            font = ImageFont.load_default()
        
        # 텍스트 크기 측정
        bbox = draw.textbbox((0, 0), first_char, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # 중앙 위치 계산
        x = (40 - text_width) // 2
        y = (40 - text_height) // 2
        
        # 배경 원 그리기
        draw.ellipse([2, 2, 38, 38], fill='#f0f0f0', outline='#ccc')
        
        # 텍스트 그리기
        draw.text((x, y), first_char, fill='black', font=font)
        
        return img
    
    def search_unsplash(self, food_name, api_key):
        """Unsplash에서 음식 이미지 검색"""
        url = "https://api.unsplash.com/search/photos"
        params = {
            'query': f"{food_name} food korean close-up",
            'per_page': 1,
            'orientation': 'squarish'
        }
        headers = {
            'Authorization': f'Client-ID {api_key}'
        }
        
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            if data['results']:
                return data['results'][0]['urls']['small']
            return None
            
        except Exception as e:
            print(f"Unsplash 검색 오류: {e}")
            return None
    
    def create_icon_from_image(self, image_url, food_name):
        """이미지 URL에서 40x40px 아이콘 생성"""
        try:
            response = requests.get(image_url)
            response.raise_for_status()
            
            # 이미지 열기
            img = Image.open(io.BytesIO(response.content))
            
            # 정사각형으로 크롭
            width, height = img.size
            if width != height:
                size = min(width, height)
                left = (width - size) // 2
                top = (height - size) // 2
                img = img.crop((left, top, left + size, top + size))
            
            # 40x40px로 리사이징
            icon = img.resize((40, 40), Image.Resampling.LANCZOS)
            
            # 저장
            output_path = os.path.join(self.output_dir, f"icon_{food_name}.png")
            icon.save(output_path)
            
            return output_path
            
        except Exception as e:
            print(f"이미지 처리 오류: {e}")
            return None
    
    def generate_summary_report(self):
        """생성 방법별 요약 보고서"""
        report = f"""
# 🎨 음식 아이콘 생성 방법 요약

**생성 시간**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 방법별 비교

### 1. 아이콘 라이브러리 (추천 ⭐⭐⭐⭐⭐)
- **비용**: 무료
- **품질**: 높음 (일관된 스타일)
- **속도**: 빠름
- **장점**: 전문적인 디자인, 즉시 사용 가능
- **단점**: 수작업 필요

### 2. Unsplash + 크롭 (실용적 ⭐⭐⭐⭐)
- **비용**: 무료 (API 키 필요)
- **품질**: 중간 (실제 사진)
- **속도**: 중간
- **장점**: 실제 음식 사진 활용
- **단점**: 크기 일관성 문제

### 3. DALL-E 3 (고품질 ⭐⭐⭐⭐⭐)
- **비용**: 유료 ($0.02/이미지)
- **품질**: 매우 높음
- **속도**: 빠름
- **장점**: 완벽한 커스터마이징
- **단점**: 비용 발생

### 4. 텍스트 아이콘 (임시방편 ⭐⭐)
- **비용**: 무료
- **품질**: 낮음
- **속도**: 매우 빠름
- **장점**: 즉시 생성 가능
- **단점**: 시각적 매력 부족

## 🎯 추천 구현 순서

1. **즉시**: 텍스트 아이콘으로 임시 대체
2. **단기**: 아이콘 라이브러리에서 수집
3. **장기**: DALL-E 3 자동 생성 시스템

## 📁 출력 디렉토리
{self.output_dir}
"""
        
        report_file = os.path.join(self.output_dir, "generation_report.md")
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return report_file

def main():
    print("🎨 음식 아이콘 자동 생성 시스템")
    print("=" * 50)
    
    generator = FoodIconGenerator()
    
    print("\n📋 사용 가능한 방법들:")
    print("1. 아이콘 라이브러리 활용")
    print("2. Unsplash + 자동 크롭")
    print("3. DALL-E 3 AI 생성")
    print("4. 간단한 텍스트 아이콘")
    
    # 방법 1: 아이콘 라이브러리 안내
    generator.method_1_icon_libraries()
    print()
    
    # 방법 4: 텍스트 아이콘 즉시 생성
    print("🚀 텍스트 아이콘 즉시 생성 시작...")
    text_icons = generator.method_4_simple_text_icons()
    print(f"✅ {len(text_icons)}개 텍스트 아이콘 생성 완료")
    print()
    
    # 보고서 생성
    report_file = generator.generate_summary_report()
    print(f"📄 보고서 생성: {report_file}")
    
    print("\n🎯 다음 단계:")
    print("1. 텍스트 아이콘으로 임시 대체 테스트")
    print("2. OpenAI API 키 발급 후 DALL-E 3 테스트")
    print("3. 아이콘 라이브러리에서 전문 아이콘 수집")

if __name__ == "__main__":
    main()