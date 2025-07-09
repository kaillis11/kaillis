#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WhatToEat 카드 생성기 v1.0
파싱된 데이터를 기반으로 실제 룰렛 카드 생성
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class WhatToEatCard:
    """WhatToEat 카드 데이터 클래스"""
    id: str
    title: str
    subtitle: str
    category: str
    price: str
    price_numeric: int
    rating: float
    reviews: int
    discount: Optional[str]
    original_price: Optional[str]
    image_url: Optional[str]
    description: str
    tags: List[str]
    source: str
    rank: int
    created_at: str

class CardGenerator:
    def __init__(self):
        """카드 생성기 초기화"""
        self.category_emojis = {
            'macaron': '🧁',
            'icecream': '🍦',
            'lowsugar_icecream': '🍦❄️',
            'dessert': '🍰',
            'snack': '🍪'
        }
        
        self.category_colors = {
            'macaron': '#FF69B4',
            'icecream': '#87CEEB',
            'lowsugar_icecream': '#E0F6FF',
            'dessert': '#FFE4E1',
            'snack': '#F5DEB3'
        }
        
    def generate_cards_from_json(self, json_file_path: str) -> List[WhatToEatCard]:
        """JSON 파일에서 카드 생성"""
        print(f"📄 JSON 파일 로드 중: {json_file_path}")
        
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"❌ 파일을 찾을 수 없습니다: {json_file_path}")
            return []
        
        products = data.get('products', [])
        meta = data.get('meta', {})
        
        cards = []
        for product in products:
            card = self._create_card_from_product(product, meta)
            cards.append(card)
            
        print(f"✅ {len(cards)}개 카드 생성 완료!")
        return cards
    
    def _create_card_from_product(self, product: Dict, meta: Dict) -> WhatToEatCard:
        """상품 데이터에서 카드 생성"""
        category = product.get('category', 'dessert')
        emoji = self.category_emojis.get(category, '🍽️')
        
        # 제목 생성 (브랜드 + 상품명)
        title = self._extract_brand_and_product(product['name'])
        
        # 부제목 생성 (할인 정보 포함)
        subtitle = self._generate_subtitle(product)
        
        # 설명 생성
        description = self._generate_description(product)
        
        # 태그 생성
        tags = self._generate_tags(product)
        
        # 카드 ID 생성
        card_id = f"{category}_{product['rank']:02d}_{datetime.now().strftime('%Y%m%d')}"
        
        return WhatToEatCard(
            id=card_id,
            title=title,
            subtitle=subtitle,
            category=category,
            price=product['price'],
            price_numeric=product['price_numeric'],
            rating=float(product['rating']),
            reviews=int(product['reviews'].replace(',', '')),
            discount=product.get('discount'),
            original_price=product.get('original_price'),
            image_url=None,  # 추후 이미지 크롤링으로 추가
            description=description,
            tags=tags,
            source=meta.get('title', 'Coupang'),
            rank=product['rank'],
            created_at=datetime.now().isoformat()
        )
    
    def _extract_brand_and_product(self, full_name: str) -> str:
        """제품명에서 브랜드와 핵심 상품명 추출"""
        # 브랜드 추출 패턴
        brand_patterns = [
            r'라라스윗',
            r'빙그레',
            r'롯데웰푸드',
            r'유키모찌',
            r'곰곰',
            r'파스키에',
            r'널담',
            r'러브빈마카롱',
            r'누니',
            r'코스트코'
        ]
        
        brand = "브랜드"
        for pattern in brand_patterns:
            if pattern in full_name:
                brand = pattern
                break
        
        # 핵심 상품명 추출 (첫 번째 쉼표 또는 괄호 전까지)
        core_name = full_name.split(',')[0].split('(')[0].strip()
        
        # 너무 길면 줄이기
        if len(core_name) > 30:
            core_name = core_name[:30] + "..."
        
        return f"{brand} {core_name}"
    
    def _generate_subtitle(self, product: Dict) -> str:
        """부제목 생성"""
        price = product['price']
        discount = product.get('discount')
        
        if discount:
            return f"💰 {price}원 ({discount} 할인)"
        else:
            return f"💰 {price}원"
    
    def _generate_description(self, product: Dict) -> str:
        """상품 설명 생성"""
        rating = product['rating']
        reviews = product['reviews']
        category_name = product['category_name']
        
        desc_parts = []
        
        # 순위 정보
        desc_parts.append(f"🏆 {product['rank']}위 {category_name}")
        
        # 평점 정보
        if float(rating) > 0:
            desc_parts.append(f"⭐ {rating}점")
        
        # 리뷰 수
        if reviews and reviews != '0':
            desc_parts.append(f"📝 {reviews}개 리뷰")
        
        # 할인 정보
        if product.get('discount') and product.get('original_price'):
            original = product['original_price']
            desc_parts.append(f"💸 정가 {original}원")
        
        return " | ".join(desc_parts)
    
    def _generate_tags(self, product: Dict) -> List[str]:
        """태그 생성"""
        tags = []
        
        # 카테고리 태그
        category_name = product['category_name']
        tags.append(category_name)
        
        # 할인 태그
        if product.get('discount'):
            tags.append("할인")
        
        # 평점 태그
        rating = float(product['rating'])
        if rating >= 4.5:
            tags.append("고평점")
        elif rating >= 4.0:
            tags.append("우수")
        
        # 리뷰 태그
        reviews = int(product['reviews'].replace(',', ''))
        if reviews >= 1000:
            tags.append("인기")
        
        # 가격 태그
        price = product['price_numeric']
        if price < 5000:
            tags.append("저렴")
        elif price < 10000:
            tags.append("합리적")
        else:
            tags.append("프리미엄")
        
        # 브랜드 태그
        name = product['name']
        if '라라스윗' in name:
            tags.append("라라스윗")
        elif '빙그레' in name:
            tags.append("빙그레")
        elif '롯데' in name:
            tags.append("롯데")
        
        return tags
    
    def save_cards_to_json(self, cards: List[WhatToEatCard], output_file: str = None) -> str:
        """카드 데이터를 JSON으로 저장"""
        if not output_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"whattoeat_cards_{timestamp}.json"
        
        # 카드 데이터를 딕셔너리로 변환
        cards_data = []
        for card in cards:
            cards_data.append({
                'id': card.id,
                'title': card.title,
                'subtitle': card.subtitle,
                'category': card.category,
                'price': card.price,
                'price_numeric': card.price_numeric,
                'rating': card.rating,
                'reviews': card.reviews,
                'discount': card.discount,
                'original_price': card.original_price,
                'image_url': card.image_url,
                'description': card.description,
                'tags': card.tags,
                'source': card.source,
                'rank': card.rank,
                'created_at': card.created_at
            })
        
        # JSON 파일로 저장
        output_data = {
            'meta': {
                'title': 'WhatToEat 룰렛 카드',
                'total_cards': len(cards_data),
                'generated_at': datetime.now().isoformat(),
                'version': '1.0'
            },
            'cards': cards_data
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 카드 저장 완료: {output_file}")
        return output_file
    
    def preview_cards(self, cards: List[WhatToEatCard], limit: int = 10):
        """카드 미리보기"""
        print(f"\n🎴 WhatToEat 카드 미리보기 (총 {len(cards)}개)")
        print("=" * 80)
        
        for i, card in enumerate(cards[:limit]):
            emoji = self.category_emojis.get(card.category, '🍽️')
            
            print(f"\n{emoji} [{card.id}] {card.title}")
            print(f"   {card.subtitle}")
            print(f"   📝 {card.description}")
            print(f"   🏷️ 태그: {', '.join(card.tags)}")
            print(f"   📊 순위: {card.rank}위")
            
        if len(cards) > limit:
            print(f"\n... 그 외 {len(cards) - limit}개 카드 더 있음")
    
    def generate_html_preview(self, cards: List[WhatToEatCard], output_file: str = None) -> str:
        """카드 HTML 미리보기 생성"""
        if not output_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"whattoeat_cards_preview_{timestamp}.html"
        
        html_content = self._generate_html_template(cards)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"🌐 HTML 미리보기 생성: {output_file}")
        return output_file
    
    def _generate_html_template(self, cards: List[WhatToEatCard]) -> str:
        """HTML 템플릿 생성"""
        card_html = ""
        
        for card in cards:
            emoji = self.category_emojis.get(card.category, '🍽️')
            color = self.category_colors.get(card.category, '#F0F0F0')
            
            card_html += f"""
            <div class="card" style="border-left: 4px solid {color};">
                <div class="card-header">
                    <span class="emoji">{emoji}</span>
                    <span class="rank">#{card.rank}</span>
                </div>
                <div class="card-title">{card.title}</div>
                <div class="card-subtitle">{card.subtitle}</div>
                <div class="card-description">{card.description}</div>
                <div class="card-tags">
                    {''.join(f'<span class="tag">{tag}</span>' for tag in card.tags)}
                </div>
            </div>
            """
        
        return f"""
        <!DOCTYPE html>
        <html lang="ko">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>WhatToEat 카드 미리보기</title>
            <style>
                body {{
                    font-family: 'Apple SD Gothic Neo', sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    margin: 0;
                    padding: 20px;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                }}
                .header {{
                    text-align: center;
                    color: white;
                    margin-bottom: 30px;
                }}
                .cards-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                    gap: 20px;
                }}
                .card {{
                    background: white;
                    border-radius: 12px;
                    padding: 20px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                    transition: transform 0.2s;
                }}
                .card:hover {{
                    transform: translateY(-5px);
                }}
                .card-header {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 10px;
                }}
                .emoji {{
                    font-size: 24px;
                }}
                .rank {{
                    background: #ff6b6b;
                    color: white;
                    padding: 4px 8px;
                    border-radius: 20px;
                    font-size: 12px;
                    font-weight: bold;
                }}
                .card-title {{
                    font-size: 18px;
                    font-weight: bold;
                    margin-bottom: 8px;
                    color: #333;
                }}
                .card-subtitle {{
                    font-size: 16px;
                    color: #666;
                    margin-bottom: 10px;
                }}
                .card-description {{
                    font-size: 14px;
                    color: #888;
                    margin-bottom: 15px;
                    line-height: 1.4;
                }}
                .card-tags {{
                    display: flex;
                    flex-wrap: wrap;
                    gap: 5px;
                }}
                .tag {{
                    background: #f0f0f0;
                    padding: 2px 8px;
                    border-radius: 12px;
                    font-size: 12px;
                    color: #666;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎴 WhatToEat 룰렛 카드</h1>
                    <p>파싱된 데이터로 생성된 {len(cards)}개의 카드</p>
                </div>
                <div class="cards-grid">
                    {card_html}
                </div>
            </div>
        </body>
        </html>
        """

def main():
    """메인 테스트 함수"""
    generator = CardGenerator()
    
    print("🎴 WhatToEat 카드 생성기 v1.0")
    print("📋 저당 아이스크림 카드 생성 중...")
    
    # 가장 최근 JSON 파일 찾기
    json_files = [f for f in os.listdir('.') if 'universal' in f and f.endswith('.json')]
    if not json_files:
        print("❌ 파싱된 JSON 파일을 찾을 수 없습니다.")
        return
    
    latest_file = max(json_files, key=os.path.getctime)
    print(f"📁 사용할 파일: {latest_file}")
    
    # 카드 생성
    cards = generator.generate_cards_from_json(latest_file)
    
    if cards:
        # 카드 미리보기
        generator.preview_cards(cards)
        
        # JSON 저장
        json_file = generator.save_cards_to_json(cards)
        
        # HTML 미리보기 생성
        html_file = generator.generate_html_preview(cards)
        
        print(f"\n✅ 카드 생성 완료!")
        print(f"📄 JSON 파일: {json_file}")
        print(f"🌐 HTML 미리보기: {html_file}")
        print(f"🎯 {len(cards)}개 카드가 WhatToEat 룰렛에 사용 가능합니다!")
    else:
        print("❌ 카드 생성에 실패했습니다.")

if __name__ == "__main__":
    main()