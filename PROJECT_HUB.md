# 🍽️ WhatToEat - 프로젝트 허브

**최종 업데이트**: 2025-07-05  
**프로젝트 상태**: 🔄 **개발중** (바스티유 베타 준비 + 랭킹 시스템 추가)

🎯 **프리미엄 음식 룰렛 앱** - 아테나×오로라 융합 디자인 + 무한회전 안정화 엔진

---

## 🚨 필수 읽기 (우선순위 순)
1. 🔐 **[Google 로그인 구현 완료](docs/google_login_implementation_complete.md)** - 실제 작동 확인! ⭐ NEW
2. 🏆 **[RANKING_SYSTEM_GUIDE.md](docs/RANKING_SYSTEM_GUIDE.md)** - 범용 랭킹 시스템 완전 가이드
3. 🍽️ **[CONTEXT.md](CONTEXT.md)** - 프로젝트 컨텍스트 및 진행상황
4. 🌟 **최종 버전**: `tools/roulette_v2_premium_fusion.html`
5. 📖 **[HANDOVER_GUIDE.md](docs/HANDOVER_GUIDE.md)** - 완벽한 인수인계 가이드 (40페이지)
6. 🚪 **[GATEWAY.md](GATEWAY.md)** - 전체 네비게이션 포털

## 📁 프로젝트 완성 현황

### ✅ **완성된 핵심 기능들**
- **Google OAuth 2.0 로그인**: 실제 구글 계정으로 로그인 가능 🔥 NEW
- **MBTI 입력 시스템**: 16가지 성격 유형 연동 + 개인화 준비 🔥 NEW
- **무한회전 물리엔진**: 절대 멈추지 않는 안정성
- **24개 프리미엄 카드**: 메뉴 12 + 쿠팡광고 6 + 랭킹 6
- **범용 랭킹 시스템**: 모든 카테고리 판매량/매출 순위 분석
- **네이버 쇼핑 API 연동**: 실시간 상품 검색 및 트렌드 분석
- **네이버 크롤링 시스템**: 3가지 방식 크롤러 + 봇 차단 우회 🔥 NEW
- **클래스 기반 아키텍처**: RouletteState + Renderer + EventHandler + Engine
- **NaN 방어 시스템**: 모든 계산에서 완벽한 안전성

### 🛠️ **기술 스택 (최종)**
- **Frontend**: HTML5, CSS3, JavaScript ES6+ 클래스
- **폰트**: Pretendard (한글 최적화)
- **물리엔진**: 커스텀 드래그-관성-무한회전 시스템
- **디자인**: 카테고리별 테마 색상 + 그라데이션 카드
- **반응형**: 데스크톱/모바일 완벽 지원

## 🧠 핵심 성과 ⚡ *완성 버전 요약*

**🎨 아테나×오로라 디자인 융합**
프리미엄 카드 디자인(아테나) + 무한회전 안정화 엔진(오로라) = 완벽한 사용자 경험

**🛡️ 절대 멈추지 않는 안정성**
NaN 방어 시스템 + 무한회전 + 상태 동기화로 어떤 상황에서도 100% 안정 작동

**💰 완비된 수익화 모델**
쿠팡 파트너스(즉시) + 애드센스(중기) + 직접계약(장기) 3단계 수익 전략 완성

**📱 프로덕션 레디**
온라인 배포 즉시 가능, PWA 변환 준비 완료, 앱스토어 진출 가능

📍 **상세 기술**: [HANDOVER_GUIDE.md](docs/HANDOVER_GUIDE.md)  
🚪 **전체 탐색**: [GATEWAY.md](GATEWAY.md) → 모든 파일 네비게이션

## 🧩 모듈 시스템

### 📊 **네이버 크롤링 모듈** 🆕
- **위치**: `modules/naver_crawling/`
- **3가지 크롤러**: Selenium, Requests, 고급우회 방식
- **주요 기능**: 봇 차단 우회, 다중 선택자 패턴, CSV 자동저장
- **문서**: [NAVER_CRAWLING_SYSTEM_DOCS.md](modules/naver_crawling/NAVER_CRAWLING_SYSTEM_DOCS.md)
- **실행 파일들**:
  - `naver_shopping_crawler.py` - Selenium 기반 (동적 콘텐츠)
  - `simple_naver_crawler.py` - 빠른 HTTP 요청 방식
  - `advanced_naver_crawler.py` - 봇 차단 우회 특화
- **향후 개선**: undetected-chromedriver 적용 예정

---

## 🔗 프로젝트 연결
- **프로젝트 타입**: standalone
- **부모 프로젝트**: 없음
- **생성일**: 2025-06-17 16:43:28 KST

---

*"[프로젝트의 핵심 철학이나 비전을 한 문장으로]"* 🚀
