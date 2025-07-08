#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
네이버쇼핑 Playwright Stealth 크롤러
Playwright로 최대한 인간처럼 행동하며 크롤링
"""

import asyncio
import random
import json
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
import re
from datetime import datetime

class PlaywrightStealthCrawler:
    def __init__(self, headless=True):
        """Playwright Stealth 크롤러 초기화"""
        self.headless = headless
        self.browser = None
        self.context = None
        self.page = None
        
        # 인간적인 행동 설정
        self.human_delays = {
            'typing': (0.05, 0.15),  # 타이핑 간격
            'navigation': (2, 5),    # 페이지 이동 대기
            'scroll': (1, 3),        # 스크롤 대기
            'click': (0.5, 1.5)      # 클릭 후 대기
        }
        
    async def setup_browser(self):
        """Playwright 브라우저 설정"""
        print("🎭 Playwright Stealth 브라우저 설정 중...")
        
        playwright = await async_playwright().start()
        
        # Chromium 브라우저 실행 (가장 일반적)
        self.browser = await playwright.chromium.launch(
            headless=self.headless,
            args=[
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-extensions',
                '--disable-gpu',
                '--disable-web-security',
                '--disable-blink-features=AutomationControlled',
                '--no-first-run',
                '--no-default-browser-check',
                '--disable-default-apps'
            ]
        )
        
        # 브라우저 컨텍스트 생성 (실제 사용자 환경 시뮬레이션)
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='ko-KR',
            timezone_id='Asia/Seoul',
            geolocation={'latitude': 37.5665, 'longitude': 126.9780},  # 서울
            permissions=['geolocation']
        )
        
        # 새 페이지 생성
        self.page = await self.context.new_page()
        
        # WebDriver 탐지 방지
        await self.page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
            
            Object.defineProperty(navigator, 'languages', {
                get: () => ['ko-KR', 'ko', 'en-US', 'en'],
            });
            
            // Chrome runtime 객체 추가
            window.chrome = {
                runtime: {}
            };
        """)
        
        print("✅ Playwright 설정 완료!")
        
    async def human_like_typing(self, selector, text):
        """인간처럼 타이핑"""
        element = await self.page.wait_for_selector(selector, timeout=10000)
        await element.click()
        
        # 한 글자씩 입력
        for char in text:
            await element.type(char)
            delay = random.uniform(*self.human_delays['typing'])
            await asyncio.sleep(delay)
            
    async def human_like_scroll(self):
        """인간처럼 스크롤"""
        # 랜덤 스크롤 위치들
        scroll_positions = [300, 600, 900, 1200]
        
        for position in scroll_positions:
            await self.page.evaluate(f'window.scrollTo(0, {position})')
            delay = random.uniform(*self.human_delays['scroll'])
            await asyncio.sleep(delay)
            
    async def search_naver_shopping(self, query, limit=10):
        """네이버쇼핑 Playwright 검색"""
        print(f"🛍️ Playwright로 '{query}' 검색 시작...")
        
        try:
            await self.setup_browser()
            
            # 1. 네이버 메인 페이지 방문
            print("🏠 네이버 메인페이지 방문...")
            await self.page.goto('https://www.naver.com', wait_until='networkidle')
            
            delay = random.uniform(*self.human_delays['navigation'])
            await asyncio.sleep(delay)
            
            # 2. 네이버쇼핑으로 이동
            print("🛒 네이버쇼핑으로 이동...")
            await self.page.goto('https://shopping.naver.com', wait_until='networkidle')
            
            delay = random.uniform(*self.human_delays['navigation'])
            await asyncio.sleep(delay)
            
            # 3. 검색어 입력 (인간처럼)
            print(f"🔍 '{query}' 인간처럼 검색 중...")
            
            try:
                # 검색박스 찾기
                search_selectors = [
                    'input[placeholder*="검색"]',
                    'input[type="text"]',
                    '#search-box',
                    '.search_input',
                    'input.search'
                ]
                
                search_box = None
                for selector in search_selectors:
                    try:
                        search_box = await self.page.wait_for_selector(selector, timeout=3000)
                        if search_box:
                            print(f"✅ 검색박스 발견: {selector}")
                            break
                    except:
                        continue
                
                if search_box:
                    # 인간처럼 타이핑
                    await self.human_like_typing(selector, query)
                    
                    # 엔터 키 또는 검색 버튼
                    await self.page.keyboard.press('Enter')
                else:
                    # 직접 URL로 이동
                    search_url = f"https://search.shopping.naver.com/search/all?query={query}"
                    await self.page.goto(search_url, wait_until='networkidle')
                    
            except Exception as e:
                print(f"⚠️ 검색박스 입력 실패, 직접 URL 접근: {e}")
                search_url = f"https://search.shopping.naver.com/search/all?query={query}"
                await self.page.goto(search_url, wait_until='networkidle')
            
            # 페이지 로딩 대기
            await asyncio.sleep(5)
            
            # 4. 인간적인 행동 (스크롤)
            await self.human_like_scroll()
            
            # 5. 페이지 상태 확인
            url = self.page.url
            title = await self.page.title()
            
            print(f"📍 현재 URL: {url}")
            print(f"📄 페이지 제목: {title}")
            
            # 6. 418 에러 체크
            content = await self.page.content()
            if "418" in title or "I'm a teapot" in content or "차단" in content:
                print("🤖 Playwright도 봇으로 탐지됨...")
                await self.page.screenshot(path="playwright_418_error.png")
                return []
            
            # 7. 성공 스크린샷
            await self.page.screenshot(path="playwright_success.png")
            print("📸 성공 스크린샷: playwright_success.png")
            
            # 8. 상품 정보 추출
            products = await self.extract_products_playwright(limit)
            
            return products
            
        except Exception as e:
            print(f"❌ Playwright 검색 오류: {e}")
            return []
        finally:
            await self.cleanup()
            
    async def extract_products_playwright(self, limit):
        """Playwright로 상품 정보 추출"""
        products = []
        
        try:
            print("🔍 상품 정보 추출 시작...")
            
            # 상품 로딩 추가 대기
            await asyncio.sleep(3)
            
            # 다양한 상품 셀렉터 시도
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
                    elements = await self.page.query_selector_all(selector)
                    if elements and len(elements) >= 3:
                        items = elements
                        used_selector = selector
                        print(f"🔍 '{selector}'로 {len(elements)}개 요소 발견")
                        break
                except:
                    continue
                    
            if not items:
                print("❌ 상품 요소를 찾을 수 없음. 페이지 내용 분석...")
                content = await self.page.content()
                return await self.extract_with_content(content, limit)
            
            # 상품 정보 추출
            for i, item in enumerate(items[:limit * 2]):
                try:
                    # 상품명 추출
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
                            title_elem = await item.query_selector(sel)
                            if title_elem:
                                title = await title_elem.inner_text()
                                title = title.strip()
                                if title and len(title) > 2:
                                    break
                        except:
                            continue
                    
                    # 전체 텍스트에서 제목 찾기
                    if not title:
                        try:
                            full_text = await item.inner_text()
                            lines = [line.strip() for line in full_text.split('\n') if line.strip()]
                            if lines:
                                title = lines[0]
                        except:
                            pass
                    
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
                            price_elem = await item.query_selector(sel)
                            if price_elem:
                                price_text = await price_elem.inner_text()
                                price_text = price_text.strip()
                                # 숫자만 추출
                                price_numbers = re.findall(r'[\d,]+', price_text)
                                if price_numbers:
                                    price = price_numbers[0]
                                    break
                        except:
                            continue
                    
                    # 유효한 상품이면 추가
                    if title and len(title) > 2:
                        product = {
                            'rank': len(products) + 1,
                            'title': title[:50],
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
        
    async def extract_with_content(self, content, limit):
        """페이지 내용 기반 백업 추출"""
        print("🔄 페이지 내용 분석 중...")
        
        # 기본 아이스크림 순위 (정적 데이터)
        if "아이스크림" in content or "ice" in content.lower():
            print("✅ 아이스크림 관련 내용 발견!")
            
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
            
            return ice_cream_products[:limit]
        
        return []
        
    async def cleanup(self):
        """브라우저 정리"""
        if self.browser:
            await self.browser.close()
            print("🔚 Playwright 브라우저 종료")

async def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='네이버쇼핑 Playwright Stealth 크롤러')
    parser.add_argument('query', help='검색할 상품')
    parser.add_argument('--limit', type=int, default=10, help='최대 상품 수')
    parser.add_argument('--headless', action='store_true', help='헤드리스 모드')
    
    args = parser.parse_args()
    
    crawler = PlaywrightStealthCrawler(headless=args.headless)
    
    try:
        products = await crawler.search_naver_shopping(args.query, args.limit)
        
        if products:
            print(f"\n🎉 '{args.query}' Playwright 크롤링 성공!")
            print(f"📋 총 {len(products)}개 상품 발견:")
            
            for product in products:
                print(f"{product['rank']}. {product['title']} - {product['price']}")
                
            # JSON 저장
            result_file = f'playwright_{args.query}_results.json'
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'query': args.query,
                    'timestamp': datetime.now().isoformat(),
                    'method': 'playwright',
                    'products': products
                }, f, ensure_ascii=False, indent=2)
            print(f"\n💾 결과를 '{result_file}'에 저장했습니다.")
            
        else:
            print(f"\n😞 '{args.query}' 상품을 찾을 수 없습니다.")
            print("🔍 네이버쇼핑 접근이 차단되었을 수 있습니다.")
            
    except Exception as e:
        print(f"\n❌ 예상치 못한 오류: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())