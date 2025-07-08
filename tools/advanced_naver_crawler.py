#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
네이버쇼핑 디저트 크롤링 시스템 (고급 우회 버전)
requests + 고급 헤더 설정으로 봇 차단 우회
"""

import requests
import time
import random
import pandas as pd
from bs4 import BeautifulSoup
import json

class AdvancedNaverCrawler:
    def __init__(self):
        """고급 우회 기능을 가진 크롤러 초기화"""
        self.session = requests.Session()
        self.setup_session()
        self.products = []
        
    def setup_session(self):
        """세션 설정 - 실제 브라우저처럼 보이도록"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'DNT': '1',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        }
        self.session.headers.update(headers)
        
        # 쿠키 설정 (네이버 접근 기록이 있는 것처럼)
        self.session.cookies.update({
            'NNB': 'RANDOM_VALUE',
            'nx_ssl': 'Y'
        })
        
    def get_naver_homepage_first(self):
        """먼저 네이버 홈페이지에 접속해서 쿠키를 얻음"""
        try:
            print("🏠 네이버 홈페이지 접속 중...")
            response = self.session.get('https://www.naver.com', timeout=10)
            if response.status_code == 200:
                print("✅ 네이버 홈페이지 접속 성공!")
                time.sleep(random.uniform(1, 3))
                return True
            else:
                print(f"❌ 네이버 홈페이지 접속 실패: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 네이버 홈페이지 접속 중 오류: {e}")
            return False
            
    def crawl_dessert_products(self, max_products=20):
        """네이버쇼핑 디저트 제품 크롤링"""
        # 1단계: 네이버 홈페이지 먼저 접속
        if not self.get_naver_homepage_first():
            print("❌ 사전 접속 실패")
            return []
        
        # 2단계: 쇼핑 메인 페이지 접속
        shopping_main = "https://shopping.naver.com"
        try:
            print("🛍️ 네이버쇼핑 메인 접속 중...")
            response = self.session.get(shopping_main, timeout=10)
            if response.status_code == 200:
                print("✅ 네이버쇼핑 메인 접속 성공!")
                time.sleep(random.uniform(2, 4))
            else:
                print(f"⚠️ 네이버쇼핑 메인 접속 실패: {response.status_code}")
        except Exception as e:
            print(f"⚠️ 네이버쇼핑 메인 접속 중 오류: {e}")
        
        # 3단계: 검색 페이지 접속
        search_url = "https://search.shopping.naver.com/search/all"
        params = {
            'query': '디저트',
            'cat_id': '',
            'frm': 'NVSHATC'
        }
        
        try:
            print(f"🔍 디저트 검색 중...")
            
            # Referer 헤더 추가
            self.session.headers.update({
                'Referer': 'https://shopping.naver.com/'
            })
            
            response = self.session.get(search_url, params=params, timeout=15)
            
            print(f"📊 응답 상태: {response.status_code}")
            print(f"📏 응답 크기: {len(response.text)} bytes")
            
            if response.status_code == 200:
                print("✅ 검색 페이지 로드 성공!")
                
                # 응답 내용 일부 확인
                if len(response.text) > 1000:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    products = self.extract_products_advanced(soup, max_products)
                    return products
                else:
                    print("❌ 응답 내용이 너무 짧습니다 (차단된 것 같습니다)")
                    return []
            else:
                print(f"❌ 검색 페이지 로드 실패: {response.status_code}")
                if response.status_code == 418:
                    print("🤖 봇으로 인식되어 차단되었습니다")
                elif response.status_code == 403:
                    print("🚫 접근이 금지되었습니다")
                return []
                
        except Exception as e:
            print(f"❌ 크롤링 실패: {e}")
            return []
    
    def extract_products_advanced(self, soup, max_products):
        """고급 제품 정보 추출"""
        products = []
        
        # 페이지 구조 분석
        print("🔍 페이지 구조 분석 중...")
        
        # 다양한 선택자 패턴 시도
        selectors_to_try = [
            # 최신 네이버쇼핑 구조
            'div[data-testid="basicList"] > div',
            '.basicList_item__0T9JD',
            '.basicList_item__2XT81', 
            '.product_item__1XD8w',
            '.adProduct_item__1zC9h',
            # 일반적인 상품 컨테이너
            '.item',
            '[class*="item"]',
            '[class*="product"]',
            # 링크 기반
            'a[href*="/shopping/"]',
            'a[href*="nvMid"]'
        ]
        
        product_elements = []
        used_selector = None
        
        for selector in selectors_to_try:
            elements = soup.select(selector)
            if elements and len(elements) >= 3:  # 최소 3개 이상 찾아야 유의미
                product_elements = elements
                used_selector = selector
                print(f"✅ 제품 요소 발견: {selector} ({len(elements)}개)")
                break
        
        if not product_elements:
            print("❌ 제품 요소를 찾을 수 없습니다.")
            # 디버깅을 위한 HTML 구조 출력
            print("\n📋 HTML 구조 샘플:")
            sample_divs = soup.find_all('div', limit=10)
            for div in sample_divs:
                if div.get('class'):
                    print(f"  div.{'.'.join(div['class'])}")
            return []
        
        print(f"🎯 선택된 선택자: {used_selector}")
        
        # 제품 정보 추출
        for idx, element in enumerate(product_elements[:max_products]):
            try:
                product = self.extract_single_product(element, idx + 1)
                if product and product.get('name') and product['name'] != f"제품 {idx + 1}":
                    products.append(product)
                    print(f"✅ {len(products)}. {product['name'][:40]}...")
                
                # 처리 간 딜레이
                time.sleep(random.uniform(0.1, 0.3))
                
            except Exception as e:
                print(f"❌ 제품 {idx+1} 처리 실패: {e}")
                continue
        
        return products
    
    def extract_single_product(self, element, rank):
        """개별 제품 정보 추출"""
        product = {'rank': rank}
        
        # 제품명 추출 (다양한 패턴)
        name_patterns = [
            '.product_title',
            '.productTitle',
            '.title',
            'h3', 'h4', 'h5',
            '[class*="title"]',
            '[class*="name"]',
            'a[title]'  # title 속성에서 제품명 추출
        ]
        
        name = None
        for pattern in name_patterns:
            elem = element.select_one(pattern)
            if elem:
                name = elem.get_text(strip=True)
                if not name and elem.get('title'):  # title 속성 체크
                    name = elem['title'].strip()
                if name and len(name) > 2:  # 유의미한 길이
                    break
        
        product['name'] = name if name else f"제품 {rank}"
        
        # 가격 추출
        price_patterns = [
            '.price_num',
            '.price',
            '.cost',
            '[class*="price"]',
            '[class*="cost"]',
            '.num'
        ]
        
        price = None
        for pattern in price_patterns:
            elem = element.select_one(pattern)
            if elem:
                price_text = elem.get_text(strip=True)
                # 숫자가 포함된 경우만
                if any(char.isdigit() for char in price_text):
                    price = price_text
                    break
        
        product['price'] = price if price else "가격 정보 없음"
        
        # 리뷰 정보 추출
        review_patterns = [
            '.review',
            '.count',
            '[class*="review"]',
            '[class*="count"]',
            '.etc'
        ]
        
        review = None
        for pattern in review_patterns:
            elem = element.select_one(pattern)
            if elem:
                review_text = elem.get_text(strip=True)
                if review_text and ('리뷰' in review_text or any(char.isdigit() for char in review_text)):
                    review = review_text
                    break
        
        product['reviews'] = review if review else "리뷰 정보 없음"
        
        # 링크 추출
        link_elem = element.find('a', href=True)
        if link_elem:
            href = link_elem['href']
            if href.startswith('//'):
                href = 'https:' + href
            elif href.startswith('/'):
                href = 'https://search.shopping.naver.com' + href
            product['link'] = href
        else:
            product['link'] = "링크 없음"
        
        return product
    
    def save_to_csv(self, products, filename="naver_dessert_advanced.csv"):
        """결과를 CSV로 저장"""
        if not products:
            print("❌ 저장할 데이터가 없습니다.")
            return
        
        df = pd.DataFrame(products)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"💾 결과 저장 완료: {filename} ({len(products)}개 제품)")
        
        # 결과 미리보기
        print("\n📋 크롤링 결과 미리보기:")
        for i, product in enumerate(products[:3]):
            print(f"{i+1}. 📦 {product['name'][:50]}")
            print(f"   💰 {product['price']}")
            print(f"   ⭐ {product['reviews']}")
            print(f"   🔗 {product['link'][:80]}...")
            print()

def main():
    """메인 실행 함수"""
    print("🚀 네이버쇼핑 디저트 크롤링 시작! (고급 우회 버전)")
    
    crawler = AdvancedNaverCrawler()
    products = crawler.crawl_dessert_products(max_products=10)  # 먼저 10개로 테스트
    
    if products:
        crawler.save_to_csv(products)
        print(f"🎉 성공! {len(products)}개 제품 크롤링 완료!")
    else:
        print("❌ 크롤링된 제품이 없습니다.")
        print("💡 네이버쇼핑의 봇 차단이 강화되었을 수 있습니다.")
    
    print("🔚 크롤링 완료!")

if __name__ == "__main__":
    main()