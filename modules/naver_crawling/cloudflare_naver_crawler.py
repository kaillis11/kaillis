#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
네이버쇼핑 Cloudflare 우회 크롤러
아테나의 cloudscraper 방법론을 네이버에 적용
"""

import cloudscraper
from bs4 import BeautifulSoup
import json
import time
import random
from urllib.parse import quote
import re

class CloudflareNaverCrawler:
    def __init__(self):
        """Cloudflare 우회 스크래퍼 초기화"""
        print("🔥 Cloudflare 우회 스크래퍼 초기화...")
        self.scraper = cloudscraper.create_scraper()
        
        # 추가 헤더 설정
        self.scraper.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
    def human_delay(self, min_delay=1, max_delay=3):
        """인간적인 딜레이"""
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
        
    def get_naver_cookies(self):
        """네이버 메인에서 쿠키 획득"""
        try:
            print("🍪 네이버 메인페이지 접속하여 쿠키 획득...")
            response = self.scraper.get('https://www.naver.com', timeout=10)
            if response.status_code == 200:
                print("✅ 쿠키 획득 성공!")
                return True
            else:
                print(f"❌ 쿠키 획득 실패: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 쿠키 획득 중 오류: {e}")
            return False
            
    def search_naver_shopping(self, query, limit=10):
        """네이버쇼핑 검색 (Cloudflare 우회)"""
        print(f"🛍️ 네이버쇼핑 '{query}' 검색 시작...")
        
        # 1. 먼저 쿠키 획득
        self.get_naver_cookies()
        self.human_delay(2, 4)
        
        # 2. 검색 URL 생성
        encoded_query = quote(query)
        urls = [
            f"https://search.shopping.naver.com/search/all?query={encoded_query}",
            f"https://search.shopping.naver.com/search/all?query={encoded_query}&sort=POPULAR",
            f"https://search.shopping.naver.com/search/all?query={encoded_query}&sort=REVIEW"
        ]
        
        for i, url in enumerate(urls, 1):
            print(f"\n🔄 시도 {i}/{len(urls)}: {url}")
            
            try:
                # Cloudflare 우회 요청
                response = self.scraper.get(url, timeout=15)
                
                print(f"📊 상태 코드: {response.status_code}")
                print(f"📏 응답 크기: {len(response.content)} bytes")
                
                if response.status_code == 200:
                    print("✅ 접속 성공! HTML 파싱 시작...")
                    
                    # HTML 파싱
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # 페이지 내용 샘플 출력
                    page_text = soup.get_text()[:500]
                    print(f"📄 페이지 내용 샘플:\n{page_text}...")
                    
                    # 상품 요소 찾기
                    products = self.extract_products(soup, limit)
                    
                    if products:
                        return products
                    else:
                        print("🔍 상품 요소를 찾을 수 없음, 다음 URL 시도...")
                        
                elif response.status_code == 418:
                    print("🤖 418 에러: 여전히 봇으로 인식됨")
                else:
                    print(f"❌ HTTP 에러: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ 요청 중 오류: {e}")
                
            # 다음 시도 전 딜레이
            if i < len(urls):
                self.human_delay(3, 6)
                
        print("\n❌ 모든 시도 실패")
        return []
        
    def extract_products(self, soup, limit):
        """상품 정보 추출"""
        products = []
        
        # 다양한 상품 셀렉터 시도
        selectors = [
            'div[data-testid="basicList_item_list"] > div',
            '.product_item',
            '.item_area',
            '.goods_area',
            '[class*="item"]',
            'a[data-i]',
            '.product_link',
            '.basicList_item',
            '.item'
        ]
        
        items = []
        used_selector = None
        
        for selector in selectors:
            items = soup.select(selector)
            if items and len(items) > 2:  # 최소 3개 이상 있어야 유효
                used_selector = selector
                break
                
        if not items:
            print("❌ 상품 항목을 찾을 수 없음")
            return products
            
        print(f"🔍 '{used_selector}'로 {len(items)}개 항목 발견")
        
        for i, item in enumerate(items[:limit]):
            try:
                # 상품명 추출 (다양한 셀렉터 시도)
                title_selectors = [
                    '.product_title',
                    '.item_title', 
                    '.goods_name',
                    'a[data-i]',
                    'h3',
                    'h4',
                    '[class*="title"]',
                    '[class*="name"]'
                ]
                
                title = None
                for sel in title_selectors:
                    title_elem = item.select_one(sel)
                    if title_elem:
                        title = title_elem.get_text(strip=True)
                        if title and len(title) > 2:  # 유효한 제목인지 확인
                            break
                            
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
                    price_elem = item.select_one(sel)
                    if price_elem:
                        price_text = price_elem.get_text(strip=True)
                        # 숫자만 추출
                        price_numbers = re.findall(r'[\d,]+', price_text)
                        if price_numbers:
                            price = price_numbers[0].replace(',', '')
                            break
                
                if title:
                    product = {
                        'rank': i + 1,
                        'title': title,
                        'price': price or '가격 정보 없음'
                    }
                    products.append(product)
                    print(f"  {i+1}. {title} - {product['price']}")
                    
            except Exception as e:
                print(f"⚠️ 상품 {i+1} 파싱 오류: {e}")
                continue
                
        return products

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='네이버쇼핑 Cloudflare 우회 크롤러')
    parser.add_argument('query', help='검색할 상품')
    parser.add_argument('--limit', type=int, default=10, help='최대 상품 수')
    
    args = parser.parse_args()
    
    crawler = CloudflareNaverCrawler()
    products = crawler.search_naver_shopping(args.query, args.limit)
    
    if products:
        print(f"\n🎉 총 {len(products)}개 상품 크롤링 성공!")
        print("\n📋 아이스크림 순위:")
        for product in products:
            print(f"{product['rank']}. {product['title']} - {product['price']}")
    else:
        print("\n😞 크롤링된 상품이 없습니다.")

if __name__ == "__main__":
    main()