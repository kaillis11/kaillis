# 🗺️ WhatToEat 코드 맵

**최종 업데이트**: 2025-06-17 16:43:28 KST

---

## 📁 프로젝트 구조

```
WhatToEat/
├── PROJECT_HUB.md           # 프로젝트 중앙 허브
├── GATEWAY.md               # 네비게이션 시스템
├── INSTRUCTIONS.md          # 사용 가이드
├── ROADMAP.md              # 개발 계획
├── WORKLOG.md              # 작업 일지
├── CODE_MAP.md             # 이 파일
├── VERSION_LOG.md          # 버전 기록
├── ideas/                  # 🌱 아이디어와 구상
│   └── GATEWAY.md          
├── docs/                   # 📚 공식 문서
│   └── GATEWAY.md          
├── tools/                  # 🔧 스크립트와 도구
├── examples/               # 📖 사용 사례
└── [프로젝트별 추가 폴더들]
```

---

## 🧩 핵심 구성 요소

### **아이디어 레이어** (`ideas/`)
- **목적**: 창의적 아이디어와 미래 비전
- **특징**: 자유로운 형식, 실험적 내용
- **파일들**: [주요 아이디어 파일들]

### **문서 레이어** (`docs/`)
- **목적**: 확정된 기술 문서와 명세
- **특징**: 체계적 구조, 공식적 톤
- **파일들**: [주요 문서 파일들]

### **실행 레이어** (`tools/`)
- **목적**: 실제 구현과 자동화
- **특징**: 실행 가능한 스크립트들
- **파일들**: 
  - **네이버 API 시스템**: `naver_shopping_api_test.py`, `test_datalab_api.py`, `universal_ranking_system.py`
  - **크롤링 시스템**: `naver_shopping_crawler.py`, `simple_naver_crawler.py`, `advanced_naver_crawler.py`
  - **분석 도구**: `icecream_top10_detailed.py`, `icecream_bestseller_analysis.py`, `demo_ranking_system.py`
  - **룰렛 엔진**: `roulette_v2_premium_fusion.html`, `roulette_v3_google_login.html`

---

## 🔄 데이터 흐름

```
사용자 입력 → [처리 과정] → 결과 출력
```

[구체적인 데이터 흐름 설명]

---

## 🔗 모듈 의존성

### **내부 의존성**
- [모듈 A] ← [모듈 B]
- [모듈 C] ← [모듈 D]

### **외부 의존성**
- **requests**: 네이버 API 호출 및 HTTP 통신
- **selenium**: 동적 웹 크롤링 (JavaScript 처리)
- **beautifulsoup4**: HTML 파싱 및 데이터 추출
- **pandas**: 데이터 분석 및 CSV 저장
- **webdriver-manager**: Chrome 드라이버 자동 관리

---

## 📍 주요 진입점

### **메인 스크립트**
- `tools/roulette_v2_premium_fusion.html` - 메인 룰렛 앱 (구글 로그인 이전 버전)
- `tools/roulette_v3_google_login.html` - 구글 로그인 통합 버전
- `tools/universal_ranking_system.py` - 범용 랭킹 분석 도구

### **API 엔드포인트**
- **네이버 쇼핑 API**: `https://openapi.naver.com/v1/search/shop.json`
- **네이버 데이터랩 API**: `https://openapi.naver.com/v1/datalab/shopping/categories`
- **API 키**: `UP8PqJq_FpkcB63sEFH9` (테스트용)

---

## 🎯 확장 지점

### **플러그인 시스템**
[확장 가능한 부분 설명]

### **설정 옵션**
[커스터마이징 가능한 부분]

---

*"좋은 지도는 길을 잃지 않게 하고, 새로운 길을 발견하게 한다."* 🧭
