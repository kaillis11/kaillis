#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
네이버 쇼핑 API 기반 제품 이미지 수집기 v1.0
쿠팡 랭킹 데이터와 연동하여 제품 이미지를 자동으로 가져오는 시스템
"""

import time
import random
import json
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlencode, quote
from typing import List, Dict, Optional

class NaverImageFetcher:
    def __init__(self, headless=True):
        """네이버 쇼핑 이미지 수집기 초기화"""
        self.setup_driver(headless)
        self.base_url = "https://search.shopping.naver.com/search?"
        
    def setup_driver(self, headless=True):
        """Selenium 드라이버 설정"""
        chrome_options = Options()
        
        # WSL 환경 최적화 설정
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # User-Agent 설정
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        chrome_options.add_argument(f'--user-agent={random.choice(user_agents)}')
        
        # Chromium 바이너리 설정 (여러 경로 시도)
        possible_binaries = [
            '/usr/bin/chromium-browser',
            '/usr/bin/chromium',
            '/usr/bin/google-chrome',
            '/usr/bin/google-chrome-stable'
        ]
        
        chrome_binary = None
        for binary in possible_binaries:
            if os.path.exists(binary):
                chrome_binary = binary
                break
        
        if chrome_binary:
            chrome_options.binary_location = chrome_binary
            print(f"🔧 Chrome 바이너리 찾음: {chrome_binary}")
        else:
            print("⚠️ Chrome 바이너리를 찾을 수 없어 기본값 사용")
            
        self.driver = webdriver.Chrome(options=chrome_options)
        
        # 차단 우회
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
    def search_product_image(self, product_name: str, max_attempts: int = 3) -> Optional[str]:
        """제품명으로 네이버 쇼핑에서 이미지 검색"""
        print(f"🔍 이미지 검색: {product_name}")
        
        # 검색어 정제 (브랜드명과 주요 키워드만 추출)
        clean_query = self._clean_product_name(product_name)
        print(f"   정제된 검색어: {clean_query}")
        
        for attempt in range(max_attempts):
            try:
                # 네이버 쇼핑 검색 URL 생성
                params = {
                    'query': clean_query,
                    'cat_id': '',
                    'frm': 'NVSCTAB'
                }
                search_url = self.base_url + urlencode(params, quote_via=quote)
                
                print(f"   시도 {attempt + 1}: {search_url}")
                self.driver.get(search_url)
                
                # 페이지 로딩 대기
                time.sleep(random.uniform(2, 4))
                
                # 첫 번째 상품 이미지 찾기
                wait = WebDriverWait(self.driver, 10)
                
                # 상품 리스트 컨테이너 대기
                try:
                    products_container = wait.until(
                        EC.presence_of_element_located((By.CLASS_NAME, "basicList_list_basis__uNBZx"))
                    )
                except:
                    print(f"   ❌ 상품 리스트 로딩 실패")
                    continue
                
                # BeautifulSoup으로 파싱
                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                
                # 첫 번째 상품 이미지 추출
                image_url = self._extract_first_image(soup)
                
                if image_url:
                    print(f"   ✅ 이미지 발견: {image_url[:50]}...")
                    return image_url
                else:
                    print(f"   ⚠️ 이미지 없음 - 재시도")
                    time.sleep(random.uniform(1, 2))
                    
            except Exception as e:
                print(f"   ❌ 검색 실패 (시도 {attempt + 1}): {e}")
                time.sleep(random.uniform(2, 3))
                
        print(f"   😞 {max_attempts}번 시도 후 이미지 찾기 실패")
        return None
    
    def _clean_product_name(self, product_name: str) -> str:
        """제품명 정제 - 브랜드명과 핵심 키워드만 추출"""
        # 주요 브랜드명과 제품 키워드 추출
        import re
        
        # 브랜드명 패턴
        brand_patterns = [
            r'(마켓오|Market O)',
            r'(배스킨라빈스|Baskin Robbins)',
            r'(뉴트리오코|Nutrioko)',
            r'(쿠캣|KUCAT)',
            r'(널담|Neoldam)',
            r'(젤리젤리|Jelly Jelly)', 
            r'(다네시타|Daneshita)',
            r'(매일유업|Maeil)',
            r'(던킨|Dunkin)',
            r'(허쉬|Hershey)'
        ]
        
        # 핵심 제품 키워드
        product_keywords = [
            '브라우니', '말차', '파이', '모찌', '웨이퍼', '찹쌀떡', '카스테라', 
            '쿠키', '초콜릿', '디저트', '아이스크림', '케이크', '도넛'
        ]
        
        found_brand = ""
        found_keywords = []
        
        # 브랜드명 찾기
        for pattern in brand_patterns:
            match = re.search(pattern, product_name, re.IGNORECASE)
            if match:
                found_brand = match.group(1)
                break
        
        # 핵심 키워드 찾기
        for keyword in product_keywords:
            if keyword in product_name:
                found_keywords.append(keyword)
        
        # 정제된 검색어 조합
        if found_brand and found_keywords:
            clean_query = f"{found_brand} {' '.join(found_keywords[:2])}"
        elif found_brand:
            clean_query = found_brand
        elif found_keywords:
            clean_query = ' '.join(found_keywords[:2])
        else:
            # 첫 번째 단어만 사용
            clean_query = product_name.split()[0] if product_name.split() else product_name
            
        return clean_query
    
    def _extract_first_image(self, soup: BeautifulSoup) -> Optional[str]:
        """첫 번째 상품 이미지 URL 추출"""
        try:
            # 다양한 이미지 선택자 시도
            image_selectors = [
                'img.image_item__1T4eB',  # 기본 상품 이미지
                'img.product_link__TrAac img',  # 링크 내부 이미지
                '.basicList_item__30_LI img',  # 리스트 아이템 이미지
                '.product_item__MDtDF img',  # 제품 아이템 이미지
                'img[alt*="상품"]',  # alt 텍스트에 "상품" 포함
                'img[src*="shopping"]'  # src에 "shopping" 포함
            ]
            
            for selector in image_selectors:
                images = soup.select(selector)
                if images:
                    for img in images:
                        src = img.get('src') or img.get('data-src')
                        if src and self._is_valid_image_url(src):
                            return src
                            
        except Exception as e:
            print(f"   ❌ 이미지 추출 중 오류: {e}")
            
        return None
    
    def _is_valid_image_url(self, url: str) -> bool:
        """유효한 이미지 URL인지 확인"""
        if not url:
            return False
            
        # 기본 조건들
        valid_conditions = [
            url.startswith('http'),  # HTTP/HTTPS로 시작
            any(ext in url.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp']),  # 이미지 확장자
            'shop' in url.lower(),  # 쇼핑 관련 URL
            len(url) > 20  # 충분한 길이
        ]
        
        # 제외할 URL 패턴
        exclude_patterns = [
            'logo', 'banner', 'icon', 'button', 'arrow', 'star'
        ]
        
        url_lower = url.lower()
        if any(pattern in url_lower for pattern in exclude_patterns):
            return False
            
        return all(valid_conditions)
    
    def process_ranking_data(self, json_file_path: str) -> Dict:
        """쿠팡 랭킹 JSON 파일을 읽어서 이미지 추가"""
        print(f"📊 랭킹 데이터 처리: {json_file_path}")
        
        # JSON 파일 읽기
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"❌ 파일을 찾을 수 없습니다: {json_file_path}")
            return {}
        except json.JSONDecodeError:
            print(f"❌ JSON 파싱 오류: {json_file_path}")
            return {}
        
        ranking = data.get('ranking', [])
        print(f"📋 총 {len(ranking)}개 제품 이미지 수집 시작...")
        
        # 각 제품별 이미지 수집
        success_count = 0
        for i, product in enumerate(ranking):
            print(f"\n{i+1}/{len(ranking)} 처리 중...")
            
            product_name = product.get('name', '')
            if not product_name:
                print("   ⚠️ 제품명이 없어 스킵")
                continue
            
            # 이미지 검색
            image_url = self.search_product_image(product_name)
            
            if image_url:
                product['image_url'] = image_url
                product['image_status'] = 'found'
                success_count += 1
            else:
                product['image_url'] = None
                product['image_status'] = 'not_found'
            
            # 이미지 처리 정보 추가
            product['image_processed_at'] = datetime.now().isoformat()
            
            # 딜레이 (차단 방지)
            if i < len(ranking) - 1:  # 마지막이 아니면
                delay = random.uniform(3, 6)
                print(f"   💤 {delay:.1f}초 대기...")
                time.sleep(delay)
        
        # 메타데이터 업데이트
        data['meta']['image_processing'] = {
            'processed_at': datetime.now().isoformat(),
            'total_products': len(ranking),
            'images_found': success_count,
            'success_rate': f"{(success_count/len(ranking)*100):.1f}%" if ranking else "0%"
        }
        
        print(f"\n🎯 이미지 수집 완료!")
        print(f"   📊 성공률: {success_count}/{len(ranking)} ({(success_count/len(ranking)*100):.1f}%)")
        
        return data
    
    def save_enhanced_data(self, data: Dict, output_suffix: str = "_with_images") -> str:
        """이미지가 추가된 데이터 저장"""
        if not data:
            print("❌ 저장할 데이터가 없습니다.")
            return ""
        
        # 출력 파일명 생성
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        category = data.get('meta', {}).get('category', 'products')
        filename = f"enhanced_{category}_ranking{output_suffix}_{timestamp}.json"
        
        # 데이터 저장
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"💾 향상된 데이터 저장: {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ 파일 저장 실패: {e}")
            return ""
    
    def close(self):
        """드라이버 종료"""
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()

def main():
    """메인 실행 함수"""
    print("🖼️ 네이버 쇼핑 이미지 수집기 v1.0 시작!")
    
    # 기존 쿠팡 랭킹 데이터 파일 경로
    json_file = "/mnt/d/ai/project_hub/active_projects/WhatToEat/modules/data_parser/coupang_dessert_ranking_20250709_122527.json"
    
    if not os.path.exists(json_file):
        print(f"❌ 랭킹 데이터 파일이 없습니다: {json_file}")
        return
    
    # 이미지 수집기 생성
    fetcher = NaverImageFetcher(headless=True)
    
    try:
        # 랭킹 데이터에 이미지 추가
        enhanced_data = fetcher.process_ranking_data(json_file)
        
        if enhanced_data:
            # 향상된 데이터 저장
            output_file = fetcher.save_enhanced_data(enhanced_data)
            
            if output_file:
                print(f"\n🎉 작업 완료!")
                print(f"   📁 결과 파일: {output_file}")
                print(f"   🔗 다음 단계: WhatToEat 룰렛에 이미지 연동")
        
    except Exception as e:
        print(f"❌ 실행 중 오류: {e}")
    
    finally:
        # 리소스 정리
        fetcher.close()
        print("🔚 이미지 수집기 종료")

if __name__ == "__main__":
    main()