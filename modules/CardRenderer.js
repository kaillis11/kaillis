/**
 * 카드 렌더러 모듈
 * - 메뉴 카드 시각적 렌더링 전담
 * - 다양한 카드 스타일 지원
 * - 애니메이션 및 인터랙션 효과
 * - 룰렛과 독립적으로 사용 가능
 */

class CardRenderer {
    constructor(options = {}) {
        this.config = {
            containerSelector: '#roulette',
            cardWidth: 400,
            cardHeight: 600,
            radius: 1800,
            fontSize: {
                title: 20,
                rank: 16,
                name: 13
            },
            colors: {
                background: 'rgba(255, 255, 255, 0.95)',
                border: 'rgba(200, 200, 200, 0.6)',
                primary: '#ff6b35',
                text: '#333'
            },
            animation: {
                enabled: true,
                duration: '0.3s'
            },
            ...options
        };

        this.container = null;
        this.cards = [];
    }

    /**
     * 컨테이너 설정
     */
    setContainer(selector) {
        this.container = document.querySelector(selector);
        if (!this.container) {
            throw new Error(`Container ${selector} not found`);
        }
    }

    /**
     * 카드 스타일 업데이트
     */
    updateConfig(newConfig) {
        this.config = { ...this.config, ...newConfig };
    }

    /**
     * 배민 스타일 카테고리 카드 렌더링
     */
    renderCategoryCards(categories) {
        if (!this.container) {
            throw new Error('Container not set. Call setContainer() first.');
        }

        // 기존 카드 제거
        this.clearCards();

        const angleStep = 360 / categories.length;
        
        categories.forEach((category, index) => {
            const card = this.createCategoryCard(category, index, angleStep);
            this.container.appendChild(card);
            this.cards.push(card);
        });
    }

    /**
     * 개별 메뉴 카드 렌더링 (기존 방식)
     */
    renderMenuCards(menuItems) {
        if (!this.container) {
            throw new Error('Container not set. Call setContainer() first.');
        }

        this.clearCards();

        const angleStep = 360 / menuItems.length;
        
        menuItems.forEach((item, index) => {
            const card = this.createMenuCard(item, index, angleStep);
            this.container.appendChild(card);
            this.cards.push(card);
        });
    }

    /**
     * 카테고리 카드 생성
     */
    createCategoryCard(category, index, angleStep) {
        const card = document.createElement('div');
        card.className = 'menu-category-card';
        card.dataset.categoryId = category.id || index;
        
        // 기본 스타일 적용
        this.applyCategoryCardStyles(card);
        
        // 카테고리 제목 생성
        const title = this.createCategoryTitle(category.title);
        card.appendChild(title);
        
        // 메뉴 아이템들 생성
        category.items.forEach(item => {
            const itemRow = this.createMenuItemRow(item);
            card.appendChild(itemRow);
        });
        
        // 위치 계산 및 배치
        this.positionCard(card, index, angleStep);
        
        return card;
    }

    /**
     * 개별 메뉴 카드 생성
     */
    createMenuCard(menuItem, index, angleStep) {
        const card = document.createElement('div');
        card.className = 'menu-item-card';
        card.dataset.menuId = menuItem.id || index;
        
        // 기본 스타일 적용
        this.applyMenuCardStyles(card);
        
        // 랭킹 요소
        if (menuItem.rank) {
            const rank = this.createElement('div', 'menu-rank', menuItem.rank);
            card.appendChild(rank);
        }
        
        // 아이콘 요소
        const icon = this.createElement('div', 'menu-icon', menuItem.icon || '🍽️');
        card.appendChild(icon);
        
        // 이름 요소
        const name = this.createElement('div', 'menu-name', menuItem.name);
        card.appendChild(name);
        
        // 위치 계산 및 배치
        this.positionCard(card, index, angleStep);
        
        return card;
    }

    /**
     * 카테고리 제목 생성
     */
    createCategoryTitle(titleText) {
        const title = document.createElement('div');
        title.className = 'category-title';
        title.textContent = titleText;
        
        Object.assign(title.style, {
            fontSize: `${this.config.fontSize.title}px`,
            fontWeight: '900',
            color: this.config.colors.text,
            textAlign: 'center',
            marginBottom: '15px',
            paddingBottom: '8px',
            borderBottom: '2px solid #f0f0f0'
        });
        
        return title;
    }

    /**
     * 메뉴 아이템 행 생성
     */
    createMenuItemRow(item) {
        const row = document.createElement('div');
        row.className = 'menu-item-row';
        
        // 행 스타일
        Object.assign(row.style, {
            display: 'flex',
            alignItems: 'center',
            padding: '8px 6px',
            margin: '3px 0',
            background: 'rgba(248, 249, 250, 0.8)',
            borderRadius: '8px',
            transition: this.config.animation.enabled ? 'all 0.3s ease' : 'none'
        });
        
        // 호버 효과
        if (this.config.animation.enabled) {
            row.addEventListener('mouseenter', () => {
                row.style.background = 'rgba(255, 107, 53, 0.1)';
                row.style.transform = 'translateX(3px)';
            });
            
            row.addEventListener('mouseleave', () => {
                row.style.background = 'rgba(248, 249, 250, 0.8)';
                row.style.transform = 'translateX(0)';
            });
        }
        
        // 랭킹 번호
        const rank = this.createElement('div', 'rank-number', item.rank);
        Object.assign(rank.style, {
            fontSize: `${this.config.fontSize.rank}px`,
            fontWeight: '900',
            color: this.config.colors.primary,
            width: '35px',
            textAlign: 'center'
        });
        
        // 메뉴 아이콘
        const icon = this.createElement('div', 'menu-icon', item.icon);
        Object.assign(icon.style, {
            width: '40px',
            height: '40px',
            borderRadius: '50%',
            background: 'linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '18px',
            margin: '0 10px',
            boxShadow: '0 2px 6px rgba(0,0,0,0.1)',
            border: '2px solid #fff'
        });
        
        // 메뉴 이름
        const name = this.createElement('div', 'menu-name', item.name);
        Object.assign(name.style, {
            fontSize: `${this.config.fontSize.name}px`,
            fontWeight: '600',
            color: this.config.colors.text,
            flex: '1'
        });
        
        row.appendChild(rank);
        row.appendChild(icon);
        row.appendChild(name);
        
        return row;
    }

    /**
     * 카테고리 카드 스타일 적용
     */
    applyCategoryCardStyles(card) {
        Object.assign(card.style, {
            position: 'absolute',
            width: `${this.config.cardWidth}px`,
            height: `${this.config.cardHeight}px`,
            background: this.config.colors.background,
            border: `1px solid ${this.config.colors.border}`,
            borderRadius: '15px',
            display: 'flex',
            flexDirection: 'column',
            padding: '15px',
            boxSizing: 'border-box',
            transformOrigin: 'center',
            boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
            cursor: 'grab',
            backdropFilter: 'blur(5px)'
        });
    }

    /**
     * 개별 메뉴 카드 스타일 적용
     */
    applyMenuCardStyles(card) {
        Object.assign(card.style, {
            position: 'absolute',
            width: `${this.config.cardWidth}px`,
            height: `${this.config.cardHeight}px`,
            background: this.config.colors.background,
            border: `1px solid ${this.config.colors.border}`,
            borderRadius: '15px',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'space-between',
            padding: '30px 20px',
            boxSizing: 'border-box',
            transformOrigin: 'center',
            boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
            cursor: 'grab',
            textAlign: 'center',
            backdropFilter: 'blur(5px)'
        });
    }

    /**
     * 카드 위치 계산 및 배치
     */
    positionCard(card, index, angleStep) {
        const angle = angleStep * index;
        const radius = this.config.radius;
        const x = Math.cos((angle - 90) * Math.PI / 180) * radius;
        const y = Math.sin((angle - 90) * Math.PI / 180) * radius;
        
        card.style.left = `calc(50% + ${x}px - ${this.config.cardWidth/2}px)`;
        card.style.top = `calc(50% + ${y}px - ${this.config.cardHeight/2}px)`;
        card.style.transform = `rotate(${angle}deg)`;
    }

    /**
     * 헬퍼: DOM 요소 생성
     */
    createElement(tag, className, textContent) {
        const element = document.createElement(tag);
        element.className = className;
        if (textContent) element.textContent = textContent;
        return element;
    }

    /**
     * 모든 카드 제거
     */
    clearCards() {
        this.cards.forEach(card => {
            if (card.parentNode) {
                card.parentNode.removeChild(card);
            }
        });
        this.cards = [];
    }

    /**
     * 카드 회전 업데이트
     */
    updateRotation(rotation, useTransition = false) {
        if (!this.container) return;

        if (useTransition) {
            this.container.style.transition = 'transform 3s cubic-bezier(0.17, 0.67, 0.12, 0.99)';
        } else {
            this.container.style.transition = 'transform 0.3s ease-out';
        }

        this.container.style.transform = `rotate(${rotation}deg)`;
    }

    /**
     * 특정 카드 하이라이트
     */
    highlightCard(index) {
        this.cards.forEach((card, i) => {
            if (i === index) {
                card.style.boxShadow = '0 8px 25px rgba(255, 107, 53, 0.4)';
                card.style.transform += ' scale(1.05)';
            } else {
                card.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';
                card.style.transform = card.style.transform.replace(' scale(1.05)', '');
            }
        });
    }

    /**
     * 모든 카드 하이라이트 제거
     */
    clearHighlight() {
        this.cards.forEach(card => {
            card.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';
            card.style.transform = card.style.transform.replace(' scale(1.05)', '');
        });
    }

    /**
     * 카드 개수 반환
     */
    getCardCount() {
        return this.cards.length;
    }
}

// ES6 모듈 내보내기
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CardRenderer;
}