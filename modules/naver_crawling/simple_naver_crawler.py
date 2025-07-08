#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
네이버쇼핑 디저트 크롤링 시스템 (간소화 버전)
requests + BeautifulSoup만 사용
"""

import requests
import time
import random
import pandas as pd
from bs4 import BeautifulSoup
import json

class SimpleNaverCrawler:
    def __init__(self):
        """간단한 네이버쇼핑 크롤러 초기화"""
        self.session = requests.Session()
        self.setup_session()
        self.products = []
        
    def setup_session(self):
        """세션 설정"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        self.session.headers.update(headers)
        
    def crawl_dessert_products(self, max_products=20):
        """네이버쇼핑 디저트 제품 크롤링"""
        url = "https://search.shopping.naver.com/search/all?query=%EB%94%94%EC%A0%80%ED%8A%B8&sort=PURCHASE"
        
        try:
            print(f"📱 네이버쇼핑 접속 중: {url}")
            response = self.session.get(url)
            
            if response.status_code == 200:
                print("✅ 페이지 로드 성공!")
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 제품 데이터 추출
                products = self.extract_products(soup, max_products)
                return products
            else:
                print(f"❌ 페이지 로드 실패: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ 크롤링 실패: {e}")
            return []
    
    def extract_products(self, soup, max_products):
        """제품 정보 추출"""
        products = []
        
        # 여러 가능한 선택자 시도
        selectors = [
            '.basicList_item__2XT81',
            '.product_item__1XD8w',
            '.item',
            '[data-testid="product-item"]',
            '.adProduct_item__1zC9h'
        ]
        
        product_elements = []
        for selector in selectors:
            product_elements = soup.select(selector)
            if product_elements:
                print(f"✅ 제품 요소 찾음: {selector} ({len(product_elements)}개)")
                break
        
        if not product_elements:
            print("❌ 제품 요소를 찾을 수 없습니다.")
            # HTML 구조 분석을 위해 샘플 출력
            print("📋 페이지 구조 분석:")
            print(soup.prettify()[:1000])
            return []
        
        for idx, element in enumerate(product_elements[:max_products]):
            try:
                product = self.extract_product_info(element, idx + 1)
                if product:
                    products.append(product)
                    print(f"✅ {idx+1}. {product['name'][:30]}... - {product['price']}")
                
                # 요청 간 딜레이
                time.sleep(random.uniform(0.5, 1.5))
                
            except Exception as e:
                print(f"❌ 제품 {idx+1} 추출 실패: {e}")
                continue
        
        return products
    
    def extract_product_info(self, element, rank):
        """개별 제품 정보 추출"""
        product = {'rank': rank}
        
        # 제품명 추출
        name_selectors = [
            '.product_title__2-ebh',
            '.title',
            '.product_name',
            'h3',
            'h4',
            '.name'
        ]
        
        name = self.extract_text_by_selectors(element, name_selectors)
        product['name'] = name if name else f"제품 {rank}"
        
        # 가격 추출
        price_selectors = [
            '.price_num__S2p_v',
            '.price',
            '.cost',
            '.amount',
            '[class*="price"]'
        ]
        
        price = self.extract_text_by_selectors(element, price_selectors)
        product['price'] = price if price else "가격 정보 없음"
        
        # 리뷰수 추출
        review_selectors = [
            '.product_etc__LGVaW',
            '.review',
            '.count',
            '[class*="review"]'
        ]
        
        review = self.extract_text_by_selectors(element, review_selectors)
        product['reviews'] = review if review else "리뷰 정보 없음"
        
        # 링크 추출
        link_element = element.find('a', href=True)
        if link_element:
            href = link_element['href']
            if href.startswith('//'):
                href = 'https:' + href
            elif href.startswith('/'):
                href = 'https://search.shopping.naver.com' + href
            product['link'] = href
        else:
            product['link'] = "링크 없음"
        
        return product
    
    def extract_text_by_selectors(self, element, selectors):
        """여러 선택자로 텍스트 추출 시도"""
        for selector in selectors:
            found = element.select_one(selector)
            if found:
                text = found.get_text(strip=True)
                if text:
                    return text
        return None
    
    def save_to_csv(self, products, filename="naver_dessert_products.csv"):
        """결과를 CSV로 저장"""
        if not products:
            print("❌ 저장할 데이터가 없습니다.")
            return
        
        df = pd.DataFrame(products)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"💾 결과 저장 완료: {filename} ({len(products)}개 제품)")
        
        # 결과 미리보기
        print("\n📋 크롤링 결과 미리보기:")
        for i, product in enumerate(products[:5]):
            print(f"{i+1}. {product['name'][:50]}...")
            print(f"   💰 {product['price']}")
            print(f"   ⭐ {product['reviews']}")
            print()

def main():
    """메인 실행 함수"""
    print("🚀 네이버쇼핑 디저트 크롤링 시작! (간소화 버전)")
    
    crawler = SimpleNaverCrawler()
    products = crawler.crawl_dessert_products(max_products=20)
    
    if products:
        crawler.save_to_csv(products)
    else:
        print("❌ 크롤링된 제품이 없습니다.")
    
    print("🔚 크롤링 완료!")

if __name__ == "__main__":
    main()