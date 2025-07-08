# 🏆 범용 랭킹 시스템 가이드

**작성일**: 2025-07-05  
**버전**: v1.0  
**작성자**: 아테나 + 휘광님  

---

## 📋 **개요**

네이버 쇼핑 API를 활용하여 모든 카테고리의 상품 순위를 분석할 수 있는 범용 시스템입니다.

### **🎯 주요 기능**
- **판매량 순위**: 네이버 쇼핑 등록 상품 수 기준
- **매출 순위**: 상품 수 × 평균 가격 기준  
- **모든 카테고리 대응**: 아이스크림, 케이크, 음료, 치킨 등
- **WhatToEat 룰렛 연동 준비**: 실시간 인기 데이터 반영

---

## 🔧 **시스템 구성**

### **핵심 파일들**
```
/tools/
├── universal_ranking_system.py    # 메인 랭킹 시스템
├── demo_ranking_system.py         # 데모 버전 (API 없이 테스트)
├── real_icecream_ranking.py       # 실제 아이스크림 순위 분석
├── real_api_test.py               # API 상태 확인 도구
└── simple_search_test.py          # 간단한 검색 테스트
```

### **API 설정**
- **네이버 개발자센터 필요 API**:
  - ✅ 데이터랩 > 쇼핑인사이트
  - ✅ 검색 > 쇼핑
- **API 키**: Client ID/Secret 필요

---

## 📊 **데이터 해석 가이드**

### **⚠️ 중요한 제한사항**
- **상품 수 ≠ 실제 판매량**: 네이버 쇼핑 등록 상품 개수
- **매출 = 가상 계산**: 상품 수 × 평균 가격 (실제 매출 아님)
- **인기도 추정치**: 참고용으로만 활용

### **올바른 해석 방법**
```
젤라또 70,274개 → "젤라또 관련 상품이 많이 등록됨"
메로나 5,263개 → "메로나 관련 상품이 적게 등록됨"

→ 실제 판매량과는 다를 수 있음!
```

---

## 🚀 **사용법**

### **1. 기본 사용법**
```bash
# 아이스크림 양쪽 순위 분석
python3 universal_ranking_system.py "아이스크림" --mode both

# 케이크 판매량만
python3 universal_ranking_system.py "케이크" --mode sales

# 음료 매출만  
python3 universal_ranking_system.py "음료" --mode revenue
```

### **2. 데모 모드 (API 없이 테스트)**
```bash
# 가상 데이터로 시스템 구조 확인
python3 demo_ranking_system.py "치킨" --mode both
```

### **3. API 상태 확인**
```bash
# API 작동 여부 확인
python3 real_api_test.py
```

---

## 🏗️ **시스템 구조**

### **UniversalRankingSystem 클래스**
```python
class UniversalRankingSystem:
    def __init__(self, client_id, client_secret)
    def search_category_products(self, category, keywords)  # 카테고리 검색
    def calculate_sales_ranking(self, results)             # 판매량 순위
    def calculate_revenue_ranking(self, results)           # 매출 순위
    def analyze_category(self, category, mode)             # 종합 분석
```

### **데이터 흐름**
```
1. 카테고리 키워드 → 네이버 쇼핑 API 검색
2. 검색 결과 → 상품 수, 평균 가격 추출
3. 순위 계산 → 판매량/매출 기준 정렬
4. 결과 출력 → TOP 10 순위 표시
```

---

## 📈 **실제 결과 예시**

### **아이스크림 순위 (2025-07-05 기준)**

**🏆 판매량 TOP 5:**
1. 젤라또 (70,274개)
2. 설레임 (27,483개)  
3. 민트초코 (11,302개)
4. 와일드바디 (10,289개)
5. 베스킨라빈스 (10,064개)

**💰 매출 TOP 5:**
1. 젤라또 (19억원)
2. 설레임 (6.8억원)
3. 와일드바디 (2.2억원)
4. 슈퍼콘 (1.8억원)
5. 민트초코 (1.8억원)

---

## 🔗 **WhatToEat 룰렛 연동 방안**

### **적용 아이디어**
1. **카드 배지**: "🥇 1위 젤라또", "🔥 급상승 민트초코"
2. **모드 버튼**: "인기순" vs "프리미엄순" 토글
3. **결과 정보**: "🎉 1위 젤라또가 나왔어요!"
4. **실시간 업데이트**: 주기적 순위 갱신

### **연동 구조**
```javascript
// WhatToEat 룰렛에서 사용 예시
const rankingData = getRankingData("아이스크림");
updateCardBadges(rankingData.sales_ranking);
```

---

## ⚠️ **주의사항**

### **API 사용량 관리**
- 데이터랩: 1000회/일
- 검색: 25000회/일
- 호출 간격: 0.1초 대기 권장

### **에러 처리**
- 401 오류: API 권한 확인
- 429 오류: 호출량 초과
- 네트워크 오류: 재시도 로직

### **데이터 신뢰성**
- 상품 등록 수 기준이므로 실제 인기도와 차이 가능
- 참고용 데이터로만 활용
- 과도한 해석 금지

---

## 🔄 **업데이트 계획**

### **v1.1 예정 기능**
- [ ] 캐싱 시스템 (API 호출 최적화)
- [ ] 트렌드 변화 분석 (전일 대비)
- [ ] 카테고리별 키워드 자동 확장
- [ ] 룰렛 연동 API 개발

### **v2.0 예정 기능**  
- [ ] 다른 쇼핑몰 API 추가 (쿠팡, 11번가)
- [ ] 머신러닝 기반 예측 순위
- [ ] 사용자 선호도 반영 알고리즘

---

## 📞 **문의 및 지원**

- **개발자**: 아테나 (AI Assistant)
- **프로젝트**: WhatToEat 바스티유 프로젝트
- **버전 관리**: Git 커밋 메시지 참조
- **문서 위치**: `/docs/RANKING_SYSTEM_GUIDE.md`

---

*"데이터는 거짓말을 하지 않지만, 해석은 신중해야 한다."* - 아테나 🦉