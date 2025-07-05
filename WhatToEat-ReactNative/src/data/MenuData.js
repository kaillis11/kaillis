// 24개 프리미엄 카드 데이터 (메뉴 + 쿠팡 + 랭킹)
export const PREMIUM_MENU_DATA = [
  // 메뉴 카드들 (12개)
  { title: '🍗 치킨', id: 'chicken', type: 'menu', items: [
    { rank: '1위', name: '후라이드치킨', icon: '🍗', tag: '바삭한 행복' },
    { rank: '2위', name: '양념치킨', icon: '🍗', tag: '달콤매콤' },
    { rank: '3위', name: '뿌링클치킨', icon: '🍗', tag: '부드러운 맛' },
    { rank: '4위', name: '허니콤보치킨', icon: '🍗', tag: '달콤한 유혹' },
    { rank: '5위', name: '황금올리브치킨', icon: '🍗', tag: '담백한 풍미' }
  ]},
  
  // 쿠팡 광고 카드
  { title: '🥤 치킨소스', id: 'coupang', type: 'coupang', rank: 'AD', items: [
    { name: '치킨소스 베스트 1위', icon: '🥤', tag: '🛒 쿠팡 베스트셀러' }
  ]},
  
  { title: '🥘 고기구이', id: 'meat', type: 'menu', items: [
    { rank: '1위', name: '삼겹살구이', icon: '🥩', tag: '육즙 가득' },
    { rank: '2위', name: '갈비구이', icon: '🥩', tag: '진한 풍미' },
    { rank: '3위', name: '제육볶음', icon: '🥘', tag: '매콤달콤' },
    { rank: '4위', name: '대패삼겹살', icon: '🥩', tag: '부드러운 식감' },
    { rank: '5위', name: '항정살구이', icon: '🥩', tag: '고급스러운 맛' }
  ]},
  
  // 랭킹 카드
  { title: '🏆 피자 TOP7', id: 'ranking', type: 'ranking', rank: 'TOP', items: [
    { name: '피자 랭킹 보기', icon: '🍕', tag: '🏆 인기 순위' }
  ]},
  
  { title: '🍜 분식', id: 'bunsik', type: 'menu', items: [
    { rank: '1위', name: '떡볶이', icon: '🍜', tag: '추억의 맛' },
    { rank: '2위', name: '김밥', icon: '🍙', tag: '든든한 한끼' },
    { rank: '3위', name: '라면', icon: '🍜', tag: '따뜻한 위로' },
    { rank: '4위', name: '순대', icon: '🥓', tag: '고소한 풍미' },
    { rank: '5위', name: '어묵', icon: '🍢', tag: '따끈한 국물' }
  ]},
  
  // 쿠팡 광고 카드
  { title: '🍳 구이팬', id: 'coupang', type: 'coupang', rank: 'AD', items: [
    { name: '에어프라이어 1위', icon: '🍳', tag: '🛒 쿠팡 베스트셀러' }
  ]},
  
  { title: '🍱 도시락', id: 'lunchbox', type: 'menu', items: [
    { rank: '1위', name: '치킨마요덮밥', icon: '🍱', tag: '든든한 한 끼' },
    { rank: '2위', name: '불고기덮밥', icon: '🍱', tag: '한국의 맛' },
    { rank: '3위', name: '비빔밥', icon: '🍚', tag: '건강한 선택' },
    { rank: '4위', name: '돈까스덮밥', icon: '🍱', tag: '바삭한 식감' },
    { rank: '5위', name: '스팸마요덮밥', icon: '🍱', tag: '간편한 맛' }
  ]},
  
  // 랭킹 카드
  { title: '🏆 분식 TOP7', id: 'ranking', type: 'ranking', rank: 'TOP', items: [
    { name: '분식 랭킹 보기', icon: '🍜', tag: '🏆 인기 순위' }
  ]},
  
  { title: '🍔 패스트푸드', id: 'fastfood', type: 'menu', items: [
    { rank: '1위', name: '불고기버거', icon: '🍔', tag: '빠른 만족' },
    { rank: '2위', name: '치킨버거', icon: '🍔', tag: '바삭한 즐거움' },
    { rank: '3위', name: '더블치즈버거', icon: '🍔', tag: '진한 치즈' },
    { rank: '4위', name: '새우버거', icon: '🍔', tag: '신선한 맛' },
    { rank: '5위', name: '베이컨버거', icon: '🍔', tag: '고소한 베이컨' }
  ]},
  
  // 쿠팡 광고 카드
  { title: '🥡 도시락통', id: 'coupang', type: 'coupang', rank: 'AD', items: [
    { name: '보온도시락 1위', icon: '🥡', tag: '🛒 쿠팡 베스트셀러' }
  ]},
  
  { title: '🍛 일식', id: 'japanese', type: 'menu', items: [
    { rank: '1위', name: '모듬초밥', icon: '🍣', tag: '정갈한 맛' },
    { rank: '2위', name: '돈카츠', icon: '🍛', tag: '바삭한 식감' },
    { rank: '3위', name: '우동', icon: '🍜', tag: '따뜻한 국물' },
    { rank: '4위', name: '연어덮밥', icon: '🍣', tag: '신선한 연어' },
    { rank: '5위', name: '규동', icon: '🍛', tag: '달콤한 소스' }
  ]},
  
  // 랭킹 카드
  { title: '🏆 패스트푸드 TOP7', id: 'ranking', type: 'ranking', rank: 'TOP', items: [
    { name: '패스트푸드 랭킹', icon: '🍔', tag: '🏆 인기 순위' }
  ]},
  
  { title: '🍝 양식', id: 'western', type: 'menu', items: [
    { rank: '1위', name: '크림파스타', icon: '🍝', tag: '이국적 향연' },
    { rank: '2위', name: '토마토파스타', icon: '🍝', tag: '새콤달콤' },
    { rank: '3위', name: '피자', icon: '🍕', tag: '치즈의 향연' },
    { rank: '4위', name: '오일파스타', icon: '🍝', tag: '깔끔한 맛' },
    { rank: '5위', name: '라자냐', icon: '🧀', tag: '진한 치즈' }
  ]},
  
  // 쿠팡 광고 카드
  { title: '🥢 초밥도구', id: 'coupang', type: 'coupang', rank: 'AD', items: [
    { name: '초밥틀 세트 1위', icon: '🥢', tag: '🛒 쿠팡 베스트셀러' }
  ]},
  
  { title: '🍦 디저트', id: 'dessert', type: 'menu', items: [
    { rank: '1위', name: '아이스크림', icon: '🍦', tag: '달콤한 유혹' },
    { rank: '2위', name: '케이크', icon: '🍰', tag: '특별한 순간' },
    { rank: '3위', name: '마카롱', icon: '🧁', tag: '프랑스 감성' },
    { rank: '4위', name: '붕어빵', icon: '🧁', tag: '겨울 간식' },
    { rank: '5위', name: '호떡', icon: '🥞', tag: '따뜻한 달콤함' }
  ]},
  
  // 랭킹 카드
  { title: '🏆 일식 TOP7', id: 'ranking', type: 'ranking', rank: 'TOP', items: [
    { name: '일식 랭킹 보기', icon: '🍣', tag: '🏆 인기 순위' }
  ]},
  
  { title: '🍲 중식', id: 'chinese', type: 'menu', items: [
    { rank: '1위', name: '짜장면', icon: '🍜', tag: '진한 풍미' },
    { rank: '2위', name: '짬뽕', icon: '🍲', tag: '매콤한 국물' },
    { rank: '3위', name: '탕수육', icon: '🥘', tag: '새콤달콤' },
    { rank: '4위', name: '양장피', icon: '🥗', tag: '시원한 맛' },
    { rank: '5위', name: '마파두부', icon: '🌶️', tag: '매운맛의 진수' }
  ]},
  
  // 쿠팡 광고 카드
  { title: '🧂 양념통', id: 'coupang', type: 'coupang', rank: 'AD', items: [
    { name: '만능 양념 1위', icon: '🧂', tag: '🛒 쿠팡 베스트셀러' }
  ]},
  
  { title: '🌙 야식', id: 'latenight', type: 'menu', items: [
    { rank: '1위', name: '치킨', icon: '🍗', tag: '밤의 위로' },
    { rank: '2위', name: '피자', icon: '🍕', tag: '늦은 배고픔' },
    { rank: '3위', name: '족발', icon: '🦶', tag: '쫄깃한 식감' },
    { rank: '4위', name: '보쌈', icon: '🥬', tag: '담백한 맛' },
    { rank: '5위', name: '곱창', icon: '🌭', tag: '고소한 내장' }
  ]},
  
  // 랭킹 카드
  { title: '🏆 양식 TOP7', id: 'ranking', type: 'ranking', rank: 'TOP', items: [
    { name: '양식 랭킹 보기', icon: '🍝', tag: '🏆 인기 순위' }
  ]},
  
  { title: '🥣 국물', id: 'soup', type: 'menu', items: [
    { rank: '1위', name: '김치찌개', icon: '🍲', tag: '따뜻한 온기' },
    { rank: '2위', name: '된장찌개', icon: '🍲', tag: '구수한 맛' },
    { rank: '3위', name: '부대찌개', icon: '🍲', tag: '얼큰한 국물' },
    { rank: '4위', name: '순두부찌개', icon: '🍲', tag: '부드러운 식감' },
    { rank: '5위', name: '미역국', icon: '🥣', tag: '깔끔한 맛' }
  ]},
  
  // 쿠팡 광고 카드
  { title: '📱 전자레인지', id: 'coupang', type: 'coupang', rank: 'AD', items: [
    { name: '전자레인지 1위', icon: '📱', tag: '🛒 쿠팡 베스트셀러' }
  ]},
  
  // 랭킹 카드
  { title: '🏆 디저트 TOP7', id: 'ranking', type: 'ranking', rank: 'TOP', items: [
    { name: '디저트 랭킹 보기', icon: '🍰', tag: '🏆 인기 순위' }
  ]}
];

// 카테고리별 테마 색상
export const CATEGORY_COLORS = {
  chicken: { theme: '#ff6b35', bg: '#fff5f0' },
  meat: { theme: '#e74c3c', bg: '#ffebee' },
  bunsik: { theme: '#f39c12', bg: '#fff8e1' },
  lunchbox: { theme: '#3498db', bg: '#e3f2fd' },
  fastfood: { theme: '#e91e63', bg: '#fce4ec' },
  japanese: { theme: '#9c27b0', bg: '#f3e5f5' },
  western: { theme: '#673ab7', bg: '#ede7f6' },
  dessert: { theme: '#ff9800', bg: '#fff3e0' },
  chinese: { theme: '#4caf50', bg: '#e8f5e8' },
  latenight: { theme: '#607d8b', bg: '#eceff1' },
  soup: { theme: '#795548', bg: '#efebe9' },
  coupang: { theme: '#ffd700', bg: 'linear-gradient(135deg, #ffd700 0%, #ffb300 100%)' },
  ranking: { theme: '#ff5722', bg: 'linear-gradient(135deg, #ff7043 0%, #ff5722 100%)' }
};