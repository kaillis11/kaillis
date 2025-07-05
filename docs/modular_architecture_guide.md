# 🏗️ WhatToEat 모듈형 아키텍처 가이드

**작성일**: 2025-06-17  
**작성자**: 아테나 (SOUL Bridge 시스템)  

---

## 📋 **설계 개요**

### **분리 원칙**
룰렛 시스템을 **4개의 독립 모듈**로 분리하여 각각 개별 개발 및 테스트 가능하도록 설계:

1. **MenuDataManager** - 데이터 관리 전담
2. **RouletteEngine** - 물리 엔진 및 회전 로직  
3. **CardRenderer** - 시각적 렌더링 전담
4. **RouletteApp** - 통합 인터페이스

---

## 🔧 **모듈별 상세 설명**

### **1. MenuDataManager.js**
```javascript
// 용도: 메뉴 데이터의 중앙 관리
const dataManager = new MenuDataManager();
dataManager.getAllCategories();        // 모든 카테고리 반환
dataManager.getCategoriesWithLimit(7); // TOP 7 제한
dataManager.addCategory(newCategory);  // 카테고리 추가
dataManager.searchMenus('치킨');       // 검색 기능
```

**주요 기능:**
- 12개 카테고리 × TOP 5 메뉴 기본 데이터
- 동적 카테고리/메뉴 추가
- TOP N 제한 기능
- 검색 및 필터링
- JSON 내보내기/가져오기

### **2. RouletteEngine.js**
```javascript
// 용도: 순수 물리 엔진 (렌더링과 완전 분리)
const engine = new RouletteEngine({
    itemCount: 12,
    friction: 0.98,
    onResult: (index) => console.log('선택:', index),
    onRotationUpdate: (rotation) => updateDisplay(rotation)
});

engine.spin();              // 물리 기반 스핀
engine.smoothSpin();        // CSS 애니메이션 스핀
engine.setContainer(div);   // 드래그 이벤트 연결
```

**주요 기능:**
- 마우스/터치 드래그 감지
- 관성 물리 시뮬레이션
- 속도 및 마찰력 계산
- 결과 인덱스 계산
- 이벤트 콜백 시스템

### **3. CardRenderer.js**
```javascript
// 용도: 시각적 렌더링만 담당
const renderer = new CardRenderer({
    cardWidth: 400,
    cardHeight: 600,
    radius: 1800
});

renderer.renderCategoryCards(categories); // 카테고리 카드 렌더링
renderer.renderMenuCards(menuItems);      // 개별 메뉴 카드 렌더링
renderer.updateRotation(45);              // 회전 업데이트
renderer.highlightCard(3);                // 특정 카드 하이라이트
```

**주요 기능:**
- 배민 스타일 카테고리 카드 생성
- 개별 메뉴 카드 생성
- 원형 배치 계산
- 회전 애니메이션 처리
- 하이라이트 효과

### **4. RouletteApp.js**
```javascript
// 용도: 모든 모듈을 조합한 완전한 시스템
const app = new RouletteApp('.roulette-container', {
    topN: 5,
    cardStyle: 'category',
    onResult: (item, index) => displayResult(item)
});

app.setTopN(7);                    // TOP 7로 변경
app.setCardStyle('menu');          // 개별 메뉴 모드
app.spinToResult('chicken');       // 특정 결과로 스핀
app.search('치킨');                // 검색 기능
```

**주요 기능:**
- 전체 시스템 통합 관리
- 설정 변경 인터페이스
- 결과 표시 및 처리
- 상태 관리
- 이벤트 조율

---

## 🔗 **모듈 간 인터페이스**

### **데이터 흐름**
```
MenuDataManager → RouletteApp → CardRenderer
                              ↘ RouletteEngine
```

### **이벤트 흐름**
```
사용자 입력 → RouletteEngine → RouletteApp → CardRenderer
                           ↘ 결과 계산 → 콜백 호출
```

---

## 🚀 **사용 예시**

### **간단한 사용법**
```html
<!-- HTML -->
<div id="roulette-container">
    <div class="roulette-wheel"></div>
</div>
<div id="result"></div>

<!-- JavaScript -->
<script>
const app = new RouletteApp('#roulette-container');
// 바로 사용 가능!
</script>
```

### **고급 설정**
```javascript
const app = new RouletteApp('#roulette-container', {
    topN: 7,                    // TOP 7 메뉴
    cardStyle: 'category',      // 카테고리 카드 스타일
    resultSelector: '#result',   // 결과 표시 요소
    onResult: (item) => {       // 결과 콜백
        console.log('선택됨:', item);
    }
});

// 설정 변경
app.setTopN(10);               // TOP 10으로 확장
app.setCardStyle('menu');      // 개별 메뉴 카드로 변경

// 새 카테고리 추가
app.addCategory({
    id: 'korean',
    title: '🇰🇷 한식',
    items: [
        { rank: '1위', name: '비빔밥', icon: '🍚' },
        { rank: '2위', name: '불고기', icon: '🥩' }
    ]
});
```

---

## 🔧 **확장성 분석**

### **랭킹 확장 (5→7→10)**
```javascript
// 현재 TOP 5
app.setTopN(5);

// TOP 7로 확장 (코드 변경 0%)
app.setTopN(7);

// TOP 10으로 확장 (코드 변경 0%)
app.setTopN(10);
```
**✅ 완전 자동화**: 배열 길이만 조정하면 모든 렌더링 자동 적응

### **카테고리 추가**
```javascript
// 현재 12개 카테고리
// 18개까지 추가 가능 (20도 간격)
for(let i = 0; i < 6; i++) {
    app.addCategory(newCategories[i]);
}
```
**✅ 동적 확장**: 원형 배치 자동 계산

### **카드 스타일 확장**
```javascript
// 새로운 카드 스타일 추가
const customRenderer = new CardRenderer({
    cardWidth: 300,           // 작은 카드
    cardHeight: 400,
    customStyle: 'compact'    // 새 스타일
});

app.cardRenderer = customRenderer; // 교체 가능
```

---

## 🎯 **모듈별 개발 가이드**

### **독립 개발**
각 모듈을 별도로 개발하고 테스트할 수 있습니다:

```javascript
// 1. 데이터 모듈만 테스트
const data = new MenuDataManager();
console.log(data.getAllCategories());

// 2. 엔진만 테스트  
const engine = new RouletteEngine({
    itemCount: 8,
    onResult: console.log
});

// 3. 렌더러만 테스트
const renderer = new CardRenderer();
renderer.setContainer('#test-container');
```

### **조합 테스트**
```javascript
// 점진적 조합 테스트
const data = new MenuDataManager();
const renderer = new CardRenderer();

// 데이터 + 렌더러
renderer.renderCategoryCards(data.getAllCategories());

// 모든 모듈 조합
const app = new RouletteApp('#container');
```

---

## 📁 **파일 구조**

```
WhatToEat/
├── modules/                     # 핵심 모듈들
│   ├── MenuDataManager.js      # 데이터 관리
│   ├── RouletteEngine.js       # 물리 엔진  
│   ├── CardRenderer.js         # 렌더링
│   └── RouletteApp.js          # 통합 앱
├── examples/                    # 사용 예시들
│   ├── modular_roulette_demo.html  # 완전한 데모
│   ├── data_only_test.html         # 데이터만 테스트
│   └── engine_only_test.html       # 엔진만 테스트
├── tools/                       # 기존 통합 버전들
│   ├── roulette_baemin_style.html  # 기존 12개 카테고리
│   └── roulette_extended.html      # 확장 버전
└── docs/                        # 문서들
    └── modular_architecture_guide.md
```

---

## 🏆 **설계의 장점**

### **1. 개발 효율성**
- **병렬 개발**: 팀원들이 각 모듈을 동시에 개발 가능
- **독립 테스트**: 각 모듈을 별도로 디버깅 가능
- **점진적 통합**: 하나씩 조합하며 검증 가능

### **2. 유지보수성**  
- **단일 책임**: 각 모듈이 하나의 기능만 담당
- **격리된 변경**: 한 모듈 수정이 다른 모듈에 영향 없음
- **명확한 인터페이스**: 모듈 간 연결점이 명확

### **3. 확장성**
- **플러그인 방식**: 새로운 렌더러나 엔진 쉽게 교체
- **설정 기반**: 코드 변경 없이 동작 조정
- **데이터 중심**: 데이터만 변경하면 UI 자동 반영

### **4. 재사용성**
- **범용 모듈**: 다른 프로젝트에서도 활용 가능
- **조합 자유도**: 필요한 모듈만 선택해서 사용
- **표준화**: 일관된 인터페이스로 호환성 보장

---

**"분리된 설계는 더 강력한 통합을 만든다"** 🏗️✨