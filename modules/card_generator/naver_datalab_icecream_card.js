// 🍦 네이버 데이터랩 아이스크림 인기순위 카드
// 2025.06.08 ~ 2025.07.08 기준
// 생성일: 2025-07-09

// TOP 40 전체 데이터
const NAVER_DATALAB_ICECREAM_TOP40 = [
    { rank: 1, name: '아이스크림', icon: '🍦', tag: '검색량 1위' },
    { rank: 2, name: '라라스윗', icon: '🍨', tag: '저당 아이스크림 대표' },
    { rank: 3, name: '하겐다즈', icon: '🍨', tag: '프리미엄 아이스크림' },
    { rank: 4, name: '미니스크류바', icon: '🍦', tag: '롯데 인기 제품' },
    { rank: 5, name: '붕어싸만코', icon: '🐟', tag: '빙그레 스테디셀러' },
    { rank: 6, name: '구슬아이스크림', icon: '🔮', tag: '추억의 아이스크림' },
    { rank: 7, name: '하겐다즈파인트', icon: '🥄', tag: '대용량 파인트' },
    { rank: 8, name: '팥빙수', icon: '🍧', tag: '여름 대표 간식' },
    { rank: 9, name: '제로아이스크림', icon: '0️⃣', tag: '무설탕/저칼로리' },
    { rank: 10, name: '저당아이스크림', icon: '🍦', tag: '건강한 선택' },
    { rank: 11, name: '월드콘', icon: '🌍', tag: '롯데 콘 아이스크림' },
    { rank: 12, name: '설레임', icon: '💕', tag: '빙그레 신제품' },
    { rank: 13, name: '상하목장소프트믹스', icon: '🥛', tag: '부드러운 맛' },
    { rank: 14, name: '폴라레티', icon: '❄️', tag: '얼음과자' },
    { rank: 15, name: '티코말차', icon: '🍵', tag: '말차맛 아이스크림' },
    { rank: 16, name: '미니죠스바', icon: '🦈', tag: '미니 사이즈' },
    { rank: 17, name: '티코아이스크림', icon: '🍦', tag: '롯데 티코' },
    { rank: 18, name: '조이아이스크림', icon: '😊', tag: '해태 제품' },
    { rank: 19, name: '상하목장아이스크림', icon: '🐄', tag: '프리미엄 우유' },
    { rank: 20, name: '라라스윗아이스크림', icon: '🍨', tag: '저당 전문 브랜드' },
    { rank: 21, name: '따옴아이스크림', icon: '🍦', tag: '따옴 브랜드' },
    { rank: 22, name: '투게더아이스크림', icon: '🤝', tag: '빙그레 투게더' },
    { rank: 23, name: '메로나', icon: '🍈', tag: '빙그레 대표상품' },
    { rank: 24, name: '폴라포', icon: '🐻', tag: '곰돌이 아이스크림' },
    { rank: 25, name: '라라스윗제로바', icon: '0️⃣', tag: '제로칼로리 바' },
    { rank: 26, name: '투게더', icon: '💑', tag: '연인 아이스크림' },
    { rank: 27, name: '딥앤로우', icon: '🍦', tag: '프리미엄 브랜드' },
    { rank: 28, name: '파인애플샤베트', icon: '🍍', tag: '과일 샤베트' },
    { rank: 29, name: '라벨리인절미빙수', icon: '🍧', tag: '인절미 빙수' },
    { rank: 30, name: '인절미빙수', icon: '🍧', tag: '전통 디저트' },
    { rank: 31, name: '설레임아이스크림', icon: '💗', tag: '빙그레 설레임' },
    { rank: 32, name: '요맘때', icon: '⏰', tag: '시즌 한정' },
    { rank: 33, name: '요거트아이스크림', icon: '🥛', tag: '요거트 맛' },
    { rank: 34, name: '대용량아이스크림', icon: '📦', tag: '가족용 사이즈' },
    { rank: 35, name: '하겐다즈아이스크림', icon: '🍨', tag: '프리미엄 라인' },
    { rank: 36, name: '하겐다즈케이크', icon: '🎂', tag: '아이스크림 케이크' },
    { rank: 37, name: '돼지바', icon: '🐷', tag: '롯데 돼지바' },
    { rank: 38, name: '고드름아이스크림', icon: '🧊', tag: '시원한 얼음과자' },
    { rank: 39, name: '라벨리아이스크림', icon: '🌸', tag: '라벨리 브랜드' },
    { rank: 40, name: '빵또아', icon: '🍞', tag: '빵 아이스크림' }
];

// 실시간 검색어처럼 변경되는 카드 (1-10위 / 11-20위 / 21-30위 / 31-40위)
const NAVER_DATALAB_ICECREAM_CARD = {
    title: '🍦 아이스크림 실시간 인기',
    id: 'icecream-trending',
    type: 'trending-realtime',
    source: '네이버 데이터랩',
    period: '2025.06.08 ~ 2025.07.08',
    rotation_interval: 5000, // 5초마다 순위 변경
    display_sets: [
        {
            range: '1-10위',
            items: NAVER_DATALAB_ICECREAM_TOP40.slice(0, 10).map(item => ({
                rank: `${item.rank}위`,
                name: item.name,
                icon: item.icon,
                tag: item.tag
            }))
        },
        {
            range: '11-20위',
            items: NAVER_DATALAB_ICECREAM_TOP40.slice(10, 20).map(item => ({
                rank: `${item.rank}위`,
                name: item.name,
                icon: item.icon,
                tag: item.tag
            }))
        },
        {
            range: '21-30위',
            items: NAVER_DATALAB_ICECREAM_TOP40.slice(20, 30).map(item => ({
                rank: `${item.rank}위`,
                name: item.name,
                icon: item.icon,
                tag: item.tag
            }))
        },
        {
            range: '31-40위',
            items: NAVER_DATALAB_ICECREAM_TOP40.slice(30, 40).map(item => ({
                rank: `${item.rank}위`,
                name: item.name,
                icon: item.icon,
                tag: item.tag
            }))
        }
    ]
};

// 트렌드 분석
const ICECREAM_TRENDS = {
    hot_keywords: ['저당', '제로', '프리미엄', '미니사이즈'],
    rising_brands: ['라라스윗', '상하목장', '티코'],
    classic_favorites: ['붕어싸만코', '월드콘', '구슬아이스크림'],
    premium_segment: ['하겐다즈', '상하목장'],
    health_conscious: ['라라스윗', '제로아이스크림', '저당아이스크림']
};

console.log('🍦 네이버 데이터랩 아이스크림 TOP 20 카드 생성 완료!');
console.log('📊 2025년 6-7월 실제 검색 트렌드 반영');
console.log('🔥 저당/제로 아이스크림 트렌드 확인!');