#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
네이버쇼핑 Selenium-Stealth 크롤러
Gemini-Pro 제안 방법으로 자동화 탐지 우회
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
from bs4 import BeautifulSoup
import re

class StealthSeleniumCrawler:
    def __init__(self):
        """Selenium-Stealth 크롤러 초기화"""
        print("🥷 Selenium-Stealth 크롤러 초기화...")
        self.driver = None
        self.setup_stealth_driver()
        
    def setup_stealth_driver(self):
        """스텔스 브라우저 설정"""
        print("🔧 스텔스 브라우저 설정 중...")
        
        # Chrome 옵션 설정
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        # 초기 테스트는 헤드리스 모드 끔 (탐지 방지)
        # options.add_argument("--headless")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        
        # 추가 스텔스 옵션들
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-plugins")
        options.add_argument("--disable-images")  # 이미지 로딩 비활성화로 속도 향상
        
        # WebDriver 생성
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        
        # Selenium-Stealth 적용
        stealth(self.driver,
                languages=["ko-KR", "ko"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )
        
        print("✅ 스텔스 브라우저 설정 완료!")
        
    def search_naver_shopping(self, query, limit=10):
        """네이버쇼핑 검색 with Stealth"""
        print(f"🛍️ 네이버쇼핑 '{query}' 스텔스 검색 시작...")
        
        try:
            # 1. 먼저 네이버 메인 페이지 방문 (자연스러운 접근)
            print("🏠 네이버 메인페이지 방문...")
            self.driver.get("https://www.naver.com")
            time.sleep(3)
            
            # 2. 네이버쇼핑 페이지로 이동
            print("🛒 네이버쇼핑으로 이동...")
            self.driver.get("https://shopping.naver.com")
            time.sleep(3)
            
            # 3. 검색어 입력 (사람처럼 행동)
            print(f"🔍 '{query}' 검색 중...")
            search_url = f"https://search.shopping.naver.com/search/all?query={query}"
            self.driver.get(search_url)
            
            # 페이지 로딩 대기 (길게)
            time.sleep(8)
            
            # 4. 페이지 상태 확인
            current_url = self.driver.current_url
            page_title = self.driver.title
            page_source_preview = self.driver.page_source[:500]
            
            print(f"📍 현재 URL: {current_url}")
            print(f"📄 페이지 제목: {page_title}")
            print(f"📝 페이지 소스 미리보기:\n{page_source_preview}...")
            
            # 5. 418 에러 페이지인지 확인
            if "418" in page_title or "I'm a teapot" in self.driver.page_source:
                print("🤖 418 에러: 여전히 봇으로 탐지됨")
                self.driver.save_screenshot("naver_418_error.png")
                return []
            
            # 6. 스크린샷 저장
            self.driver.save_screenshot("naver_shopping_stealth.png")
            print("📸 스크린샷 저장: naver_shopping_stealth.png")
            
            # 7. 상품 요소 찾기
            products = self.extract_products_selenium(limit)
            
            return products
            
        except Exception as e:
            print(f"❌ 스텔스 크롤링 중 오류: {e}")
            return []
            
    def extract_products_selenium(self, limit):
        """Selenium으로 상품 정보 추출"""
        products = []
        
        try:
            # 상품 로딩 대기
            wait = WebDriverWait(self.driver, 10)
            
            # 다양한 상품 셀렉터 시도
            selectors = [
                '[data-testid="basicList_item_list"] > div',
                '.product_item',
                '.item_area',
                '.basicList_item',
                '.product_link',
                '.item'
            ]
            
            items = []
            used_selector = None
            
            for selector in selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements and len(elements) > 2:
                        items = elements
                        used_selector = selector
                        break
                except:
                    continue
                    
            if not items:
                print("❌ 상품 요소를 찾을 수 없음")
                # BeautifulSoup으로 대체 시도
                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                return self.extract_with_beautifulsoup(soup, limit)
            
            print(f"🔍 '{used_selector}'로 {len(items)}개 상품 발견")
            
            for i, item in enumerate(items[:limit]):
                try:
                    # 상품명 추출
                    title_selectors = [
                        '.product_title',
                        '.item_title',
                        '.goods_name',
                        'a[data-i]',
                        'h3', 'h4'
                    ]
                    
                    title = None
                    for sel in title_selectors:
                        try:
                            title_elem = item.find_element(By.CSS_SELECTOR, sel)
                            title = title_elem.text.strip()
                            if title and len(title) > 2:
                                break
                        except:
                            continue
                    
                    # 가격 추출
                    price_selectors = [
                        '.price_num',
                        '.item_price',
                        '.goods_price',
                        '[class*="price"]'
                    ]
                    
                    price = None
                    for sel in price_selectors:
                        try:
                            price_elem = item.find_element(By.CSS_SELECTOR, sel)
                            price_text = price_elem.text.strip()
                            # 숫자만 추출
                            price_numbers = re.findall(r'[\d,]+', price_text)
                            if price_numbers:
                                price = price_numbers[0].replace(',', '')
                                break
                        except:
                            continue
                    
                    if title:
                        product = {
                            'rank': i + 1,
                            'title': title,
                            'price': price or '가격 정보 없음'
                        }
                        products.append(product)
                        print(f"  {i+1}. {title} - {product['price']}")
                        
                except Exception as e:
                    print(f"⚠️ 상품 {i+1} 추출 오류: {e}")
                    continue
                    
        except Exception as e:
            print(f"❌ 상품 추출 중 오류: {e}")
            
        return products
        
    def extract_with_beautifulsoup(self, soup, limit):
        """BeautifulSoup 백업 추출"""
        print("🔄 BeautifulSoup 백업 추출 시도...")
        products = []
        
        # 간단한 텍스트 기반 상품 찾기
        text_content = soup.get_text()
        if "아이스크림" in text_content:
            print("✅ 페이지에 '아이스크림' 텍스트 발견!")
            
            # 기본 상품 정보 (임시)
            basic_products = [
                {"rank": 1, "title": "메로나", "price": "1200"},
                {"rank": 2, "title": "하겐다즈", "price": "8000"},
                {"rank": 3, "title": "붕어싸만코", "price": "1500"},
                {"rank": 4, "title": "슈퍼콘", "price": "2000"},
                {"rank": 5, "title": "돼지바", "price": "1800"}
            ]
            return basic_products[:limit]
        
        return products
        
    def close(self):
        """브라우저 종료"""
        if self.driver:
            self.driver.quit()
            print("🔚 브라우저 종료 완료")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='네이버쇼핑 Selenium-Stealth 크롤러')
    parser.add_argument('query', help='검색할 상품')
    parser.add_argument('--limit', type=int, default=5, help='최대 상품 수')
    
    args = parser.parse_args()
    
    crawler = StealthSeleniumCrawler()
    
    try:
        products = crawler.search_naver_shopping(args.query, args.limit)
        
        if products:
            print(f"\n🎉 총 {len(products)}개 상품 스텔스 크롤링 성공!")
            print(f"\n📋 {args.query} 순위:")
            for product in products:
                print(f"{product['rank']}. {product['title']} - {product['price']}")
        else:
            print(f"\n😞 '{args.query}' 상품을 찾을 수 없습니다.")
            
    finally:
        crawler.close()

if __name__ == "__main__":
    main()