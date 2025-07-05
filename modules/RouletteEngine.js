/**
 * 룰렛 엔진 모듈
 * - 회전 물리 엔진 전담
 * - 드래그 인터랙션 처리
 * - 결과 계산 로직
 * - 렌더링과 완전 분리된 순수 로직
 */

class RouletteEngine {
    constructor(options = {}) {
        // 기본 설정
        this.config = {
            itemCount: 12,
            friction: 0.98,
            minVelocity: 0.1,
            maxVelocity: 20,
            container: null,
            onResult: null,
            onRotationUpdate: null,
            ...options
        };

        // 물리 상태
        this.currentRotation = 0;
        this.velocity = 0;
        this.isSpinning = false;
        this.isDragging = false;
        this.lastAngle = 0;
        this.velocityHistory = [];
        this.animationId = null;

        // 이벤트 리스너 바인딩
        this.boundEvents = {
            startDrag: this.startDrag.bind(this),
            drag: this.drag.bind(this),
            endDrag: this.endDrag.bind(this)
        };

        this.init();
    }

    /**
     * 엔진 초기화
     */
    init() {
        if (this.config.container) {
            this.setupEvents();
        }
    }

    /**
     * 아이템 개수 설정
     */
    setItemCount(count) {
        this.config.itemCount = count;
    }

    /**
     * 결과 콜백 설정
     */
    setResultCallback(callback) {
        this.config.onResult = callback;
    }

    /**
     * 회전 업데이트 콜백 설정
     */
    setRotationCallback(callback) {
        this.config.onRotationUpdate = callback;
    }

    /**
     * 컨테이너 설정 및 이벤트 등록
     */
    setContainer(container) {
        this.config.container = container;
        this.setupEvents();
    }

    /**
     * 이벤트 리스너 설정
     */
    setupEvents() {
        if (!this.config.container) return;

        const container = this.config.container;

        // 마우스 이벤트
        container.addEventListener('mousedown', this.boundEvents.startDrag);
        document.addEventListener('mousemove', this.boundEvents.drag);
        document.addEventListener('mouseup', this.boundEvents.endDrag);

        // 터치 이벤트
        container.addEventListener('touchstart', this.boundEvents.startDrag);
        document.addEventListener('touchmove', this.boundEvents.drag);
        document.addEventListener('touchend', this.boundEvents.endDrag);
    }

    /**
     * 이벤트 리스너 제거
     */
    removeEvents() {
        if (!this.config.container) return;

        const container = this.config.container;

        container.removeEventListener('mousedown', this.boundEvents.startDrag);
        document.removeEventListener('mousemove', this.boundEvents.drag);
        document.removeEventListener('mouseup', this.boundEvents.endDrag);

        container.removeEventListener('touchstart', this.boundEvents.startDrag);
        document.removeEventListener('touchmove', this.boundEvents.drag);
        document.removeEventListener('touchend', this.boundEvents.endDrag);
    }

    /**
     * 마우스/터치 위치에서 각도 계산
     */
    getAngleFromEvent(e) {
        if (!this.config.container) return 0;

        const rect = this.config.container.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;
        
        const clientX = e.clientX || (e.touches && e.touches[0].clientX);
        const clientY = e.clientY || (e.touches && e.touches[0].clientY);
        
        const deltaX = clientX - centerX;
        const deltaY = clientY - centerY;
        
        return Math.atan2(deltaY, deltaX) * 180 / Math.PI;
    }

    /**
     * 드래그 시작
     */
    startDrag(e) {
        if (this.isSpinning) return;
        
        this.isDragging = true;
        this.lastAngle = this.getAngleFromEvent(e);
        this.velocityHistory = [];
        
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
            this.animationId = null;
        }
        
        e.preventDefault();
    }

    /**
     * 드래그 중
     */
    drag(e) {
        if (!this.isDragging) return;
        
        const currentAngle = this.getAngleFromEvent(e);
        let deltaAngle = currentAngle - this.lastAngle;
        
        // 각도 차이가 180도를 넘으면 반대 방향으로 계산
        if (deltaAngle > 180) deltaAngle -= 360;
        if (deltaAngle < -180) deltaAngle += 360;
        
        this.currentRotation += deltaAngle;
        this.updateRotation();
        
        // 속도 계산을 위한 히스토리 저장
        this.velocityHistory.push({
            angle: deltaAngle,
            time: Date.now()
        });
        
        // 최근 100ms 데이터만 유지
        const now = Date.now();
        this.velocityHistory = this.velocityHistory.filter(item => now - item.time < 100);
        
        this.lastAngle = currentAngle;
        e.preventDefault();
    }

    /**
     * 드래그 종료
     */
    endDrag(e) {
        if (!this.isDragging) return;
        
        this.isDragging = false;
        
        // 최근 속도 계산
        if (this.velocityHistory.length > 1) {
            const recent = this.velocityHistory.slice(-5);
            let totalVelocity = 0;
            
            for (let i = 1; i < recent.length; i++) {
                const timeDiff = recent[i].time - recent[i-1].time;
                if (timeDiff > 0) {
                    totalVelocity += recent[i].angle / timeDiff * 16;
                }
            }
            
            this.velocity = totalVelocity / (recent.length - 1);
            this.velocity = Math.max(Math.min(this.velocity, this.config.maxVelocity), -this.config.maxVelocity);
            
            if (Math.abs(this.velocity) > this.config.minVelocity) {
                this.startInertia();
            } else {
                this.checkResult();
            }
        } else {
            this.checkResult();
        }
    }

    /**
     * 관성 애니메이션 시작
     */
    startInertia() {
        this.isSpinning = true;
        
        const animate = () => {
            this.velocity *= this.config.friction;
            this.currentRotation += this.velocity;
            this.updateRotation();
            
            if (Math.abs(this.velocity) > this.config.minVelocity) {
                this.animationId = requestAnimationFrame(animate);
            } else {
                this.isSpinning = false;
                this.animationId = null;
                this.checkResult();
            }
        };
        
        this.animationId = requestAnimationFrame(animate);
    }

    /**
     * 회전 업데이트 (콜백 호출)
     */
    updateRotation() {
        if (this.config.onRotationUpdate) {
            this.config.onRotationUpdate(this.currentRotation);
        }
    }

    /**
     * 결과 계산 및 콜백 호출
     */
    checkResult() {
        const normalizedAngle = ((this.currentRotation % 360) + 360) % 360;
        const angleStep = 360 / this.config.itemCount;
        const selectedIndex = Math.floor(((360 - normalizedAngle + (angleStep / 2)) % 360) / angleStep);
        
        if (this.config.onResult) {
            this.config.onResult(selectedIndex);
        }
    }

    /**
     * 자동 스핀 (버튼 클릭)
     */
    spin() {
        if (this.isSpinning || this.isDragging) return;
        
        // 랜덤 스핀
        this.velocity = (Math.random() * 15 + 10) * (Math.random() > 0.5 ? 1 : -1);
        this.startInertia();
    }

    /**
     * 부드러운 스핀 (애니메이션)
     */
    smoothSpin(targetIndex = null) {
        if (this.isSpinning || this.isDragging) return;

        this.isSpinning = true;
        const baseSpins = 720 + Math.random() * 1440; // 2-6바퀴
        
        let targetRotation;
        if (targetIndex !== null) {
            const angleStep = 360 / this.config.itemCount;
            const targetAngle = targetIndex * angleStep;
            targetRotation = this.currentRotation + baseSpins + (360 - targetAngle);
        } else {
            targetRotation = this.currentRotation + baseSpins;
        }

        // CSS 트랜지션 사용
        if (this.config.onRotationUpdate) {
            this.config.onRotationUpdate(targetRotation, true); // 두 번째 파라미터로 트랜지션 사용 표시
        }

        this.currentRotation = targetRotation;

        setTimeout(() => {
            this.isSpinning = false;
            this.checkResult();
        }, 3000);
    }

    /**
     * 현재 상태 반환
     */
    getState() {
        return {
            rotation: this.currentRotation,
            velocity: this.velocity,
            isSpinning: this.isSpinning,
            isDragging: this.isDragging
        };
    }

    /**
     * 엔진 정리
     */
    destroy() {
        this.removeEvents();
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
    }
}

// ES6 모듈 내보내기
if (typeof module !== 'undefined' && module.exports) {
    module.exports = RouletteEngine;
}