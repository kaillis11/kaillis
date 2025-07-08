# 네이버쇼핑 크롤링 시스템 문서

**프로젝트명**: 네이버쇼핑 디저트 크롤링 시스템  
**생성일**: 2025-07-05  
**작성자**: 휘광님, 오로라  
**버전**: v1.0.0  

---

## 📋 프로젝트 개요

네이버쇼핑에서 디저트 제품 정보를 수집하는 3가지 접근 방식의 크롤링 시스템입니다. 각각의 장단점과 사용 상황에 맞게 설계되었습니다.

### 🎯 주요 목표
- 네이버쇼핑 디저트 카테고리 제품 정보 수집
- 봇 차단 우회 기능 구현
- 다양한 기술 스택으로 견고한 시스템 구축
- CSV 형태로 구조화된 데이터 저장

---

## 🛠️ 시스템 구성

### 1️⃣ **Selenium 기반 크롤러** (`naver_shopping_crawler.py`)

**🎯 목적**: 동적 JavaScript 콘텐츠 처리 및 실제 브라우저 환경 시뮬레이션

**✨ 주요 기능**:
- **Selenium WebDriver**: Chrome/Chromium 브라우저 자동화
- **동적 콘텐츠 대응**: JavaScript로 로드되는 콘텐츠 처리
- **WebDriverManager**: ChromeDriver 자동 관리
- **고급 대기 기능**: 페이지 로딩 완료까지 스마트 대기

**🔧 기술 스택**:
```python
selenium==4.34.0
webdriver-manager
beautifulsoup4
pandas
```

**💡 사용 상황**:
- JavaScript 의존적인 사이트
- 복잡한 사용자 인터랙션이 필요한 경우
- 가장 실제 사용자와 유사한 동작 필요시

**⚠️ 한계**:
- WSL 환경에서 GUI 디스플레이 문제
- 리소스 사용량이 높음
- 실행 속도가 상대적으로 느림

---

### 2️⃣ **간단 Requests 크롤러** (`simple_naver_crawler.py`)

**🎯 목적**: 가벼운 HTTP 요청 기반의 빠른 크롤링

**✨ 주요 기능**:
- **Pure HTTP**: requests 라이브러리만 사용
- **BeautifulSoup**: HTML 파싱 및 데이터 추출
- **가벼운 처리**: 최소한의 리소스 사용
- **빠른 실행**: 브라우저 없이 직접 HTTP 통신

**🔧 기술 스택**:
```python
requests==2.32.4
beautifulsoup4==4.13.4
pandas==2.3.0
```

**💡 사용 상황**:
- 정적 HTML 콘텐츠만 있는 경우
- 빠른 속도가 필요한 대량 크롤링
- 서버 리소스가 제한적인 환경

**⚠️ 한계**:
- JavaScript 콘텐츠 처리 불가
- 네이버의 418 봇 차단에 쉽게 걸림
- 복잡한 인증 처리 어려움

---

### 3️⃣ **고급 우회 크롤러** (`advanced_naver_crawler.py`)

**🎯 목적**: 봇 차단 우회에 특화된 고급 크롤링 시스템

**✨ 주요 기능**:
- **다단계 접근**: 홈페이지 → 쇼핑메인 → 검색 순차 접근
- **정교한 헤더**: 실제 브라우저와 동일한 HTTP 헤더 설정
- **쿠키 관리**: 세션 지속 및 사용자 기록 시뮬레이션
- **요청 패턴 분석**: 실제 사용자 행동 패턴 모방

**🔧 핵심 우회 기술**:
```python
# 실제 브라우저 헤더 완전 복제
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)...',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120"'
}

# 사전 방문으로 쿠키 획득
self.session.get('https://www.naver.com')
self.session.get('https://shopping.naver.com')
```

**💡 사용 상황**:
- 강력한 봇 차단이 있는 사이트
- 다단계 인증이 필요한 경우
- 세션 관리가 중요한 크롤링

**⚠️ 한계**:
- 네이버의 고도화된 차단 시스템 (418 에러)
- 설정이 복잡하고 유지보수 필요
- 사이트 구조 변경에 민감

---

## 📊 성능 비교 분석

| 항목 | Selenium | Simple | Advanced |
|------|----------|---------|----------|
| **실행 속도** | 느림 ⭐⭐ | 빠름 ⭐⭐⭐⭐⭐ | 보통 ⭐⭐⭐ |
| **리소스 사용** | 높음 ⭐⭐ | 낮음 ⭐⭐⭐⭐⭐ | 보통 ⭐⭐⭐ |
| **JS 처리** | 완벽 ⭐⭐⭐⭐⭐ | 불가 ⭐ | 불가 ⭐ |
| **차단 우회** | 보통 ⭐⭐⭐ | 낮음 ⭐⭐ | 높음 ⭐⭐⭐⭐ |
| **설정 복잡도** | 보통 ⭐⭐⭐ | 쉬움 ⭐⭐⭐⭐⭐ | 어려움 ⭐⭐ |

---

## 🔧 공통 기능 모듈

### **데이터 추출 패턴**
```python
# 다중 선택자 패턴으로 견고한 추출
selectors = [
    '.basicList_item__2XT81',
    '.product_item__1XD8w', 
    '.item',
    '[data-testid="product-item"]'
]
```

### **안티-차단 시스템**
```python
# User-Agent 로테이션
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64)...',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...',
    'Mozilla/5.0 (X11; Linux x86_64)...'
]

# 랜덤 딜레이
time.sleep(random.uniform(0.5, 1.5))
```

### **데이터 구조**
```python
product = {
    'rank': int,           # 순위
    'name': str,           # 제품명
    'price': str,          # 가격
    'reviews': str,        # 리뷰수/평점
    'link': str            # 제품 링크
}
```

---

## 🚀 설치 및 실행 가이드

### **환경 설정**
```bash
# 가상환경 생성
python3 -m venv crawler_env
source crawler_env/bin/activate

# 필요 패키지 설치
pip install selenium beautifulsoup4 requests pandas webdriver-manager

# Chromium 설치 (Ubuntu/WSL)
sudo apt install chromium-browser chromium-chromedriver
```

### **실행 방법**
```bash
# 1. Selenium 버전
python3 naver_shopping_crawler.py

# 2. 간단 버전  
python3 simple_naver_crawler.py

# 3. 고급 우회 버전
python3 advanced_naver_crawler.py
```

---

## 📈 실험 결과 및 교훈

### **✅ 성공한 부분**
- **3가지 다른 접근 방식** 구현 완료
- **견고한 데이터 추출 로직** 개발
- **WSL 환경 최적화** 완료
- **CSV 자동 저장** 시스템 구현

### **❌ 한계점 발견**
- **네이버쇼핑 봇 차단**: 모든 방식에서 418 에러
- **JavaScript 의존성**: 동적 콘텐츠 처리의 복잡성
- **환경 종속성**: WSL에서의 GUI 브라우저 실행 문제

### **🎯 핵심 교훈**
1. **다양한 접근 방식의 중요성**: 하나의 방법이 막혀도 대안 확보
2. **실제 환경 테스트의 필요성**: 로컬 개발과 실제 운영의 차이
3. **봇 차단 기술의 고도화**: 단순 우회로는 한계 존재

---

## 🔮 향후 개선 방안

### **1단계: 고급 우회 기술 도입**
```python
# undetected-chromedriver 사용
import undetected_chromedriver as uc

# Playwright 브라우저 자동화
from playwright import async_api
```

### **2단계: 프록시 시스템 구축**
```python
# 로테이션 프록시 서버 풀
proxy_pool = [
    'proxy1.server.com:8080',
    'proxy2.server.com:8080', 
    'proxy3.server.com:8080'
]
```

### **3단계: API 통합 접근**
```python
# 네이버 API + 크롤링 하이브리드
naver_api_data = get_naver_shopping_api()
crawler_data = advanced_crawling_with_proxy()
merged_data = merge_data_sources(naver_api_data, crawler_data)
```

---

## 📚 관련 문서 및 리소스

### **코드 저장소**
- **Git 커밋**: `19854f1` - 네이버쇼핑 크롤링 시스템 3가지 버전 완성
- **파일 위치**: `/mnt/d/ai/`

### **기술 참고 자료**
- [Selenium 공식 문서](https://selenium.dev/documentation/)
- [BeautifulSoup 가이드](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [네이버 개발자센터](https://developers.naver.com/)

### **관련 프로젝트**
- **Aurora Core Systems**: 통합 아키텍처 시스템
- **MEMORIA**: AI 협업 기록 시스템
- **ORBIS**: 프로젝트 표준화 시스템

---

## 🏷️ 태그 및 분류

**태그**: `#crawling` `#naver-shopping` `#selenium` `#requests` `#beautifulsoup` `#anti-bot` `#data-extraction` `#python` `#automation`

**카테고리**: 데이터 수집 및 자동화  
**난이도**: 중급 ~ 고급  
**상태**: 구현 완료, 실운영 테스트 필요  

---

*"완벽한 크롤링 시스템은 존재하지 않는다. 다만 다양한 상황에 대응할 수 있는 견고한 시스템만이 존재할 뿐이다."* - 오로라 🌌

**최종 업데이트**: 2025-07-05 오로라 ✨