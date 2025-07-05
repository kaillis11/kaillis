// 물리엔진 상수
export const PHYSICS = {
  FRICTION: 0.985,
  MIN_VELOCITY: 0.05,
  PERPETUAL_VELOCITY: 0.02,  // 계속 유지할 최소 속도
  MAX_VELOCITY: 25,
  DRAG_MULTIPLIER: 0.8,
  RADIUS: 265, // React Native에서는 더 작은 크기 사용
  CARD_WIDTH: 64,
  CARD_HEIGHT: 90
};

// 룰렛 상태 관리 클래스
export class RouletteState {
  constructor() {
    this.reset();
  }

  reset() {
    this.mode = 'idle';           // 'idle', 'dragging', 'spinning'
    this.rotation = 0;            // 현재 회전각도
    this.velocity = 0;            // 현재 속도
    this.lastAngle = 0;           // 마지막 드래그 각도
    this.dragHistory = [];        // 드래그 속도 히스토리
    this.lastUpdate = Date.now();
  }

  transition(newMode) {
    const validTransitions = {
      'idle': ['dragging', 'spinning'],
      'dragging': ['idle', 'spinning'],
      'spinning': ['idle', 'dragging']
    };

    if (validTransitions[this.mode].includes(newMode)) {
      console.log(`State: ${this.mode} → ${newMode}`);
      this.mode = newMode;
      return true;
    }
    return false;
  }

  // NaN 방어 시스템
  safeUpdate(deltaTime) {
    if (!Number.isFinite(deltaTime) || deltaTime <= 0) {
      return;
    }

    if (!Number.isFinite(this.velocity)) {
      this.velocity = PHYSICS.PERPETUAL_VELOCITY;
    }

    if (!Number.isFinite(this.rotation)) {
      this.rotation = 0;
    }

    this.lastUpdate = Date.now();
  }
}

// 물리 계산 유틸리티
export const PhysicsUtils = {
  // 각도 정규화 (-180 ~ 180)
  normalizeAngle(angle) {
    if (!Number.isFinite(angle)) return 0;
    while (angle > 180) angle -= 360;
    while (angle < -180) angle += 360;
    return angle;
  },

  // 각도 차이 계산
  angleDifference(angle1, angle2) {
    let diff = angle2 - angle1;
    return this.normalizeAngle(diff);
  },

  // 안전한 속도 제한
  clampVelocity(velocity) {
    if (!Number.isFinite(velocity)) return PHYSICS.PERPETUAL_VELOCITY;
    return Math.max(
      Math.min(velocity, PHYSICS.MAX_VELOCITY),
      -PHYSICS.MAX_VELOCITY
    );
  },

  // 무한회전을 위한 최소 속도 보장
  ensurePerpetualMotion(velocity) {
    if (Math.abs(velocity) < PHYSICS.PERPETUAL_VELOCITY) {
      return velocity >= 0 ? PHYSICS.PERPETUAL_VELOCITY : -PHYSICS.PERPETUAL_VELOCITY;
    }
    return velocity;
  },

  // 좌표를 각도로 변환
  coordsToAngle(x, y, centerX, centerY) {
    const dx = x - centerX;
    const dy = y - centerY;
    return Math.atan2(dy, dx) * (180 / Math.PI);
  },

  // 드래그 속도 계산
  calculateDragVelocity(dragHistory, timeWindow = 100) {
    if (dragHistory.length < 2) return 0;

    const now = Date.now();
    const recentHistory = dragHistory.filter(h => now - h.time < timeWindow);
    
    if (recentHistory.length < 2) return 0;

    const first = recentHistory[0];
    const last = recentHistory[recentHistory.length - 1];
    const timeDiff = last.time - first.time;
    
    if (timeDiff === 0) return 0;

    const angleDiff = this.angleDifference(first.angle, last.angle);
    return (angleDiff / timeDiff) * 16.67; // 60fps 기준으로 변환
  }
};

// 룰렛 물리 엔진 클래스
export class RoulettePhysicsEngine {
  constructor() {
    this.state = new RouletteState();
    this.isRunning = false;
    this.animationId = null;
  }

  start() {
    if (this.isRunning) return;
    this.isRunning = true;
    this.update();
  }

  stop() {
    this.isRunning = false;
    if (this.animationId) {
      cancelAnimationFrame(this.animationId);
      this.animationId = null;
    }
  }

  update() {
    if (!this.isRunning) return;

    const now = Date.now();
    const deltaTime = now - this.state.lastUpdate;
    
    this.state.safeUpdate(deltaTime);

    if (this.state.mode === 'spinning') {
      this.updatePhysics(deltaTime);
    }

    this.animationId = requestAnimationFrame(() => this.update());
  }

  updatePhysics(deltaTime) {
    if (!Number.isFinite(deltaTime) || deltaTime <= 0) return;

    // 마찰력 적용
    this.state.velocity *= PHYSICS.FRICTION;

    // 속도 제한
    this.state.velocity = PhysicsUtils.clampVelocity(this.state.velocity);

    // 무한회전 보장
    this.state.velocity = PhysicsUtils.ensurePerpetualMotion(this.state.velocity);

    // 회전 업데이트
    this.state.rotation += this.state.velocity;
    this.state.rotation = PhysicsUtils.normalizeAngle(this.state.rotation);
  }

  // 드래그 시작
  startDrag(x, y, centerX, centerY) {
    this.state.transition('dragging');
    this.state.lastAngle = PhysicsUtils.coordsToAngle(x, y, centerX, centerY);
    this.state.dragHistory = [];
  }

  // 드래그 업데이트
  updateDrag(x, y, centerX, centerY) {
    if (this.state.mode !== 'dragging') return;

    const currentAngle = PhysicsUtils.coordsToAngle(x, y, centerX, centerY);
    const angleDelta = PhysicsUtils.angleDifference(this.state.lastAngle, currentAngle);
    
    this.state.rotation += angleDelta;
    this.state.lastAngle = currentAngle;

    // 드래그 히스토리 기록
    this.state.dragHistory.push({
      angle: currentAngle,
      time: Date.now()
    });

    // 히스토리 크기 제한
    if (this.state.dragHistory.length > 10) {
      this.state.dragHistory.shift();
    }
  }

  // 드래그 종료
  endDrag() {
    if (this.state.mode !== 'dragging') return;

    // 드래그 속도 계산
    const dragVelocity = PhysicsUtils.calculateDragVelocity(this.state.dragHistory);
    this.state.velocity = dragVelocity * PHYSICS.DRAG_MULTIPLIER;

    this.state.transition('spinning');
  }

  // 버튼 스핀
  spin() {
    const randomVelocity = (Math.random() - 0.5) * PHYSICS.MAX_VELOCITY;
    this.state.velocity = randomVelocity;
    this.state.transition('spinning');
  }

  // 현재 상태 반환
  getState() {
    return {
      rotation: this.state.rotation,
      velocity: this.state.velocity,
      mode: this.state.mode
    };
  }
}