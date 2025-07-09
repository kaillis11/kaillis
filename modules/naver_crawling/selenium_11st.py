#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
11번가 Selenium 크롤러 (자바스크립트 동적 로딩 대응)
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote

def test_11st_selenium():
    """11번가 Selenium 테스트"""
    
    print("🚗 11번가 Selenium 크롤러 시작...")
    
    # Chrome 옵션 설정
    options = Options()
    options.add_argument("--headless")  # 헤드리스 모드
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
    
    driver = None
    try:
        # ChromeDriver 실행
        service = Service()  # 자동으로 chromedriver 찾기
        driver = webdriver.Chrome(service=service, options=options)
        
        # 11번가 검색 페이지로 이동
        query = "아이스크림"
        encoded_query = quote(query)
        search_url = f"https://search.11st.co.kr/Search.tmall?kwd={encoded_query}"
        
        print(f"📍 URL 접속: {search_url}")
        driver.get(search_url)
        
        # 페이지 로딩 대기
        print("⏳ 페이지 로딩 대기...")
        time.sleep(5)
        
        # 페이지 정보 출력
        print(f"📄 페이지 제목: {driver.title}")
        print(f"📍 현재 URL: {driver.current_url}")
        
        # 페이지 소스 저장
        with open('11st_selenium_source.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print("📄 페이지 소스 저장: 11st_selenium_source.html")
        
        # 상품 요소 찾기 시도
        possible_selectors = [
            '.prd_info',
            '.list_product', 
            '.product_unit',
            '.c_prd_item',
            '.search_product',
            '.prd_item',
            '.product-item',
            '[data-product]',
            '.item',
            '.goods'
        ]
        
        print("\n🔍 상품 요소 찾기:")
        for selector in possible_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f"✅ '{selector}': {len(elements)}개 발견")
                else:
                    print(f"❌ '{selector}': 없음")
            except Exception as e:
                print(f"⚠️ '{selector}': 오류 - {e}")
        
        # 페이지 텍스트에서 아이스크림 키워드 찾기
        page_text = driver.find_element(By.TAG_NAME, "body").text
        print(f"\n📄 페이지 텍스트 샘플 (첫 500자):")
        print(page_text[:500])
        
        # 아이스크림 키워드 검색
        icecream_keywords = ['메로나', '하겐다즈', '붕어싸만코', '슈퍼콘', '돼지바', '아이스크림']
        found_keywords = [kw for kw in icecream_keywords if kw in page_text]
        
        if found_keywords:
            print(f"\n✅ 발견된 키워드: {', '.join(found_keywords)}")
        else:
            print(f"\n❌ 아이스크림 키워드 없음")
        
        # 스크린샷 저장
        driver.save_screenshot('11st_selenium_screenshot.png')
        print("📸 스크린샷 저장: 11st_selenium_screenshot.png")
        
        return True
        
    except Exception as e:
        print(f"❌ Selenium 오류: {e}")
        return False
        
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    test_11st_selenium()