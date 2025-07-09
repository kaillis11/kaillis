#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
11번가 스텔스 Selenium 크롤러 - 봇 탐지 우회 기능 포함
"""

import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from urllib.parse import quote

def test_11st_stealth():
    """11번가 스텔스 Selenium 테스트"""
    
    print("🥷 11번가 스텔스 Selenium 크롤러 시작...")
    
    # Chrome 옵션 설정 - 스텔스 모드
    options = Options()
    
    # 헤드리스 모드 일시적으로 비활성화 (디버깅용)
    # options.add_argument("--headless")
    
    # 봇 탐지 우회를 위한 옵션들
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # 일반 브라우저처럼 보이기 위한 설정
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    
    # 다양한 User-Agent 중 랜덤 선택
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0"
    ]
    options.add_argument(f"--user-agent={random.choice(user_agents)}")
    
    driver = None
    try:
        # ChromeDriver 실행
        service = Service()  # 자동으로 chromedriver 찾기
        driver = webdriver.Chrome(service=service, options=options)
        
        # 자바스크립트로 navigator.webdriver 속성 제거
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            '''
        })
        
        # 먼저 11번가 메인 페이지 방문 (쿠키 수집)
        print("🏠 11번가 메인 페이지 방문...")
        driver.get("https://www.11st.co.kr")
        time.sleep(random.uniform(2, 4))  # 랜덤 대기
        
        # 검색어 설정
        query = "아이스크림"
        encoded_query = quote(query)
        search_url = f"https://search.11st.co.kr/Search.tmall?kwd={encoded_query}"
        
        print(f"📍 검색 페이지로 이동: {search_url}")
        driver.get(search_url)
        
        # 인간적인 페이지 로딩 대기
        print("⏳ 페이지 로딩 대기...")
        time.sleep(random.uniform(3, 6))
        
        # 랜덤 스크롤 동작 (인간적인 행동 모방)
        print("🖱️ 인간적인 스크롤 동작...")
        for _ in range(3):
            scroll_height = random.randint(300, 700)
            driver.execute_script(f"window.scrollBy(0, {scroll_height});")
            time.sleep(random.uniform(0.5, 1.5))
        
        # 페이지 정보 출력
        print(f"📄 페이지 제목: {driver.title}")
        print(f"📍 현재 URL: {driver.current_url}")
        
        # 페이지 소스 저장
        with open('11st_stealth_source.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print("📄 페이지 소스 저장: 11st_stealth_source.html")
        
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
        
        # 실제 상품 데이터 추출 시도
        print("\n🛍️ 상품 데이터 추출 시도...")
        products = []
        
        # 다양한 셀렉터로 상품 찾기
        for selector in ['.c_prd_item', '.prd_info', '.list_product li', '.product_unit']:
            try:
                items = driver.find_elements(By.CSS_SELECTOR, selector)
                if items:
                    print(f"📦 '{selector}'에서 {len(items)}개 상품 발견")
                    
                    for idx, item in enumerate(items[:5]):  # 최대 5개만
                        try:
                            # 상품명 찾기
                            name_selectors = ['.c_prd_name', '.prd_name', '.title', 'a', 'h3']
                            product_name = None
                            for name_sel in name_selectors:
                                try:
                                    name_elem = item.find_element(By.CSS_SELECTOR, name_sel)
                                    product_name = name_elem.text.strip()
                                    if product_name:
                                        break
                                except:
                                    continue
                            
                            # 가격 찾기
                            price_selectors = ['.c_prd_price', '.sale_price', '.price', '.price_now']
                            product_price = None
                            for price_sel in price_selectors:
                                try:
                                    price_elem = item.find_element(By.CSS_SELECTOR, price_sel)
                                    product_price = price_elem.text.strip()
                                    if product_price:
                                        break
                                except:
                                    continue
                            
                            if product_name:
                                products.append({
                                    'name': product_name,
                                    'price': product_price or '가격정보없음'
                                })
                                print(f"  {idx+1}. {product_name} - {product_price or '가격정보없음'}")
                        
                        except Exception as e:
                            print(f"  ⚠️ 상품 {idx+1} 추출 실패: {e}")
                    
                    if products:
                        break  # 상품을 찾았으면 중단
                        
            except Exception as e:
                print(f"⚠️ '{selector}' 처리 중 오류: {e}")
        
        if products:
            print(f"\n🎉 총 {len(products)}개 상품 추출 성공!")
        else:
            print("\n😞 상품 데이터 추출 실패 - 페이지 구조가 변경되었을 수 있습니다.")
        
        # 스크린샷 저장
        driver.save_screenshot('11st_stealth_screenshot.png')
        print("📸 스크린샷 저장: 11st_stealth_screenshot.png")
        
        return True
        
    except Exception as e:
        print(f"❌ Selenium 오류: {e}")
        return False
        
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    test_11st_stealth()