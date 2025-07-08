#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
네이버쇼핑 페이지 구조 분석기
실제 HTML 구조를 분석하여 상품 셀렉터를 찾는 도구
"""

import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import time
import re
import json
from datetime import datetime

class NaverStructureAnalyzer:
    def __init__(self, headless=False):
        """구조 분석기 초기화"""
        self.headless = headless
        self.driver = None
        
    def setup_driver(self):
        """브라우저 설정"""
        print("🔧 분석용 브라우저 설정...")
        
        options = uc.ChromeOptions()
        if self.headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        self.driver = uc.Chrome(options=options)
        print("✅ 브라우저 준비 완료!")
        
    def analyze_naver_shopping_structure(self, query="아이스크림"):
        """네이버쇼핑 페이지 구조 상세 분석"""
        print(f"🔍 '{query}' 페이지 구조 분석 시작...")
        
        try:
            self.setup_driver()
            
            # 네이버쇼핑 접근
            search_url = f"https://search.shopping.naver.com/search/all?query={query}"
            print(f"📍 접근 URL: {search_url}")
            
            self.driver.get(search_url)
            time.sleep(8)  # 페이지 완전 로딩 대기
            
            # 페이지 기본 정보
            current_url = self.driver.current_url
            title = self.driver.title
            
            print(f"📄 페이지 제목: {title}")
            print(f"📍 최종 URL: {current_url}")
            
            # HTML 소스 저장
            page_source = self.driver.page_source
            with open(f'naver_shopping_{query}_source.html', 'w', encoding='utf-8') as f:
                f.write(page_source)
            print(f"💾 HTML 소스 저장: naver_shopping_{query}_source.html")
            
            # BeautifulSoup으로 구조 분석
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # 1. 모든 클래스명 수집
            all_classes = set()
            for element in soup.find_all(class_=True):
                if isinstance(element.get('class'), list):
                    all_classes.update(element.get('class'))
                else:
                    all_classes.add(element.get('class'))
            
            # 상품 관련 클래스 필터링
            product_classes = [cls for cls in all_classes if any(keyword in cls.lower() for keyword in 
                             ['product', 'item', 'goods', 'list', 'card', 'tile', 'basic'])]
            
            print(f"\n🎯 상품 관련 클래스 {len(product_classes)}개 발견:")
            for cls in sorted(product_classes)[:20]:  # 상위 20개만 표시
                print(f"  - {cls}")
            
            # 2. 반복되는 구조 찾기
            print(f"\n🔄 반복 패턴 분석...")
            
            # 상품 컨테이너 후보들
            container_candidates = [
                '[class*="list"]',
                '[class*="item"]', 
                '[class*="product"]',
                '[class*="goods"]',
                '[class*="card"]',
                '[class*="tile"]',
                '[class*="basic"]'
            ]
            
            analysis_results = {}
            
            for selector in container_candidates:
                try:
                    elements = self.driver.find_elements("css selector", selector)
                    if len(elements) > 5:  # 5개 이상 반복되는 요소
                        print(f"  🔍 '{selector}': {len(elements)}개 요소")
                        
                        # 첫 번째 요소의 HTML 구조 분석
                        if elements:
                            element_html = elements[0].get_attribute('outerHTML')
                            element_soup = BeautifulSoup(element_html, 'html.parser')
                            
                            # 텍스트 내용 확인
                            text_content = elements[0].text.strip()
                            
                            analysis_results[selector] = {
                                'count': len(elements),
                                'sample_text': text_content[:100],
                                'contains_price': bool(re.search(r'[\d,]+원', text_content)),
                                'contains_korean': bool(re.search(r'[가-힣]', text_content)),
                                'text_length': len(text_content)
                            }
                            
                except Exception as e:
                    continue
            
            # 3. 가장 유력한 상품 컨테이너 찾기
            print(f"\n🎯 상품 컨테이너 후보 분석:")
            
            best_candidates = []
            for selector, data in analysis_results.items():
                score = 0
                
                # 점수 계산
                if data['contains_price']:
                    score += 3
                if data['contains_korean']:
                    score += 2
                if 10 < data['text_length'] < 200:
                    score += 2
                if 5 <= data['count'] <= 50:
                    score += 1
                    
                if score >= 3:
                    best_candidates.append((selector, data, score))
            
            # 점수순 정렬
            best_candidates.sort(key=lambda x: x[2], reverse=True)
            
            print(f"🏆 최고 후보들:")
            for selector, data, score in best_candidates[:5]:
                print(f"  점수 {score}: {selector}")
                print(f"    - 개수: {data['count']}")
                print(f"    - 가격 포함: {data['contains_price']}")
                print(f"    - 샘플 텍스트: {data['sample_text'][:50]}...")
                print()
            
            # 4. 실제 상품 추출 테스트
            if best_candidates:
                print(f"🧪 최고 후보로 상품 추출 테스트...")
                best_selector = best_candidates[0][0]
                
                products = self.extract_products_test(best_selector)
                
                if products:
                    print(f"✅ {len(products)}개 상품 추출 성공!")
                    for i, product in enumerate(products[:3], 1):
                        print(f"  {i}. {product.get('title', 'N/A')} - {product.get('price', 'N/A')}")
                else:
                    print(f"❌ 상품 추출 실패")
            
            # 분석 결과 저장
            analysis_summary = {
                'timestamp': datetime.now().isoformat(),
                'query': query,
                'url': current_url,
                'title': title,
                'total_classes': len(all_classes),
                'product_classes': product_classes,
                'analysis_results': analysis_results,
                'best_candidates': [(sel, data, score) for sel, data, score in best_candidates]
            }
            
            with open(f'naver_structure_analysis_{query}.json', 'w', encoding='utf-8') as f:
                json.dump(analysis_summary, f, ensure_ascii=False, indent=2)
            
            print(f"\n💾 분석 결과 저장: naver_structure_analysis_{query}.json")
            
            return analysis_summary
            
        except Exception as e:
            print(f"❌ 구조 분석 오류: {e}")
            return None
        finally:
            if self.driver:
                self.driver.quit()
                
    def extract_products_test(self, selector, limit=5):
        """선택된 셀렉터로 실제 상품 추출 테스트"""
        products = []
        
        try:
            elements = self.driver.find_elements("css selector", selector)
            print(f"  🔍 {selector}로 {len(elements)}개 요소 발견")
            
            for i, element in enumerate(elements[:limit]):
                try:
                    # 텍스트 추출
                    full_text = element.text.strip()
                    
                    # 제목 추정 (첫 번째 의미있는 텍스트)
                    lines = [line.strip() for line in full_text.split('\n') if line.strip()]
                    title = lines[0] if lines else "제목없음"
                    
                    # 가격 추출
                    price_match = re.search(r'([\d,]+원)', full_text)
                    price = price_match.group(1) if price_match else "가격없음"
                    
                    # 한글이 포함된 유의미한 제목인지 확인
                    if re.search(r'[가-힣]', title) and len(title) > 2:
                        product = {
                            'rank': len(products) + 1,
                            'title': title[:50],
                            'price': price,
                            'full_text_preview': full_text[:100]
                        }
                        products.append(product)
                        
                        if len(products) >= limit:
                            break
                            
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"  ❌ 추출 테스트 오류: {e}")
            
        return products

def main():
    """메인 실행"""
    import argparse
    
    parser = argparse.ArgumentParser(description='네이버쇼핑 구조 분석기')
    parser.add_argument('--query', default='아이스크림', help='분석할 검색어')
    parser.add_argument('--headless', action='store_true', help='헤드리스 모드')
    
    args = parser.parse_args()
    
    analyzer = NaverStructureAnalyzer(headless=args.headless)
    result = analyzer.analyze_naver_shopping_structure(args.query)
    
    if result and result.get('best_candidates'):
        print(f"\n🎉 구조 분석 완료!")
        print(f"💡 최고 셀렉터: {result['best_candidates'][0][0]}")
    else:
        print(f"\n😞 구조 분석 실패")

if __name__ == "__main__":
    main()