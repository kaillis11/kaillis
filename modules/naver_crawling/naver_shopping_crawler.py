#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
네이버쇼핑 디저트 크롤링 시스템
Selenium + BeautifulSoup 조합으로 동적 콘텐츠 처리
"""

import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests

class NaverShoppingCrawler:
    def __init__(self, headless=True):
        """네이버쇼핑 크롤러 초기화"""
        self.setup_driver(headless)
        self.products = []
        
    def setup_driver(self, headless=True):
        """Selenium 드라이버 설정"""
        chrome_options = Options()
        
        # 안티-차단 설정 (WSL 환경 최적화)
        chrome_options.add_argument('--headless')  # WSL에서는 항상 headless
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--allow-running-insecure-content')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        chrome_options.add_argument('--disable-images')
        chrome_options.add_argument('--disable-javascript')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # User-Agent 설정
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        chrome_options.add_argument(f'--user-agent={random.choice(user_agents)}')
        
        # 드라이버 생성 (Chromium 사용)
        chrome_options.binary_location = '/usr/bin/chromium-browser'
        self.driver = webdriver.Chrome(options=chrome_options)
        
        # JavaScript 차단 우회
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
    def crawl_dessert_products(self, max_products=20):
        """네이버쇼핑 디저트 제품 크롤링"""
        url = "https://search.shopping.naver.com/ns/search?query=%EB%94%94%EC%A0%80%ED%8A%B8&sort=PURCHASE"
        
        try:
            print(f"📱 네이버쇼핑 접속 중: {url}")
            self.driver.get(url)
            
            # 페이지 로딩 대기
            time.sleep(random.uniform(3, 5))
            
            # 제품 리스트 로딩 대기
            wait = WebDriverWait(self.driver, 10)
            products_container = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "basicList_list_basis__uNBZx"))
            )
            
            # BeautifulSoup으로 HTML 파싱
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            # 제품 정보 추출
            product_items = soup.find_all('div', class_='product_item__MDtDF')
            
            print(f"🔍 발견된 제품 수: {len(product_items)}")
            
            for idx, item in enumerate(product_items[:max_products]):
                try:
                    product_data = self.extract_product_info(item, idx + 1)
                    if product_data:
                        self.products.append(product_data)
                        print(f"✅ {idx+1}. {product_data['name'][:50]}...")
                        
                    # 랜덤 딜레이 (차단 방지)
                    time.sleep(random.uniform(0.5, 1.5))
                    
                except Exception as e:
                    print(f"❌ 제품 {idx+1} 추출 실패: {e}")
                    continue
                    
        except Exception as e:
            print(f"❌ 크롤링 실패: {e}")
            
        return self.products
    
    def extract_product_info(self, item, rank):
        """개별 제품 정보 추출"""
        try:
            # 제품명
            name_elem = item.find('a', class_='product_link__TrAac')
            name = name_elem.get('title', '') if name_elem else ''
            
            # 가격
            price_elem = item.find('span', class_='price_num__S2p_v')
            price = price_elem.text.strip() if price_elem else ''
            
            # 리뷰 수
            review_elem = item.find('em', class_='product_grade_total__cbzMi')
            reviews = review_elem.text.strip() if review_elem else '0'
            
            # 평점
            rating_elem = item.find('span', class_='product_grade__IzyU3')
            rating = rating_elem.text.strip() if rating_elem else '0'
            
            # 판매자
            seller_elem = item.find('span', class_='product_mall__Y4cNh')
            seller = seller_elem.text.strip() if seller_elem else ''
            
            # 상품 링크
            link = name_elem.get('href', '') if name_elem else ''
            
            return {
                'rank': rank,
                'name': name,
                'price': price,
                'reviews': reviews,
                'rating': rating,
                'seller': seller,
                'link': link,
                'platform': '네이버쇼핑'
            }
            
        except Exception as e:
            print(f"❌ 제품 정보 추출 실패: {e}")
            return None
    
    def save_to_csv(self, filename='naver_shopping_desserts.csv'):
        """결과를 CSV 파일로 저장"""
        if self.products:
            df = pd.DataFrame(self.products)
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"💾 결과 저장 완료: {filename}")
            print(f"📊 총 {len(self.products)}개 제품 수집")
        else:
            print("❌ 저장할 데이터가 없습니다.")
    
    def close(self):
        """드라이버 종료"""
        if self.driver:
            self.driver.quit()

def main():
    """메인 실행 함수"""
    print("🚀 네이버쇼핑 디저트 크롤링 시작!")
    
    # 크롤러 생성 (headless=False로 하면 브라우저 창이 보임)
    crawler = NaverShoppingCrawler(headless=True)
    
    try:
        # 디저트 제품 크롤링 (상위 20개)
        products = crawler.crawl_dessert_products(max_products=20)
        
        # 결과 출력
        print("\n📋 크롤링 결과:")
        for product in products:
            print(f"{product['rank']}. {product['name'][:60]} - {product['price']} ({product['reviews']}리뷰)")
        
        # CSV 저장
        crawler.save_to_csv()
        
    except Exception as e:
        print(f"❌ 실행 중 오류: {e}")
    
    finally:
        # 리소스 정리
        crawler.close()
        print("🔚 크롤링 완료!")

if __name__ == "__main__":
    main()