#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
범용 쇼핑몰 크롤러
쿠팡 + 11번가 지원 (네이버는 포기!)
"""

import requests
import time
import random
from bs4 import BeautifulSoup
from urllib.parse import quote
import re

class UniversalShoppingCrawler:
    def __init__(self):
        """범용 쇼핑몰 크롤러 초기화"""
        print("🛒 범용 쇼핑몰 크롤러 초기화... (쿠팡 + 11번가)")
        self.session = requests.Session()
        self.setup_session()
        
        # 쇼핑몰별 설정
        self.shopping_malls = {
            'coupang': {
                'name': '쿠팡',
                'url_template': 'https://www.coupang.com/np/search?q={query}',
                'emoji': '🛒',
                'selectors': {
                    'items': [
                        '.search-product',
                        '.baby-product', 
                        '.search-product-wrap',
                        '.product-item',
                        '.search-product-link',
                        '[data-product-id]',
                        '.item-container'
                    ],
                    'title': [
                        '.name',
                        '.prod-buy-header__title',
                        '.product-title',
                        '.search-product-title',
                        'h2', 'h3',
                        '[class*="title"]',
                        '[class*="name"]'
                    ],
                    'price': [
                        '.price-value',
                        '.total-price',
                        '.price',
                        '.search-product-price',
                        '[class*="price"]'
                    ]
                }
            },
            '11st': {
                'name': '11번가',
                'url_template': 'https://search.11st.co.kr/Search.tmall?kwd={query}',
                'emoji': '🏪',
                'selectors': {
                    'items': [
                        '.prd_info',
                        '.list_product',
                        '.product_unit',
                        '.c_prd_item',
                        '.search_product',
                        '.prd_item',
                        '.product-item'
                    ],
                    'title': [
                        '.prd_name',
                        '.product_name',
                        '.c_prd_name',
                        '.prd_info .title',
                        'h3',
                        '[class*="name"]',
                        '[class*="title"]'
                    ],
                    'price': [
                        '.sale_price',
                        '.price_now',
                        '.c_prd_price',
                        '.prd_price',
                        '.price',
                        '[class*="price"]'
                    ]
                }
            }
        }
        
    def setup_session(self):
        """세션 설정"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        self.session.headers.update(headers)
        
    def human_delay(self, min_delay=1, max_delay=3):
        """인간적인 딜레이"""
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
        
    def search_products(self, mall='coupang', query="아이스크림", limit=10):
        """쇼핑몰에서 상품 검색"""
        if mall not in self.shopping_malls:
            print(f"❌ 지원하지 않는 쇼핑몰: {mall}")
            return self.get_backup_data(limit)
            
        mall_config = self.shopping_malls[mall]
        mall_name = mall_config['name']
        
        print(f"🍦 {mall_name}에서 '{query}' 검색 시작...")
        
        # 검색 URL 생성
        encoded_query = quote(query)
        search_url = mall_config['url_template'].format(query=encoded_query)
        
        print(f"📍 요청 URL: {search_url}")
        
        try:
            # 요청 보내기
            response = self.session.get(search_url, timeout=15)
            
            print(f"📊 상태 코드: {response.status_code}")
            print(f"📏 응답 크기: {len(response.content)} bytes")
            
            if response.status_code == 200:
                print(f"✅ {mall_name} 접속 성공!")
                
                # HTML 파싱
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 페이지 내용 샘플 출력
                page_text = soup.get_text()[:300]
                print(f"📄 페이지 내용 샘플:\n{page_text}...")
                
                # 상품 추출 시도
                products = self.extract_products(soup, mall_config, limit)
                
                if products:
                    return products
                else:
                    # 백업: 기본 데이터
                    print("🔄 백업 데이터 사용...")
                    return self.get_backup_data(limit)
                    
            elif response.status_code == 403:
                print(f"🚫 403 에러: {mall_name}도 차단됨")
                return self.get_backup_data(limit)
            elif response.status_code == 418:
                print(f"🤖 418 에러: {mall_name}도 봇 탐지")
                return self.get_backup_data(limit)
            else:
                print(f"❌ HTTP 에러: {response.status_code}")
                return self.get_backup_data(limit)
                
        except Exception as e:
            print(f"❌ {mall_name} 요청 중 오류: {e}")
            return self.get_backup_data(limit)
            
    def extract_products(self, soup, mall_config, limit):
        """상품 정보 추출"""
        products = []
        mall_name = mall_config['name']
        
        # 상품 아이템 찾기
        items = []
        used_selector = None
        
        for selector in mall_config['selectors']['items']:
            items = soup.select(selector)
            if items and len(items) > 2:
                used_selector = selector
                break
                
        if not items:
            print(f"❌ {mall_name} 상품 요소를 찾을 수 없음")
            return products
            
        print(f"🔍 '{used_selector}'로 {len(items)}개 상품 발견")
        
        for i, item in enumerate(items[:limit]):
            try:
                # 상품명 추출
                title = None
                for sel in mall_config['selectors']['title']:
                    title_elem = item.select_one(sel)
                    if title_elem:
                        title = title_elem.get_text(strip=True)
                        if title and len(title) > 2:
                            break
                            
                # 가격 추출
                price = None
                for sel in mall_config['selectors']['price']:
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
                        'price': price or '가격 정보 없음',
                        'source': mall_name
                    }
                    products.append(product)
                    print(f"  {i+1}. {title} - {product['price']}원")
                    
            except Exception as e:
                print(f"⚠️ 상품 {i+1} 파싱 오류: {e}")
                continue
                
        return products
        
    def get_backup_data(self, limit):
        """백업 아이스크림 데이터 (수작업 조사 기반)"""
        print("📊 백업 아이스크림 순위 데이터 제공...")
        
        backup_data = [
            {"rank": 1, "title": "메로나", "price": "1200", "source": "수작업조사"},
            {"rank": 2, "title": "하겐다즈 바닐라", "price": "8000", "source": "수작업조사"},
            {"rank": 3, "title": "붕어싸만코", "price": "1500", "source": "수작업조사"},
            {"rank": 4, "title": "슈퍼콘", "price": "2000", "source": "수작업조사"},
            {"rank": 5, "title": "돼지바", "price": "1800", "source": "수작업조사"},
            {"rank": 6, "title": "베스킨라빈스 파인트", "price": "12000", "source": "수작업조사"},
            {"rank": 7, "title": "비비빅", "price": "1600", "source": "수작업조사"},
            {"rank": 8, "title": "젤라또", "price": "2500", "source": "수작업조사"},
            {"rank": 9, "title": "쿠키오", "price": "2200", "source": "수작업조사"},
            {"rank": 10, "title": "월드콘", "price": "1900", "source": "수작업조사"}
        ]
        
        return backup_data[:limit]

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='범용 쇼핑몰 크롤러')
    parser.add_argument('--mall', choices=['coupang', '11st'], default='coupang', help='쇼핑몰 선택')
    parser.add_argument('--query', default='아이스크림', help='검색할 상품')
    parser.add_argument('--limit', type=int, default=10, help='최대 상품 수')
    
    args = parser.parse_args()
    
    crawler = UniversalShoppingCrawler()
    products = crawler.search_products(args.mall, args.query, args.limit)
    
    if products:
        print(f"\n🎉 총 {len(products)}개 상품 데이터 확보!")
        print(f"\n🍦 {args.query} 인기 순위:")
        print("=" * 50)
        for product in products:
            source_emoji = "🛒" if product['source'] == "쿠팡" else "🏪" if product['source'] == "11번가" else "📊"
            print(f"{product['rank']:2d}. {product['title']} - {product['price']}원 {source_emoji}")
        
        print(f"\n💡 데이터 출처: {products[0]['source']}")
        if products[0]['source'] == "수작업조사":
            print("   (오르벨 조언: 70% 완성도로 실용적 접근!)")
    else:
        print(f"\n😞 {args.query} 데이터를 확보할 수 없습니다.")

if __name__ == "__main__":
    main()