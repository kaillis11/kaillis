/**
 * 룰렛 애플리케이션 통합 모듈
 * - MenuDataManager, RouletteEngine, CardRenderer를 조합
 * - 완전한 룰렛 시스템 제공
 * - 쉬운 설정과 사용법
 */

class RouletteApp {
    constructor(containerSelector, options = {}) {
        // 기본 설정
        this.config = {
            topN: 5,
            cardStyle: 'category', // 'category' or 'menu'
            autoResize: true,
            showResult: true,
            resultSelector: '#result',
            selectedMenuSelector: '#selected-menu',
            ...options
        };

        // 모듈 인스턴스들
        this.dataManager = new MenuDataManager();
        this.cardRenderer = new CardRenderer();
        this.engine = null;

        // DOM 요소들
        this.container = document.querySelector(containerSelector);
        this.resultElement = null;
        this.selectedMenuElement = null;

        this.init();
    }

    /**
     * 초기화
     */
    init() {
        if (!this.container) {
            throw new Error('Container element not found');
        }

        // 결과 표시 요소 찾기
        if (this.config.showResult) {
            this.resultElement = document.querySelector(this.config.resultSelector);
            this.selectedMenuElement = document.querySelector(this.config.selectedMenuSelector);
        }

        // 카드 렌더러 설정
        this.cardRenderer.setContainer(this.container.parentElement.querySelector('.roulette-wheel'));

        // 룰렛 엔진 초기화
        this.initEngine();

        // 초기 렌더링
        this.render();
    }

    /**
     * 룰렛 엔진 초기화
     */
    initEngine() {
        const categories = this.getCurrentData();
        
        this.engine = new RouletteEngine({
            itemCount: categories.length,
            container: this.container,
            onResult: this.handleResult.bind(this),
            onRotationUpdate: this.handleRotationUpdate.bind(this)
        });
    }

    /**
     * 현재 데이터 가져오기
     */
    getCurrentData() {
        if (this.config.cardStyle === 'category') {
            return this.dataManager.getCategoriesWithLimit(this.config.topN);
        } else {
            // 개별 메뉴 모드 (모든 메뉴를 플랫하게)
            const categories = this.dataManager.getCategoriesWithLimit(this.config.topN);
            const allMenus = [];
            categories.forEach(category => {
                category.items.forEach(item => {
                    allMenus.push({
                        ...item,
                        category: category.title
                    });
                });
            });
            return allMenus;
        }
    }

    /**
     * 렌더링
     */
    render() {
        const data = this.getCurrentData();
        
        if (this.config.cardStyle === 'category') {
            this.cardRenderer.renderCategoryCards(data);
        } else {
            this.cardRenderer.renderMenuCards(data);
        }

        // 엔진 아이템 수 업데이트
        if (this.engine) {
            this.engine.setItemCount(data.length);
        }
    }

    /**
     * 회전 업데이트 핸들러
     */
    handleRotationUpdate(rotation, useTransition = false) {
        this.cardRenderer.updateRotation(rotation, useTransition);
    }

    /**
     * 결과 핸들러
     */
    handleResult(selectedIndex) {
        const data = this.getCurrentData();
        const selectedItem = data[selectedIndex];

        // 카드 하이라이트
        this.cardRenderer.highlightCard(selectedIndex);

        // 결과 표시
        if (this.config.showResult && this.selectedMenuElement) {
            this.displayResult(selectedItem);
        }

        // 외부 콜백 호출
        if (this.config.onResult) {
            this.config.onResult(selectedItem, selectedIndex);
        }
    }

    /**
     * 결과 표시
     */
    displayResult(selectedItem) {
        let resultHtml = '';

        if (this.config.cardStyle === 'category') {
            // 카테고리 모드: 카테고리에서 랜덤 메뉴 선택
            const randomMenu = selectedItem.items[Math.floor(Math.random() * selectedItem.items.length)];
            resultHtml = `
                <strong>${selectedItem.title}</strong><br>
                ${randomMenu.icon} <strong>${randomMenu.name}</strong> (${randomMenu.rank})
            `;
        } else {
            // 개별 메뉴 모드
            resultHtml = `
                ${selectedItem.icon} <strong>${selectedItem.name}</strong><br>
                <small style="color: #ff6b35;">${selectedItem.rank} 인기 메뉴</small>
            `;
        }

        this.selectedMenuElement.innerHTML = resultHtml;
        
        if (this.resultElement) {
            this.resultElement.style.display = 'block';
        }
    }

    /**
     * TOP N 설정 변경
     */
    setTopN(n) {
        this.config.topN = n;
        this.render();
    }

    /**
     * 카드 스타일 변경
     */
    setCardStyle(style) {
        if (style !== 'category' && style !== 'menu') {
            throw new Error('Card style must be "category" or "menu"');
        }
        
        this.config.cardStyle = style;
        this.render();
    }

    /**
     * 메뉴 데이터 추가
     */
    addCategory(category) {
        this.dataManager.addCategory(category);
        this.render();
    }

    /**
     * 메뉴 아이템 추가
     */
    addMenuItem(categoryId, menuItem) {
        this.dataManager.addMenuItem(categoryId, menuItem);
        this.render();
    }

    /**
     * 스핀 (드래그 물리 엔진)
     */
    spin() {
        if (this.engine) {
            this.engine.spin();
        }
    }

    /**
     * 부드러운 스핀 (CSS 애니메이션)
     */
    smoothSpin(targetIndex = null) {
        if (this.engine) {
            this.engine.smoothSpin(targetIndex);
        }
    }

    /**
     * 특정 결과로 스핀
     */
    spinToResult(categoryId, menuName = null) {
        const data = this.getCurrentData();
        let targetIndex = -1;

        if (this.config.cardStyle === 'category') {
            targetIndex = data.findIndex(category => category.id === categoryId);
        } else {
            if (menuName) {
                targetIndex = data.findIndex(item => 
                    item.category === categoryId && item.name === menuName
                );
            } else {
                targetIndex = data.findIndex(item => item.category === categoryId);
            }
        }

        if (targetIndex !== -1) {
            this.smoothSpin(targetIndex);
        }
    }

    /**
     * 결과 숨기기
     */
    hideResult() {
        if (this.resultElement) {
            this.resultElement.style.display = 'none';
        }
        this.cardRenderer.clearHighlight();
    }

    /**
     * 상태 정보 반환
     */
    getState() {
        return {
            config: this.config,
            dataCount: this.dataManager.getCategoryCount(),
            engineState: this.engine ? this.engine.getState() : null,
            cardCount: this.cardRenderer.getCardCount()
        };
    }

    /**
     * 데이터 내보내기
     */
    exportData() {
        return this.dataManager.exportData();
    }

    /**
     * 데이터 가져오기
     */
    importData(jsonData) {
        this.dataManager.importData(jsonData);
        this.render();
    }

    /**
     * 검색 기능
     */
    search(keyword) {
        return this.dataManager.searchMenus(keyword);
    }

    /**
     * 정리
     */
    destroy() {
        if (this.engine) {
            this.engine.destroy();
        }
        this.cardRenderer.clearCards();
    }
}

// ES6 모듈 내보내기
if (typeof module !== 'undefined' && module.exports) {
    module.exports = RouletteApp;
}