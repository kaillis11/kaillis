#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
11번가 HTML 구조 분석 도구
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

def analyze_11st_structure():
    """11번가 페이지 구조 분석"""
    
    # 세션 설정
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    session.headers.update(headers)
    
    # 11번가 검색
    query = "아이스크림"
    encoded_query = quote(query)
    search_url = f"https://search.11st.co.kr/Search.tmall?kwd={encoded_query}"
    
    print(f"🔍 11번가 구조 분석 시작...")
    print(f"📍 URL: {search_url}")
    
    try:
        response = session.get(search_url, timeout=15)
        print(f"📊 상태 코드: {response.status_code}")
        print(f"📏 응답 크기: {len(response.content)} bytes")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # HTML 구조 샘플 저장
            with open('11st_sample.html', 'w', encoding='utf-8') as f:
                f.write(soup.prettify())
            print("📄 HTML 샘플 저장: 11st_sample.html")
            
            # 클래스 이름들 찾기
            print("\n🔍 발견된 클래스들:")
            all_classes = set()
            for element in soup.find_all(True):
                if element.get('class'):
                    for cls in element.get('class'):
                        all_classes.add(cls)
            
            # 상품 관련 클래스 필터링
            product_classes = [cls for cls in all_classes if any(keyword in cls.lower() for keyword in 
                             ['product', 'item', 'prd', 'goods', 'list', 'search', 'result'])]
            
            print("📦 상품 관련 클래스들:")
            for cls in sorted(product_classes)[:20]:  # 상위 20개만
                print(f"  .{cls}")
            
            # div 태그들의 클래스 분석
            print("\n🏗️ div 태그 클래스 분석:")
            div_classes = set()
            for div in soup.find_all('div'):
                if div.get('class'):
                    for cls in div.get('class'):
                        if any(keyword in cls.lower() for keyword in ['product', 'item', 'prd', 'goods']):
                            div_classes.add(cls)
            
            for cls in sorted(div_classes)[:15]:
                print(f"  div.{cls}")
            
            # 실제 상품 검색 (텍스트 기반)
            print("\n🍦 아이스크림 관련 텍스트 찾기:")
            page_text = soup.get_text()
            icecream_keywords = ['메로나', '하겐다즈', '붕어싸만코', '슈퍼콘', '돼지바', '아이스크림']
            
            found_keywords = []
            for keyword in icecream_keywords:
                if keyword in page_text:
                    found_keywords.append(keyword)
            
            if found_keywords:
                print(f"✅ 발견된 키워드: {', '.join(found_keywords)}")
                print("💡 실제 상품 데이터가 페이지에 있음!")
            else:
                print("❌ 아이스크림 관련 키워드 없음")
                print("🤔 동적 로딩이거나 다른 구조일 수 있음")
            
            # 페이지 소스 일부 출력
            print(f"\n📄 페이지 내용 샘플 (첫 1000자):")
            print(page_text[:1000])
            
    except Exception as e:
        print(f"❌ 분석 중 오류: {e}")

if __name__ == "__main__":
    analyze_11st_structure()