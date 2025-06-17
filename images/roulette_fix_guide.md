# 룰렛 문제 해결 가이드

## 문제 진단
현재 룰렛은 **"접힌 부채를 펼쳐놓은 모양"**이 되어 있습니다.
- 중심점이 화면 아래에 있어서 반원형으로 배치되어야 하는데
- 실제로는 반원을 반으로 잘라서 일직선으로 늘어놓은 형태가 되었습니다.

## 해결 방법

### 1. CSS Transform 수정
```css
/* 현재 문제가 있는 방식 */
.roulette-section {
    transform-origin: center bottom; /* 이게 문제! */
    transform: rotate(각도);
}

/* 올바른 방식 */
.roulette-section {
    transform-origin: 50% 100%; /* 하단 중앙 기준 */
    transform: rotate(각도) translateY(-반지름);
}
```

### 2. 각도 계산 수정
```javascript
// 각 섹션의 올바른 각도 계산
const totalSections = 4; // 또는 섹션 개수
const anglePerSection = 180 / totalSections; // 반원이므로 180도

sections.forEach((section, index) => {
    const startAngle = index * anglePerSection - 90; // -90도부터 시작
    const endAngle = (index + 1) * anglePerSection - 90;
    
    section.style.transform = `
        rotate(${startAngle}deg) 
        skewY(${-anglePerSection}deg)
    `;
});
```

### 3. 위치 조정
```css
.roulette-container {
    position: relative;
    bottom: 0; /* 화면 하단에 고정 */
    left: 50%;
    transform: translateX(-50%);
    width: 400px;
    height: 200px; /* 반원이므로 높이는 절반 */
    overflow: hidden; /* 하단 부분 숨김 */
}
```

## 비유로 이해하기
현재 상황은 **"피자를 4조각으로 자른 후, 각 조각을 따로 떼어서 일렬로 늘어놓은 것"**과 같습니다.

올바른 방법은 **"부채를 펼치듯이 중심점에서 둥글게 퍼지게 하는 것"**입니다.

## 체크리스트
- [ ] Transform-origin을 하단 중앙으로 설정
- [ ] 각 섹션을 반원 형태로 배치
- [ ] 회전 애니메이션을 원형으로 수정
- [ ] 오버플로우 처리로 하단 부분 숨김
- [ ] 각도 계산을 180도 기준으로 수정

## 참고사항
- 반원 룰렛은 일반 원형 룰렛보다 복잡합니다
- CSS의 clip-path나 SVG를 사용하는 것도 고려해볼 수 있습니다
- 모바일에서의 터치 이벤트도 함께 테스트해보세요
