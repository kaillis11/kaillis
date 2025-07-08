#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
네이버쇼핑 스텔스 크롤러 v2.0
최신 우회 기법과 더 정교한 브라우저 시뮬레이션
"""

import requests
import time
import random
import json
from bs4 import BeautifulSoup
from urllib.parse import quote, urlencode
import re

class StealthNaverCrawler:
    def __init__(self):
        self.session = requests.Session()
        self.setup_stealth_session()
        
    def setup_stealth_session(self):
        """최신 스텔스 헤더 설정"""
        # 최신 Chrome 헤더
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Cache-Control': 'max-age=0',
            'DNT': '1'
        }
        self.session.headers.update(headers)
        
    def human_delay(self, min_delay=1, max_delay=3):
        """인간적인 딜레이 패턴"""
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
        
    def get_naver_cookies(self):
        """네이버 메인에서 쿠키 획득"""
        try:
            print("🍪 네이버 메인페이지 접속하여 쿠키 획득...")
            response = self.session.get('https://www.naver.com', timeout=10)
            if response.status_code == 200:
                print("✅ 쿠키 획득 성공!")
                return True
            else:
                print(f"❌ 쿠키 획득 실패: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 쿠키 획득 중 오류: {e}")
            return False
            
    def alternative_search_url(self, query):
        """대안적인 검색 URL 생성"""
        # 모바일 페이지 우선 시도
        encoded_query = quote(query)
        
        urls = [
            f"https://msearch.shopping.naver.com/search/all?query={encoded_query}",
            f"https://search.shopping.naver.com/search/all?query={encoded_query}&sort=REVIEW",
            f"https://search.shopping.naver.com/search/all?query={encoded_query}&sort=POPULAR",
            f"https://search.shopping.naver.com/api/search/all?query={encoded_query}"
        ]
        
        return urls
        
    def try_multiple_approaches(self, query, limit=10):
        """여러 접근 방법 시도"""
        print(f"🎯 '{query}' 검색을 위한 다중 접근 시도...")
        
        # 1. 먼저 쿠키 획득
        if not self.get_naver_cookies():
            print("⚠️ 쿠키 없이 진행...")
            
        self.human_delay(2, 4)
        
        # 2. 여러 URL 시도
        urls = self.alternative_search_url(query)
        
        for i, url in enumerate(urls, 1):
            print(f"\n🔄 접근 방법 {i}/{len(urls)} 시도...")
            print(f"📍 URL: {url}")
            
            try:
                # Referer 설정 (자연스러운 접근처럼)
                if i > 1:
                    self.session.headers['Referer'] = 'https://www.naver.com'
                
                response = self.session.get(url, timeout=15)
                print(f"📊 상태 코드: {response.status_code}")
                print(f"📏 응답 크기: {len(response.content)} bytes")
                
                if response.status_code == 200:
                    # HTML 파싱 시도
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # 상품 요소 찾기 (여러 셀렉터 시도)
                    selectors = [
                        'div[data-testid="basicList_item_list"] > div',
                        '.product_item',
                        '.item_area',
                        '.goods_area',
                        '[class*="item"]',
                        'a[data-i]'
                    ]
                    
                    products_found = False
                    for selector in selectors:
                        items = soup.select(selector)
                        if items and len(items) > 0:
                            print(f"✅ 상품 발견! 셀렉터: {selector}, 개수: {len(items)}")
                            products_found = True
                            break
                    
                    if products_found:
                        return self.extract_products(soup, limit)
                    else:
                        print("🔍 상품 요소를 찾을 수 없음")
                        # 페이지 내용 일부 출력
                        if len(response.text) > 100:
                            print(f"📄 페이지 내용 샘플: {response.text[:200]}...")
                        
                elif response.status_code == 418:
                    print("🤖 418 에러: 봇으로 인식됨")
                else:
                    print(f"❌ HTTP 에러: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ 요청 중 오류: {e}")
                
            # 다음 시도 전 딜레이
            if i < len(urls):
                self.human_delay(3, 6)
                
        print("\n❌ 모든 접근 방법 실패")
        return []
        
    def extract_products(self, soup, limit):
        """상품 정보 추출"""
        products = []
        
        # 다양한 상품 셀렉터 시도
        selectors = [
            'div[data-testid="basicList_item_list"] > div',
            '.product_item',
            '.item_area',
            '.goods_area'
        ]
        
        items = []
        for selector in selectors:
            items = soup.select(selector)
            if items:
                break
                
        if not items:
            print("❌ 상품 항목을 찾을 수 없음")
            return products
            
        print(f"🔍 {len(items)}개 상품 항목 발견")
        
        for i, item in enumerate(items[:limit]):
            try:
                # 상품명 추출
                title_selectors = [
                    '.product_title',
                    '.item_title',
                    'a[data-i]',
                    'h3',
                    'h4',
                    '.goods_name'
                ]
                
                title = None
                for sel in title_selectors:
                    title_elem = item.select_one(sel)
                    if title_elem:
                        title = title_elem.get_text(strip=True)
                        break
                        
                # 가격 추출
                price_selectors = [
                    '.price_num',
                    '.item_price',
                    '.goods_price',
                    '[class*="price"]'
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
    
    parser = argparse.ArgumentParser(description='네이버쇼핑 스텔스 크롤러')
    parser.add_argument('query', help='검색할 상품')
    parser.add_argument('--limit', type=int, default=10, help='최대 상품 수')
    
    args = parser.parse_args()
    
    crawler = StealthNaverCrawler()
    products = crawler.try_multiple_approaches(args.query, args.limit)
    
    if products:
        print(f"\n🎉 총 {len(products)}개 상품 크롤링 성공!")
        for product in products:
            print(f"{product['rank']}. {product['title']} - {product['price']}")
    else:
        print("\n😞 크롤링된 상품이 없습니다.")

if __name__ == "__main__":
    main()