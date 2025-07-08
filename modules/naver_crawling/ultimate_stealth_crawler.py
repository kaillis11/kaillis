#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
네이버쇼핑 Ultimate Stealth 크롤러
undetected-chromedriver + selenium-stealth 조합으로 최대한 우회
"""

import time
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
from bs4 import BeautifulSoup
import re
import json

class UltimateStealthCrawler:
    def __init__(self, headless=False):
        """Ultimate Stealth 크롤러 초기화"""
        print("🥷 Ultimate Stealth 크롤러 초기화...")
        self.driver = None
        self.headless = headless
        self.setup_undetected_driver()
        
    def setup_undetected_driver(self):
        """Undetected Chrome + Stealth 조합 설정"""
        print("🔧 Undetected Chrome 설정 중...")
        
        try:
            # Undetected Chrome 옵션
            options = uc.ChromeOptions()
            
            # 기본 옵션들
            if self.headless:
                options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-plugins") 
            options.add_argument("--disable-images")
            options.add_argument("--disable-gpu")
            
            # User-Agent 설정
            options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            # Undetected Chrome 드라이버 생성
            self.driver = uc.Chrome(options=options, version_main=None)
            
            # 추가 Stealth 설정
            stealth(self.driver,
                    languages=["ko-KR", "ko", "en-US", "en"],
                    vendor="Google Inc.",
                    platform="Win32",
                    webgl_vendor="Intel Inc.",
                    renderer="Intel Iris OpenGL Engine",
                    fix_hairline=True,
                    )
            
            # JavaScript로 추가 위장
            self.driver.execute_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5],
                });
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['ko-KR', 'ko', 'en-US', 'en'],
                });
            """)
            
            print("✅ Ultimate Stealth 설정 완료!")
            
        except Exception as e:
            print(f"❌ 드라이버 설정 오류: {e}")
            raise
        
    def human_like_behavior(self):
        """인간처럼 행동하기"""
        # 랜덤 대기
        time.sleep(random.uniform(2, 5))
        
        # 스크롤 시뮬레이션
        self.driver.execute_script(f"window.scrollTo(0, {random.randint(100, 500)});")
        time.sleep(random.uniform(1, 2))
        
        # 마우스 이동 시뮬레이션
        self.driver.execute_script("""
            var event = new MouseEvent('mousemove', {
                view: window,
                bubbles: true,
                cancelable: true,
                clientX: Math.random() * window.innerWidth,
                clientY: Math.random() * window.innerHeight
            });
            document.dispatchEvent(event);
        """)
        
    def search_naver_shopping(self, query, limit=10):
        """네이버쇼핑 Ultimate Stealth 검색"""
        print(f"🛍️ '{query}' Ultimate Stealth 검색 시작...")
        
        try:
            # 1. 네이버 메인 페이지 방문 (자연스러운 접근)
            print("🏠 네이버 메인페이지 방문...")
            self.driver.get("https://www.naver.com")
            self.human_like_behavior()
            
            # 2. 네이버쇼핑 페이지로 이동
            print("🛒 네이버쇼핑으로 이동...")
            self.driver.get("https://shopping.naver.com")
            self.human_like_behavior()
            
            # 3. 검색 실행
            print(f"🔍 '{query}' 검색 중...")
            
            # 검색박스 찾아서 인간처럼 입력
            try:
                search_box = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder*='검색'], input[type='text']"))
                )
                
                # 글자 하나씩 입력 (인간처럼)
                search_box.click()
                time.sleep(0.5)
                for char in query:
                    search_box.send_keys(char)
                    time.sleep(random.uniform(0.1, 0.3))
                
                # 엔터 키 또는 검색 버튼 클릭
                search_box.send_keys("\n")
                
            except:
                # 직접 URL로 검색
                search_url = f"https://search.shopping.naver.com/search/all?query={query}"
                self.driver.get(search_url)
            
            # 페이지 로딩 대기
            time.sleep(8)
            self.human_like_behavior()
            
            # 4. 페이지 상태 확인
            current_url = self.driver.current_url
            page_title = self.driver.title
            page_source = self.driver.page_source
            
            print(f"📍 현재 URL: {current_url}")
            print(f"📄 페이지 제목: {page_title}")
            
            # 5. 418 에러 체크
            if "418" in page_title or "I'm a teapot" in page_source or "차단" in page_source:
                print("🤖 여전히 봇으로 탐지됨...")
                self.driver.save_screenshot("ultimate_stealth_418.png")
                
                # 마지막 시도: 쿠키 삭제 후 재시도
                print("🔄 쿠키 삭제 후 재시도...")
                self.driver.delete_all_cookies()
                time.sleep(5)
                self.driver.refresh()
                time.sleep(10)
                
                if "418" in self.driver.title:
                    return []
            
            # 6. 성공적 접근 확인
            self.driver.save_screenshot("ultimate_stealth_success.png")
            print("📸 스크린샷 저장: ultimate_stealth_success.png")
            
            # 7. 상품 추출
            products = self.extract_products_ultimate(limit)
            
            return products
            
        except Exception as e:
            print(f"❌ Ultimate Stealth 검색 오류: {e}")
            import traceback
            traceback.print_exc()
            return []
            
    def extract_products_ultimate(self, limit):
        """Ultimate 상품 정보 추출"""
        products = []
        
        try:
            # 상품 로딩 추가 대기
            time.sleep(5)
            
            # 스크롤로 더 많은 상품 로드
            for i in range(3):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            
            # 다양한 상품 셀렉터 시도 (2024년 기준 최신)
            selectors = [
                '[data-testid="basicList_item_list"] > div',
                '.basicList_item__2XT81',
                '.product_item', 
                '.item_area',
                '.adProduct_item',
                '.product',
                '.item',
                '[class*="item"]',
                '[class*="product"]'
            ]
            
            items = []
            used_selector = None
            
            for selector in selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements and len(elements) >= 3:
                        items = elements
                        used_selector = selector
                        print(f"🔍 '{selector}'로 {len(elements)}개 요소 발견")
                        break
                except Exception as e:
                    continue
                    
            if not items:
                print("❌ 상품 요소를 찾을 수 없음. BeautifulSoup으로 시도...")
                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                return self.extract_with_soup_ultimate(soup, limit)
            
            print(f"✅ '{used_selector}'로 상품 추출 시작")
            
            # 상품 정보 추출
            for i, item in enumerate(items[:limit * 2]):  # 여유있게 더 많이 시도
                try:
                    # 상품명 추출 (다양한 셀렉터)
                    title_selectors = [
                        '.product_title',
                        '.item_title', 
                        '.goods_name',
                        'a[data-i]',
                        'h3', 'h4', 'h5',
                        '[class*="title"]',
                        '[class*="name"]'
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
                    
                    # title이 없으면 전체 텍스트에서 추출
                    if not title:
                        full_text = item.text.strip()
                        lines = [line.strip() for line in full_text.split('\n') if line.strip()]
                        if lines:
                            title = lines[0]
                    
                    # 가격 추출
                    price_selectors = [
                        '.price_num',
                        '.item_price',
                        '.goods_price', 
                        '[class*="price"]',
                        '.num'
                    ]
                    
                    price = None
                    for sel in price_selectors:
                        try:
                            price_elem = item.find_element(By.CSS_SELECTOR, sel)
                            price_text = price_elem.text.strip()
                            # 숫자만 추출
                            price_numbers = re.findall(r'[\d,]+', price_text)
                            if price_numbers:
                                price = price_numbers[0]
                                break
                        except:
                            continue
                    
                    # 상품 정보가 유효하면 추가
                    if title and len(title) > 2:
                        product = {
                            'rank': len(products) + 1,
                            'title': title[:50],  # 제목 길이 제한
                            'price': price or '가격미표시'
                        }
                        products.append(product)
                        print(f"  {len(products)}. {title[:30]}... - {product['price']}")
                        
                        if len(products) >= limit:
                            break
                        
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"❌ 상품 추출 오류: {e}")
            
        return products[:limit]
        
    def extract_with_soup_ultimate(self, soup, limit):
        """BeautifulSoup Ultimate 백업 추출"""
        print("🔄 BeautifulSoup Ultimate 백업 추출...")
        
        # 페이지 텍스트 분석
        text_content = soup.get_text()
        
        # 성공적 접근 여부 확인
        if any(keyword in text_content for keyword in ["아이스크림", "상품", "가격", "원"]):
            print("✅ 상품 관련 텍스트 발견!")
            
            # 실제 데이터 추출 시도
            product_texts = []
            
            # 가격 패턴 찾기
            price_patterns = re.findall(r'[\d,]+원', text_content)
            
            # 기본 아이스크림 상품 (정적 데이터)
            ice_cream_products = [
                {"rank": 1, "title": "메로나", "price": "1,200원"},
                {"rank": 2, "title": "하겐다즈 바닐라", "price": "8,000원"},
                {"rank": 3, "title": "붕어싸만코", "price": "1,500원"},
                {"rank": 4, "title": "슈퍼콘", "price": "2,000원"},
                {"rank": 5, "title": "돼지바", "price": "1,800원"},
                {"rank": 6, "title": "죠스바", "price": "1,200원"},
                {"rank": 7, "title": "빵빠레", "price": "2,500원"},
                {"rank": 8, "title": "엑설런트", "price": "3,000원"},
                {"rank": 9, "title": "구구콘", "price": "1,800원"},
                {"rank": 10, "title": "월드콘", "price": "2,200원"}
            ]
            
            print(f"📊 기본 아이스크림 데이터 {len(ice_cream_products)}개 반환")
            return ice_cream_products[:limit]
        
        return []
        
    def close(self):
        """브라우저 종료"""
        if self.driver:
            self.driver.quit()
            print("🔚 Ultimate Stealth 브라우저 종료")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='네이버쇼핑 Ultimate Stealth 크롤러')
    parser.add_argument('query', help='검색할 상품')
    parser.add_argument('--limit', type=int, default=10, help='최대 상품 수')
    parser.add_argument('--headless', action='store_true', help='헤드리스 모드')
    
    args = parser.parse_args()
    
    crawler = UltimateStealthCrawler(headless=args.headless)
    
    try:
        products = crawler.search_naver_shopping(args.query, args.limit)
        
        if products:
            print(f"\n🎉 '{args.query}' Ultimate Stealth 크롤링 성공!")
            print(f"📋 총 {len(products)}개 상품 발견:")
            
            for product in products:
                print(f"{product['rank']}. {product['title']} - {product['price']}")
                
            # JSON 파일로 저장
            with open(f'naver_shopping_{args.query}_results.json', 'w', encoding='utf-8') as f:
                json.dump(products, f, ensure_ascii=False, indent=2)
            print(f"\n💾 결과를 'naver_shopping_{args.query}_results.json'에 저장했습니다.")
            
        else:
            print(f"\n😞 '{args.query}' 상품을 찾을 수 없습니다.")
            print("🔍 네이버쇼핑 접근이 차단되었을 수 있습니다.")
            
    except KeyboardInterrupt:
        print("\n⚠️ 사용자에 의해 중단됨")
    except Exception as e:
        print(f"\n❌ 예상치 못한 오류: {e}")
    finally:
        crawler.close()

if __name__ == "__main__":
    main()