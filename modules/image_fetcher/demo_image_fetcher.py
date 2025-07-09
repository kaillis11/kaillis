#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
네이버 쇼핑 이미지 수집기 데모 버전 v1.0
실제 크롤링 없이 구조 테스트용
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional

class DemoImageFetcher:
    def __init__(self):
        """데모 이미지 수집기 초기화"""
        # 샘플 이미지 URL들 (실제 네이버 쇼핑 이미지들)
        self.sample_images = [
            "https://shopping-phinf.pstatic.net/main_2947008/29470085618.20220321172208.jpg",
            "https://shopping-phinf.pstatic.net/main_3246789/32467891234.20230215094525.jpg", 
            "https://shopping-phinf.pstatic.net/main_1892045/18920456789.20220812153042.jpg",
            "https://shopping-phinf.pstatic.net/main_4561237/45612374521.20230404201830.jpg",
            "https://shopping-phinf.pstatic.net/main_3785642/37856429863.20220925102156.jpg",
            "https://shopping-phinf.pstatic.net/main_2634785/26347856234.20230118164729.jpg",
            "https://shopping-phinf.pstatic.net/main_5729184/57291846573.20220707090315.jpg",
            "https://shopping-phinf.pstatic.net/main_4196847/41968473562.20230303130642.jpg",
            "https://shopping-phinf.pstatic.net/main_3827456/38274567894.20220519224517.jpg",
            "https://shopping-phinf.pstatic.net/main_6394572/63945728456.20230612075829.jpg"
        ]
        
    def search_product_image(self, product_name: str) -> Optional[str]:
        """제품명으로 데모 이미지 반환"""
        print(f"🔍 [데모] 이미지 검색: {product_name}")
        
        # 제품명을 기반으로 샘플 이미지 선택
        hash_value = sum(ord(c) for c in product_name)
        image_idx = hash_value % len(self.sample_images)
        selected_image = self.sample_images[image_idx]
        
        print(f"   ✅ [데모] 이미지 반환: {selected_image}")
        return selected_image
    
    def process_ranking_data(self, json_file_path: str) -> Dict:
        """쿠팡 랭킹 JSON 파일을 읽어서 데모 이미지 추가"""
        print(f"📊 [데모] 랭킹 데이터 처리: {json_file_path}")
        
        # JSON 파일 읽기
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"❌ 파일을 찾을 수 없습니다: {json_file_path}")
            return {}
        except json.JSONDecodeError:
            print(f"❌ JSON 파싱 오류: {json_file_path}")
            return {}
        
        ranking = data.get('ranking', [])
        print(f"📋 총 {len(ranking)}개 제품 데모 이미지 추가...")
        
        # 각 제품별 데모 이미지 추가
        success_count = 0
        for i, product in enumerate(ranking):
            print(f"\n{i+1}/{len(ranking)} 처리 중...")
            
            product_name = product.get('name', '')
            if not product_name:
                print("   ⚠️ 제품명이 없어 스킵")
                continue
            
            # 데모 이미지 추가
            image_url = self.search_product_image(product_name)
            
            if image_url:
                product['image_url'] = image_url
                product['image_status'] = 'demo_found'
                success_count += 1
            else:
                product['image_url'] = None
                product['image_status'] = 'demo_failed'
            
            # 이미지 처리 정보 추가
            product['image_processed_at'] = datetime.now().isoformat()
            product['image_processing_mode'] = 'demo'
        
        # 메타데이터 업데이트
        data['meta']['image_processing'] = {
            'processed_at': datetime.now().isoformat(),
            'processing_mode': 'demo',
            'total_products': len(ranking),
            'images_found': success_count,
            'success_rate': f"{(success_count/len(ranking)*100):.1f}%" if ranking else "0%"
        }
        
        print(f"\n🎯 [데모] 이미지 추가 완료!")
        print(f"   📊 성공률: {success_count}/{len(ranking)} ({(success_count/len(ranking)*100):.1f}%)")
        
        return data
    
    def save_enhanced_data(self, data: Dict, output_suffix: str = "_with_demo_images") -> str:
        """데모 이미지가 추가된 데이터 저장"""
        if not data:
            print("❌ 저장할 데이터가 없습니다.")
            return ""
        
        # 출력 파일명 생성
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        category = data.get('meta', {}).get('category', 'products')
        filename = f"demo_{category}_ranking{output_suffix}_{timestamp}.json"
        
        # 데이터 저장
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"💾 데모 데이터 저장: {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ 파일 저장 실패: {e}")
            return ""

def main():
    """메인 실행 함수"""
    print("🖼️ 네이버 쇼핑 이미지 수집기 데모 v1.0 시작!")
    
    # 기존 쿠팡 랭킹 데이터 파일 경로
    json_file = "/mnt/d/ai/project_hub/active_projects/WhatToEat/modules/data_parser/coupang_dessert_ranking_20250709_122527.json"
    
    if not os.path.exists(json_file):
        print(f"❌ 랭킹 데이터 파일이 없습니다: {json_file}")
        return
    
    # 데모 이미지 수집기 생성
    fetcher = DemoImageFetcher()
    
    try:
        # 랭킹 데이터에 데모 이미지 추가
        enhanced_data = fetcher.process_ranking_data(json_file)
        
        if enhanced_data:
            # 향상된 데이터 저장
            output_file = fetcher.save_enhanced_data(enhanced_data)
            
            if output_file:
                print(f"\n🎉 데모 작업 완료!")
                print(f"   📁 결과 파일: {output_file}")
                print(f"   🔗 다음 단계: WhatToEat 룰렛에 이미지 연동")
                print(f"   ⚠️  실제 환경에서는 naver_image_fetcher.py를 사용하세요")
        
    except Exception as e:
        print(f"❌ 실행 중 오류: {e}")
    
    print("🔚 데모 수집기 종료")

if __name__ == "__main__":
    main()