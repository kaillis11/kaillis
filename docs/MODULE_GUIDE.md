# 🍽️ WhatToEat 프로젝트 모듈 가이드

**마지막 업데이트**: 2025-07-09 12:55 KST  
**작성자**: 아이리스 & 휘광님

---

## 📋 개요

WhatToEat 프로젝트에서 개발된 모든 모듈들의 완전한 사용 가이드입니다. 각 모듈은 독립적으로 사용 가능하며, 다른 프로젝트에서도 재활용할 수 있도록 설계되었습니다.

---

## 🎯 1. 메인 룰렛 시스템

### 📄 `tools/roulette_v2_premium_fusion.html`

**설명**: 무한회전 물리엔진 기반 프리미엄 음식 룰렛  
**상태**: ✅ 완성 (프로덕션 레디)

#### 🔧 주요 기능
- **무한회전 물리엔진**: 자연스러운 회전과 감속
- **24개 프리미엄 카드**: GS25 삼각김밥, 디저트, 아이스크림 등
- **반응형 디자인**: 모든 화면 크기 지원
- **NaN 방어시스템**: 수학적 오류 방지
- **클래스 기반 아키텍처**: 유지보수 용이

#### 🚀 사용법
```bash
# 웹서버 실행
cd /mnt/d/ai/project_hub/active_projects/WhatToEat/tools
python3 -m http.server 8002
# 브라우저에서 http://localhost:8002/roulette_v2_premium_fusion.html 접속
```

#### ⚙️ 설정 가능한 항목
- `CARD_WIDTH`: 카드 너비 (기본값: 450px)
- `FRICTION`: 마찰계수 (기본값: 0.98)
- `MIN_SPEED`: 최소 회전 속도 (기본값: 0.1)

#### 📝 수정 방법
1. **카드 내용 변경**: `menuData` 배열 수정
2. **디자인 변경**: CSS 클래스 `.menu-category-card` 수정
3. **물리엔진 조정**: `RouletteMath` 클래스 내부 상수 조정

---

## 📊 2. 데이터 파싱 시스템

### 📄 `modules/data_parser/improved_parser.py`

**설명**: 쿠팡 웹페이지 복사 데이터를 구조화된 JSON으로 변환  
**상태**: ✅ 완성 (검증됨)

#### 🔧 주요 기능
- **정확한 순위 추출**: 수작업 복사 데이터에서 TOP 10 추출
- **메타데이터 자동 생성**: 카테고리, 시간, 소스 정보 포함
- **가격 정규화**: 문자열과 숫자 형태 동시 제공
- **할인/배지 정보**: 쿠팡추천, 쿠폰할인 등 부가 정보

#### 🚀 사용법
```python
from improved_parser import ImprovedCoupangParser

parser = ImprovedCoupangParser()
products = parser.parse_coupang_data('dessert')  # 디저트 카테고리
parser.save_to_json(products, 'dessert')  # JSON 저장
```

#### 📥 입력 형식
- **카테고리**: `dessert`, `icecream`, `frozen`, `snack`, `drink`
- **수작업 데이터**: 쿠팡 웹페이지에서 Ctrl+A 복사한 텍스트

#### 📤 출력 형식
```json
{
  "meta": {
    "title": "쿠팡 디저트 인기 순위",
    "category": "dessert",
    "total_products": 10,
    "parsed_at": "2025-07-09T12:25:27.118270"
  },
  "ranking": [
    {
      "rank": 1,
      "name": "마켓오 브라우니 제주말차 12개입, 240g, 1개",
      "price": "5,010",
      "price_numeric": 5010,
      "reviews": "3,252",
      "rating": "5.0"
    }
  ]
}
```

### 📄 `modules/data_parser/clipboard_parser.py`

**설명**: 실시간 클립보드 파싱 시스템 (pyperclip 기반)  
**상태**: ✅ 완성 (실험적)

#### 🔧 주요 기능
- **실시간 클립보드 모니터링**: 복사 즉시 파싱
- **다중 쇼핑몰 지원**: 쿠팡, 11번가 등
- **패턴 매칭**: 정규표현식 기반 데이터 추출
- **자동 카테고리 분류**: 상품명 기반 카테고리 판별

#### 🚀 사용법
```python
from clipboard_parser import CoupangDataParser

parser = CoupangDataParser()
# 쿠팡에서 상품 리스트 복사 후
products = parser.parse_text_data(clipboard_text, 'dessert')
```

### 📄 `modules/data_parser/test_parser.py`

**설명**: 파싱 시스템 테스트 및 디버깅 도구  
**상태**: ✅ 완성 (개발용)

#### 🔧 주요 기능
- **파일 기반 테스트**: `test_coupang_data.txt` 읽어서 파싱
- **광고 필터링**: AD, 광고, 스폰서 키워드 제거
- **패턴 분석**: 다양한 정규표현식 패턴 테스트

---

## 🖼️ 3. 이미지 수집 시스템

### 📄 `modules/image_fetcher/naver_image_fetcher.py`

**설명**: 네이버 쇼핑 Selenium 기반 실제 이미지 수집기  
**상태**: 🔧 개발중 (Selenium 환경 이슈)

#### 🔧 주요 기능
- **제품명 정제**: 브랜드명 + 핵심 키워드 추출
- **다중 시도**: 실패 시 3번까지 재시도
- **이미지 검증**: 유효한 상품 이미지만 선별
- **기존 데이터 연동**: JSON 파일에 이미지 URL 추가
- **차단 방지**: 랜덤 딜레이 + User-Agent 로테이션

#### 🚀 사용법 (WSL 환경 설정 필요)
```bash
# Selenium 환경 설정 후
cd /mnt/d/ai/project_hub/active_projects/WhatToEat/modules/image_fetcher
source ../common_venv/bin/activate
python3 naver_image_fetcher.py
```

#### ⚠️ 현재 이슈
- WSL 환경에서 Chromium 설정 문제
- 타임아웃 발생 (2분 제한)
- 실제 환경에서는 작동할 것으로 예상

### 📄 `modules/image_fetcher/demo_image_fetcher.py`

**설명**: 데모용 이미지 수집기 (실제 크롤링 없이 구조 테스트)  
**상태**: ✅ 완성 (테스트용)

#### 🔧 주요 기능
- **샘플 이미지 제공**: 실제 네이버 쇼핑 이미지 URL 10개
- **해시 기반 선택**: 제품명 기반으로 일관된 이미지 매핑
- **구조 테스트**: 실제 시스템과 동일한 JSON 구조 생성
- **100% 성공률**: 모든 제품에 이미지 할당

#### 🚀 사용법
```python
from demo_image_fetcher import DemoImageFetcher

fetcher = DemoImageFetcher()
enhanced_data = fetcher.process_ranking_data('ranking.json')
fetcher.save_enhanced_data(enhanced_data)
```

#### 📤 출력 예시
```json
{
  "rank": 1,
  "name": "마켓오 브라우니 제주말차",
  "image_url": "https://shopping-phinf.pstatic.net/main_6394572/63945728456.20230612075829.jpg",
  "image_status": "demo_found",
  "image_processing_mode": "demo"
}
```

---

## 🌐 4. 크롤링 시스템 (실험적)

### 📄 `modules/naver_crawling/universal_shopping_crawler.py`

**설명**: 범용 쇼핑몰 크롤링 시스템  
**상태**: ⚠️ 실험적 (봇 차단으로 제한적)

#### 🔧 주요 기능
- **다중 쇼핑몰 지원**: 쿠팡, 11번가 설정 내장
- **백업 데이터**: 크롤링 실패 시 기본 데이터 제공
- **에러 핸들링**: 다양한 차단 방식에 대한 대응

#### ⚠️ 현실적 한계
- **쿠팡**: 강력한 봇 차단 (418 에러)
- **11번가**: JavaScript 동적 로딩으로 데이터 없음
- **네이버 쇼핑**: Selenium 필요, 환경 설정 복잡

#### 📋 결론
**수작업 복사 + 파싱** 방식이 현재 가장 현실적이고 안정적임

---

## 🔗 5. 통합 워크플로우

### 🎯 권장 사용 순서

1. **데이터 수집**
   ```bash
   # 쿠팡에서 디저트 검색 → 전체 선택 복사
   ```

2. **데이터 파싱**
   ```python
   from improved_parser import ImprovedCoupangParser
   parser = ImprovedCoupangParser()
   products = parser.parse_coupang_data('dessert')
   json_file = parser.save_to_json(products, 'dessert')
   ```

3. **이미지 추가** (데모)
   ```python
   from demo_image_fetcher import DemoImageFetcher
   fetcher = DemoImageFetcher()
   enhanced_data = fetcher.process_ranking_data(json_file)
   final_file = fetcher.save_enhanced_data(enhanced_data)
   ```

4. **룰렛 연동**
   ```javascript
   // roulette_v2_premium_fusion.html의 menuData 배열 업데이트
   ```

---

## 🛠️ 6. 개발 환경 설정

### Python 환경
```bash
# 공통 가상환경 사용
cd /mnt/d/ai/project_hub/active_projects
source common_venv/bin/activate

# 필수 패키지
pip install beautifulsoup4 requests selenium pyperclip
```

### 프로젝트 구조
```
WhatToEat/
├── tools/
│   └── roulette_v2_premium_fusion.html    # 메인 룰렛
├── modules/
│   ├── data_parser/                       # 데이터 파싱
│   ├── image_fetcher/                     # 이미지 수집
│   └── naver_crawling/                    # 크롤링 (실험적)
├── docs/
│   └── MODULE_GUIDE.md                    # 이 문서
└── common_venv/                           # 공통 가상환경
```

---

## ⭐ 7. 모듈 품질 평가

| 모듈 | 완성도 | 재사용성 | 안정성 | 문서화 |
|------|--------|----------|--------|--------|
| 메인 룰렛 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 개선된 파서 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 클립보드 파서 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| 데모 이미지 수집기 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 실제 이미지 수집기 | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| 범용 크롤러 | ⭐⭐ | ⭐⭐⭐ | ⭐ | ⭐⭐⭐ |

---

## 🚀 8. 다음 단계 로드맵

### 우선순위 1 (즉시)
- [ ] **네이버 API 공식 연동** (크롤링 대신)
- [ ] **룰렛에 이미지 데이터 실제 연동**
- [ ] **실시간 업데이트 시스템 구축**

### 우선순위 2 (단기)
- [ ] **카테고리 확장** (음료, 과자, 냉동식품)
- [ ] **쿠팡 파트너스 링크 연동**
- [ ] **모바일 최적화**

### 우선순위 3 (장기)
- [ ] **AI 추천 시스템**
- [ ] **사용자 선호도 학습**
- [ ] **다중 쇼핑몰 통합**

---

## 📞 문의 및 지원

**개발자**: 아이리스 (AI 협업 시스템)  
**프로젝트 관리자**: 휘광님  
**마지막 업데이트**: 2025-07-09 12:55 KST

이 문서는 WhatToEat 프로젝트의 모든 모듈을 다른 프로젝트에서도 활용할 수 있도록 작성되었습니다. 각 모듈은 독립적으로 사용 가능하며, 필요에 따라 커스터마이징할 수 있습니다.