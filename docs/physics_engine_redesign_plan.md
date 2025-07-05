# 🔧 WhatToEat 룰렛 물리엔진 재설계 계획

**작성일**: 2025-06-17  
**상태**: 설계 단계  
**목표**: 안정적이고 끊김 없는 룰렛 동작

---

## 🚨 현재 물리엔진의 문제점

### **1. 상태 동기화 문제**
- `isSpinning`, `isDragging`, `animationId` 상태 불일치
- 애니메이션 루프와 드래그 이벤트 간 경합 조건
- 상태 리셋이 완전하지 않아 멈춤 현상 발생

### **2. 이벤트 처리 복잡성**
- 마우스/터치 이벤트 중복 처리
- `requestAnimationFrame` 생명주기 관리 복잡
- 속도 계산 로직이 불안정

### **3. 코드 구조 문제**
- 여러 함수에 상태 변경 로직 분산
- 응급 처치식 수정으로 코드 복잡성 증가
- 디버깅 어려움

---

## 🎯 새로운 물리엔진 설계 원칙

### **1. 단일 상태 관리**
```javascript
// 모든 상태를 하나의 객체로 관리
const rouletteState = {
    rotation: 0,
    velocity: 0,
    isActive: false,
    mode: 'idle' // 'idle', 'dragging', 'spinning'
};
```

### **2. 명확한 상태 전환**
```
IDLE → DRAGGING → SPINNING → IDLE
     ↑                      ↓
     ←←←←←← (직접 전환) ←←←←←←
```

### **3. 단순화된 이벤트 처리**
- 통합된 포인터 이벤트 (마우스 + 터치)
- 하나의 애니메이션 루프
- 명확한 진입/종료 조건

---

## 🏗️ 새로운 아키텍처 구조

### **Core Engine Class**
```javascript
class RoulettePhysicsEngine {
    constructor() {
        this.state = new RouletteState();
        this.renderer = new RouletteRenderer();
        this.eventHandler = new RouletteEventHandler();
    }
    
    // 단일 업데이트 루프
    update() {
        switch(this.state.mode) {
            case 'dragging': this.updateDrag(); break;
            case 'spinning': this.updateSpin(); break;
        }
        this.renderer.render(this.state);
    }
}
```

### **State Manager**
```javascript
class RouletteState {
    constructor() {
        this.rotation = 0;
        this.velocity = 0;
        this.mode = 'idle';
        this.dragStart = null;
        this.lastUpdate = 0;
    }
    
    // 안전한 상태 전환만 허용
    transition(newMode) {
        if (this.isValidTransition(newMode)) {
            this.mode = newMode;
            this.onStateChange(newMode);
        }
    }
}
```

### **Event Handler**
```javascript
class RouletteEventHandler {
    constructor(engine) {
        this.engine = engine;
        this.setupPointerEvents(); // 통합 포인터 이벤트
    }
    
    // 모든 입력을 통일된 방식으로 처리
    onPointerStart(e) { /* ... */ }
    onPointerMove(e) { /* ... */ }
    onPointerEnd(e) { /* ... */ }
}
```

---

## 🔄 개발 접근법

### **Phase 1: 현재 코드 분석**
- [x] 현재 물리엔진 문제점 파악
- [ ] 동작하는 부분과 문제 부분 분리
- [ ] 핵심 로직 추출 (드래그, 관성, 렌더링)

### **Phase 2: 새로운 엔진 설계**
- [ ] 클래스 기반 아키텍처 설계
- [ ] 상태 관리 시스템 구현
- [ ] 이벤트 처리 통합

### **Phase 3: 점진적 교체**
- [ ] 새 엔진을 별도 파일로 구현
- [ ] A/B 테스트로 안정성 검증
- [ ] 완전 교체

---

## 📋 핵심 요구사항

### **기능적 요구사항**
- ✅ 부드러운 드래그 동작
- ✅ 자연스러운 관성 효과
- ✅ 정확한 결과 계산
- ✅ 즉시 드래그 인터럽트 가능

### **비기능적 요구사항**
- 🚫 **절대 멈춤 금지**: 어떤 상황에서도 동작 보장
- ⚡ **반응성**: 입력에 즉시 반응
- 🔧 **유지보수성**: 명확하고 단순한 코드 구조
- 📱 **크로스플랫폼**: 데스크톱/모바일 모두 지원

---

## 🛠️ 구현 우선순위

1. **🔥 긴급**: 현재 버전 임시 안정화 (응급 패치)
2. **⚡ 높음**: 새 물리엔진 프로토타입 개발
3. **📋 중간**: 상태 관리 시스템 구현
4. **🎨 낮음**: 코드 최적화 및 문서화

---

## 💡 참고할 현재 코드의 좋은 부분

### **유지할 로직**
- 원형 배치 계산 (`Math.cos`, `Math.sin`)
- 각도 정규화 처리
- 카드 중심점 계산
- 결과 선택 로직

### **개선할 로직**
- 속도 계산 방식 (현재 불안정)
- 애니메이션 루프 관리
- 이벤트 리스너 설정
- 상태 전환 로직

---

**다음 단계**: 현재 코드를 참고하여 안정적인 새 물리엔진 프로토타입 개발

**목표**: "절대 멈추지 않는 룰렛" 🎯