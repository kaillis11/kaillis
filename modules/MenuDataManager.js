/**
 * 메뉴 데이터 관리 모듈
 * - 카테고리와 메뉴 데이터의 중앙 관리
 * - 룰렛과 카드 시스템 모두에서 사용 가능
 * - 확장성을 고려한 데이터 구조
 */

class MenuDataManager {
    constructor() {
        this.categories = [];
        this.loadDefaultData();
    }

    /**
     * 기본 메뉴 데이터 로드
     */
    loadDefaultData() {
        this.categories = [
            {
                id: "chicken",
                title: "🍗 치킨",
                items: [
                    { rank: "1위", name: "크크크치킨", icon: "🍗" },
                    { rank: "2위", name: "뿌링클", icon: "🍗" },
                    { rank: "3위", name: "교촌오리지날", icon: "🍗" },
                    { rank: "4위", name: "황금올리브", icon: "🍗" },
                    { rank: "5위", name: "고추바사삭", icon: "🍗" },
                    { rank: "6위", name: "양념치킨", icon: "🍗" },
                    { rank: "7위", name: "후라이드치킨", icon: "🍗" },
                    { rank: "8위", name: "맛초킹", icon: "🍗" }
                ]
            },
            {
                id: "meat",
                title: "🥘 고기·구이",
                items: [
                    { rank: "1위", name: "삼겹살구이", icon: "🥩" },
                    { rank: "2위", name: "갈비구이", icon: "🥩" },
                    { rank: "3위", name: "제육볶음", icon: "🥘" },
                    { rank: "4위", name: "대패삼겹살", icon: "🥩" },
                    { rank: "5위", name: "항정살구이", icon: "🥩" },
                    { rank: "6위", name: "목살구이", icon: "🥩" },
                    { rank: "7위", name: "불고기", icon: "🥘" },
                    { rank: "8위", name: "닭갈비", icon: "🍗" }
                ]
            },
            {
                id: "bunsik",
                title: "🍜 분식",
                items: [
                    { rank: "1위", name: "떡볶이", icon: "🍜" },
                    { rank: "2위", name: "김밥", icon: "🍙" },
                    { rank: "3위", name: "라면", icon: "🍜" },
                    { rank: "4위", name: "튀김", icon: "🍤" },
                    { rank: "5위", name: "순대", icon: "🥓" },
                    { rank: "6위", name: "호떡", icon: "🥞" },
                    { rank: "7위", name: "어묵", icon: "🍢" },
                    { rank: "8위", name: "쫄면", icon: "🍜" }
                ]
            },
            {
                id: "lunchbox",
                title: "🍱 도시락",
                items: [
                    { rank: "1위", name: "치킨마요덮밥", icon: "🍱" },
                    { rank: "2위", name: "불고기덮밥", icon: "🍱" },
                    { rank: "3위", name: "비빔밥", icon: "🍚" },
                    { rank: "4위", name: "돈까스덮밥", icon: "🍱" },
                    { rank: "5위", name: "스팸마요덮밥", icon: "🍱" },
                    { rank: "6위", name: "제육덮밥", icon: "🍱" },
                    { rank: "7위", name: "참치마요덮밥", icon: "🍱" },
                    { rank: "8위", name: "김치볶음밥", icon: "🍚" }
                ]
            },
            {
                id: "fastfood",
                title: "🍔 패스트푸드",
                items: [
                    { rank: "1위", name: "불고기버거", icon: "🍔" },
                    { rank: "2위", name: "빅맥", icon: "🍔" },
                    { rank: "3위", name: "와퍼", icon: "🍔" },
                    { rank: "4위", name: "징거버거", icon: "🍔" },
                    { rank: "5위", name: "싸이버거", icon: "🍔" },
                    { rank: "6위", name: "새우버거", icon: "🍔" },
                    { rank: "7위", name: "더블치즈버거", icon: "🍔" },
                    { rank: "8위", name: "상하이스파이시", icon: "🍔" }
                ]
            },
            {
                id: "japanese",
                title: "🍛 일식",
                items: [
                    { rank: "1위", name: "모듬초밥", icon: "🍣" },
                    { rank: "2위", name: "돈카츠", icon: "🍛" },
                    { rank: "3위", name: "우동", icon: "🍜" },
                    { rank: "4위", name: "연어덮밥", icon: "🍣" },
                    { rank: "5위", name: "규동", icon: "🍛" },
                    { rank: "6위", name: "가츠동", icon: "🍛" },
                    { rank: "7위", name: "텐동", icon: "🍛" },
                    { rank: "8위", name: "소바", icon: "🍜" }
                ]
            },
            {
                id: "western",
                title: "🍝 양식",
                items: [
                    { rank: "1위", name: "크림파스타", icon: "🍝" },
                    { rank: "2위", name: "토마토파스타", icon: "🍝" },
                    { rank: "3위", name: "피자", icon: "🍕" },
                    { rank: "4위", name: "오일파스타", icon: "🍝" },
                    { rank: "5위", name: "라자냐", icon: "🧀" },
                    { rank: "6위", name: "스테이크", icon: "🥩" },
                    { rank: "7위", name: "리조또", icon: "🍚" },
                    { rank: "8위", name: "그라탕", icon: "🧀" }
                ]
            },
            {
                id: "dessert",
                title: "🥤 카페·디저트",
                items: [
                    { rank: "1위", name: "아이스크림", icon: "🍦" },
                    { rank: "2위", name: "케이크", icon: "🍰" },
                    { rank: "3위", name: "마카롱", icon: "🧁" },
                    { rank: "4위", name: "붕어빵", icon: "🧁" },
                    { rank: "5위", name: "호떡", icon: "🥞" },
                    { rank: "6위", name: "와플", icon: "🧇" },
                    { rank: "7위", name: "크로플", icon: "🥐" },
                    { rank: "8위", name: "티라미수", icon: "🍰" }
                ]
            },
            {
                id: "chinese",
                title: "🥟 중식",
                items: [
                    { rank: "1위", name: "짜장면", icon: "🍜" },
                    { rank: "2위", name: "짬뽕", icon: "🍲" },
                    { rank: "3위", name: "탕수육", icon: "🥘" },
                    { rank: "4위", name: "볶음밥", icon: "🍚" },
                    { rank: "5위", name: "짬짜면", icon: "🍜" },
                    { rank: "6위", name: "군만두", icon: "🥟" },
                    { rank: "7위", name: "마라탕", icon: "🌶️" },
                    { rank: "8위", name: "유산슬", icon: "🥘" }
                ]
            },
            {
                id: "latenight",
                title: "🌙 야식",
                items: [
                    { rank: "1위", name: "치킨", icon: "🍗" },
                    { rank: "2위", name: "족발", icon: "🦶" },
                    { rank: "3위", name: "보쌈", icon: "🥓" },
                    { rank: "4위", name: "피자", icon: "🍕" },
                    { rank: "5위", name: "마라탕", icon: "🌶️" },
                    { rank: "6위", name: "곱창", icon: "🥘" },
                    { rank: "7위", name: "닭발", icon: "🍗" },
                    { rank: "8위", name: "포장마차", icon: "🍜" }
                ]
            },
            {
                id: "soup",
                title: "🍲 찜·탕",
                items: [
                    { rank: "1위", name: "갈비찜", icon: "🍲" },
                    { rank: "2위", name: "삼계탕", icon: "🍲" },
                    { rank: "3위", name: "김치찌개", icon: "🍲" },
                    { rank: "4위", name: "된장찌개", icon: "🍲" },
                    { rank: "5위", name: "부대찌개", icon: "🍲" },
                    { rank: "6위", name: "찜닭", icon: "🍲" },
                    { rank: "7위", name: "해물탕", icon: "🍲" },
                    { rank: "8위", name: "감자탕", icon: "🍲" }
                ]
            },
            {
                id: "asian",
                title: "🌏 아시안",
                items: [
                    { rank: "1위", name: "쌀국수", icon: "🍜" },
                    { rank: "2위", name: "팟타이", icon: "🍜" },
                    { rank: "3위", name: "카레", icon: "🍛" },
                    { rank: "4위", name: "똠양꿍", icon: "🍲" },
                    { rank: "5위", name: "월남쌈", icon: "🌯" },
                    { rank: "6위", name: "나시고렝", icon: "🍚" },
                    { rank: "7위", name: "분짜", icon: "🍜" },
                    { rank: "8위", name: "마라샹궈", icon: "🌶️" }
                ]
            }
        ];
    }

    /**
     * 모든 카테고리 반환
     */
    getAllCategories() {
        return [...this.categories];
    }

    /**
     * 특정 카테고리 반환
     */
    getCategory(categoryId) {
        return this.categories.find(cat => cat.id === categoryId);
    }

    /**
     * 카테고리 개수 반환
     */
    getCategoryCount() {
        return this.categories.length;
    }

    /**
     * 카테고리 추가
     */
    addCategory(category) {
        if (!category.id || !category.title || !category.items) {
            throw new Error('Invalid category format');
        }
        this.categories.push(category);
    }

    /**
     * 메뉴 추가 (특정 카테고리에)
     */
    addMenuItem(categoryId, menuItem) {
        const category = this.getCategory(categoryId);
        if (!category) {
            throw new Error(`Category ${categoryId} not found`);
        }
        category.items.push(menuItem);
    }

    /**
     * TOP N 메뉴만 반환 (랭킹 제한)
     */
    getCategoriesWithLimit(topN = 5) {
        return this.categories.map(category => ({
            ...category,
            items: category.items.slice(0, topN)
        }));
    }

    /**
     * 랜덤 메뉴 선택
     */
    getRandomMenu() {
        const randomCategory = this.categories[Math.floor(Math.random() * this.categories.length)];
        const randomItem = randomCategory.items[Math.floor(Math.random() * randomCategory.items.length)];
        return {
            category: randomCategory,
            item: randomItem
        };
    }

    /**
     * 검색 기능
     */
    searchMenus(keyword) {
        const results = [];
        this.categories.forEach(category => {
            category.items.forEach(item => {
                if (item.name.includes(keyword) || category.title.includes(keyword)) {
                    results.push({
                        category: category,
                        item: item
                    });
                }
            });
        });
        return results;
    }

    /**
     * 데이터 내보내기 (JSON)
     */
    exportData() {
        return JSON.stringify(this.categories, null, 2);
    }

    /**
     * 데이터 가져오기 (JSON)
     */
    importData(jsonData) {
        try {
            this.categories = JSON.parse(jsonData);
        } catch (error) {
            throw new Error('Invalid JSON data');
        }
    }
}

// ES6 모듈 내보내기
if (typeof module !== 'undefined' && module.exports) {
    module.exports = MenuDataManager;
}