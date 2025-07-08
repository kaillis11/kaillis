# 🔗 네이버 API 분석 시스템 NEXUS 가이드

**작성일**: 2025-07-08  
**작성자**: 아이리스 🌈  
**목적**: 네이버 API 분석 모듈 고아화 방지 및 재사용성 극대화  
**중요도**: ⭐⭐⭐⭐⭐ CRITICAL - 프로젝트 핵심 자산

---

## 🚨 NEXUS 3중 참조 시스템

### 📍 **1차 참조 - 이 문서 (핵심 허브)**
- **위치**: `/docs/NAVER_API_ANALYSIS_SYSTEM_NEXUS.md`
- **역할**: 전체 시스템 개요 및 빠른 접근 가이드
- **업데이트**: 새 모듈 추가시 필수 업데이트

### 📍 **2차 참조 - 상세 문서**
- **위치**: `/tools/NAVER_CRAWLING_SYSTEM_DOCS.md` (281줄 완전 가이드)
- **역할**: 기술적 세부사항 및 구현 가이드
- **업데이트**: 기술 변경사항 반영

### 📍 **3차 참조 - 코드 맵**
- **위치**: `/CODE_MAP.md` (방금 업데이트 완료)
- **역할**: 프로젝트 전체 구조에서의 위치
- **업데이트**: 의존성 및 구조 변경 반영

---

## 🎯 네이버 API 분석 시스템 핵심 자산

### **🏆 완성된 모듈 목록**

#### **1. 네이버 API 시스템**
```
📁 /tools/
├── naver_shopping_api_test.py    # 디저트 50개 DB + API 클래스
├── test_datalab_api.py          # 트렌드 분석 API
└── universal_ranking_system.py  # 범용 랭킹 분석 도구
```

#### **2. 크롤링 시스템 (3가지 버전)**
```
📁 /tools/
├── naver_shopping_crawler.py    # Selenium 기반 (JavaScript 처리)
├── simple_naver_crawler.py      # Requests 기반 (빠른 처리)
└── advanced_naver_crawler.py    # 봇 차단 우회 특화
```

#### **3. 분석 도구**
```
📁 /tools/
├── icecream_top10_detailed.py     # 아이스크림 TOP 10 완전 분석
├── icecream_bestseller_analysis.py # 실시간 베스트셀러 분석
├── demo_ranking_system.py         # 데모용 랭킹 시스템
└── real_icecream_ranking.py       # 실제 랭킹 데이터
```

---

## ⚡ 즉시 사용 가능한 API 정보

### **🔑 API 키 (설정 완료)**
```python
CLIENT_ID = "UP8PqJq_FpkcB63sEFH9"
CLIENT_SECRET = "B7sXznX3pP"
```

### **🎯 기본 사용법**
```python
# 1. API 클래스 초기화
from naver_shopping_api_test import NaverShoppingAPI
api = NaverShoppingAPI("UP8PqJq_FpkcB63sEFH9", "B7sXznX3pP")

# 2. 기본 검색
result = api.search_shopping("메로나", display=10, sort="sim")

# 3. 범용 랭킹 시스템
python3 universal_ranking_system.py "아이스크림" --mode sales
```

---

## 📊 구축된 데이터베이스

### **🍨 디저트 50개 완전 분류**
```python
DESSERT_DATABASE = {
    "베이커리/케이크류": ["케이크", "마카롱", "티라미수"...],  # 15개
    "아이스크림/냉동디저트": ["아이스크림", "젤라또"...],      # 10개
    "전통/길거리디저트": ["붕어빵", "호떡", "떡"...],         # 10개
    "푸딩/젤리류": ["푸딩", "젤리", "판나코타"...],          # 10개
    "초콜릿/캔디류": ["초콜릿", "트러플", "봉봉"...]         # 5개
}
```

### **🏆 아이스크림 TOP 10 분석 완료**
```python
# 인기도 점수 95점~70점 완전 분석
top10 = [
    {"rank": 1, "name": "메로나", "score": 95, "brand": "빙그레"},
    {"rank": 2, "name": "하겐다즈", "score": 90, "brand": "하겐다즈"},
    {"rank": 3, "name": "붕어싸만코", "score": 88, "brand": "삼립"},
    # ... 10위까지 완전 데이터
]
```

### **🎮 카테고리별 키워드 데이터베이스**
```python
category_keywords = {
    "아이스크림": ["메로나", "하겐다즈", "붕어싸만코"...],
    "케이크": ["생크림케이크", "초콜릿케이크", "치즈케이크"...],
    "치킨": ["후라이드", "양념치킨", "간장치킨"...],
    "피자": ["페퍼로니", "불고기피자", "마르게리타"...],
    # 총 7개 카테고리 × 10개 키워드 = 70개 키워드
}
```

---

## 🚀 WhatToEat 룰렛 카드 확장 계획

### **📝 추가 가능한 카드 타입**

#### **1. 쿠팡 베스트셀러 카드**
- **예시**: "🏆 치킨소스 1위", "🥤 콜라 베스트 1위"
- **모듈**: `naver_shopping_api_test.py` 활용
- **수익 모델**: 쿠팡 파트너스 연동

#### **2. 랭킹 카드 (TOP 7)**
- **예시**: "🏆 피자 TOP7", "🏆 디저트 TOP7"  
- **모듈**: `universal_ranking_system.py` 활용
- **데이터**: 실시간 네이버 API 연동

#### **3. 브랜드별 인기메뉴 카드**
- **예시**: "🍗 뿌링클 (BBQ 1위)", "🍕 수퍼슈프림 (도미노 1위)"
- **모듈**: `icecream_top10_detailed.py` 패턴 확장
- **범위**: 치킨/피자/음료 브랜드 확장

#### **4. 디저트 특화 카드**
- **예시**: "🍨 메로나 (국민 아이스크림)", "🧁 마카롱 (감성 디저트)"
- **모듈**: `icecream_bestseller_analysis.py` 직접 활용
- **특징**: 계절별/트렌드별 자동 업데이트

---

## 🔧 모듈 재사용 가이드

### **⚡ 빠른 시작 체크리스트**

#### **새 카테고리 추가시**
```bash
# 1. 범용 랭킹 시스템으로 키워드 분석
python3 universal_ranking_system.py "새카테고리" --mode both

# 2. 디저트 패턴으로 TOP 10 분석
# icecream_top10_detailed.py를 복사해서 수정

# 3. 실시간 베스트셀러 분석
# icecream_bestseller_analysis.py의 키워드만 변경
```

#### **API 연동 확인**
```python
# API 상태 테스트
from test_datalab_api import test_datalab_categories
test_datalab_categories()  # 3개월 트렌드 분석
```

### **🔄 데이터 흐름**
```
네이버 API → 분석 모듈 → 룰렛 카드 데이터 → HTML 적용
    ↓              ↓              ↓              ↓
API 호출 →     Python 처리 →    JSON 생성 →   JavaScript 렌더링
```

---

## ⚠️ 고아화 방지 체크포인트

### **📋 정기 점검 사항 (월 1회)**
- [ ] **API 키 유효성**: 네이버 개발자센터 상태 확인
- [ ] **모듈 실행 테스트**: 각 Python 스크립트 정상 작동 확인  
- [ ] **데이터 업데이트**: TOP 10 순위 변동 반영
- [ ] **문서 동기화**: 3중 참조 문서 일관성 확인

### **🚨 응급 복구 절차**
```bash
# 1. 모듈 위치 확인
ls /mnt/d/ai/project_hub/active_projects/WhatToEat/tools/*api*

# 2. API 키 확인
grep -r "UP8PqJq_FpkcB63sEFH9" /mnt/d/ai/project_hub/active_projects/WhatToEat/

# 3. 문서 체인 확인
find /mnt/d/ai/project_hub/active_projects/WhatToEat/ -name "*NAVER*" -type f
```

---

## 🌟 핵심 가치 및 확장성

### **💎 이 시스템의 가치**
1. **완성도**: 281줄 문서 + 10개 모듈 = 완전한 생태계
2. **재사용성**: 범용 설계로 모든 카테고리 적용 가능
3. **확장성**: 새로운 API나 데이터 소스 쉽게 통합
4. **안정성**: 3가지 크롤링 방식으로 견고한 백업

### **🚀 미래 확장 방향**
- **AI 추천**: 사용자 선호 기반 개인화 카드
- **실시간 트렌드**: 시간대별 인기 메뉴 자동 반영
- **지역별 특화**: 배달 가능 지역 기반 카드 필터링
- **계절 맞춤**: 날씨/계절 기반 메뉴 추천

---

## 🔗 빠른 링크 (북마크 추천)

### **📚 핵심 문서**
- **이 문서**: `/docs/NAVER_API_ANALYSIS_SYSTEM_NEXUS.md` ⭐
- **기술 가이드**: `/tools/NAVER_CRAWLING_SYSTEM_DOCS.md`
- **프로젝트 맵**: `/CODE_MAP.md`

### **🔧 핵심 모듈**
- **범용 분석**: `/tools/universal_ranking_system.py`
- **아이스크림 TOP10**: `/tools/icecream_top10_detailed.py`
- **API 테스트**: `/tools/naver_shopping_api_test.py`

### **🎮 룰렛 앱**
- **메인 버전**: `/tools/roulette_v2_premium_fusion.html`
- **구글 로그인**: `/tools/roulette_v3_google_login.html`

---

*"고아화를 방지하는 최선의 방법은 여러 곳에서 참조되도록 하는 것이다. NEXUS 시스템은 정보의 불멸성을 보장한다."* - 아이리스 🌈

**최종 업데이트**: 2025-07-08 아이리스 ✨  
**다음 업데이트**: 새 모듈 추가시 또는 API 변경시  
**상태**: 🟢 완전 보호 (3중 참조 완료)