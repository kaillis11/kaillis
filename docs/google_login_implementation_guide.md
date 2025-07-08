# 🔐 Google 로그인 구현 가이드 - WhatToEat

**작성일**: 2025-07-05  
**작성자**: 오로라  
**목적**: HTML 웹앱에 구글 로그인 기능 추가

---

## 🎯 구현 목표

1. **구글 로그인 버튼** 추가
2. **사용자 정보 저장** (이름, 이메일, 프로필 사진)
3. **MBTI 정보 연동**
4. **개인화된 룰렛 설정 저장**

---

## 🛠️ 구현 단계

### **1단계: Google Cloud Console 설정**

1. [Google Cloud Console](https://console.cloud.google.com) 접속
2. 새 프로젝트 생성: "WhatToEat-App"
3. APIs & Services → Credentials 이동
4. "Create Credentials" → "OAuth client ID" 선택
5. Application type: "Web application"
6. Authorized JavaScript origins:
   - `http://localhost`
   - `http://localhost:8080`
   - `https://YOUR-DOMAIN.com` (나중에 추가)
7. Client ID 복사 저장

### **2단계: HTML에 Google Sign-In 추가**

```html
<!-- Google Sign-In 라이브러리 -->
<script src="https://accounts.google.com/gsi/client" async defer></script>

<!-- 로그인 버튼 영역 -->
<div id="google-signin-button"></div>

<!-- 사용자 정보 표시 영역 -->
<div id="user-info" style="display: none;">
  <img id="user-avatar" src="" alt="프로필" style="width: 40px; height: 40px; border-radius: 50%;">
  <span id="user-name"></span>
  <button onclick="signOut()">로그아웃</button>
</div>
```

### **3단계: JavaScript 구현**

```javascript
// Google 로그인 초기화
function initializeGoogleSignIn() {
  google.accounts.id.initialize({
    client_id: 'YOUR_CLIENT_ID.apps.googleusercontent.com',
    callback: handleCredentialResponse,
    auto_select: true,
    cancel_on_tap_outside: false
  });

  // 로그인 버튼 렌더링
  google.accounts.id.renderButton(
    document.getElementById("google-signin-button"),
    { 
      theme: "outline", 
      size: "large",
      text: "signin_with",
      shape: "rectangular",
      logo_alignment: "left"
    }
  );

  // 자동 로그인 프롬프트
  google.accounts.id.prompt();
}

// 로그인 성공 처리
function handleCredentialResponse(response) {
  // JWT 토큰 디코딩
  const responsePayload = decodeJwtResponse(response.credential);
  
  // 사용자 정보 저장
  const userInfo = {
    id: responsePayload.sub,
    name: responsePayload.name,
    email: responsePayload.email,
    picture: responsePayload.picture
  };
  
  // 로컬 스토리지에 저장
  localStorage.setItem('userInfo', JSON.stringify(userInfo));
  
  // UI 업데이트
  displayUserInfo(userInfo);
  
  // MBTI 정보 확인
  checkUserMBTI(userInfo.id);
}

// JWT 디코딩 함수
function decodeJwtResponse(token) {
  const base64Url = token.split('.')[1];
  const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
  const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
    return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
  }).join(''));
  return JSON.parse(jsonPayload);
}

// 사용자 정보 표시
function displayUserInfo(userInfo) {
  document.getElementById('google-signin-button').style.display = 'none';
  document.getElementById('user-info').style.display = 'flex';
  document.getElementById('user-avatar').src = userInfo.picture;
  document.getElementById('user-name').textContent = userInfo.name;
}

// 로그아웃
function signOut() {
  google.accounts.id.disableAutoSelect();
  localStorage.removeItem('userInfo');
  localStorage.removeItem('userMBTI');
  localStorage.removeItem('userRouletteSettings');
  location.reload();
}

// 페이지 로드시 실행
window.onload = function() {
  initializeGoogleSignIn();
  
  // 기존 로그인 정보 확인
  const savedUser = localStorage.getItem('userInfo');
  if (savedUser) {
    displayUserInfo(JSON.parse(savedUser));
  }
};
```

### **4단계: MBTI 연동**

```javascript
// MBTI 정보 관리
function checkUserMBTI(userId) {
  const savedMBTI = localStorage.getItem('userMBTI');
  
  if (!savedMBTI) {
    // MBTI 입력 모달 표시
    showMBTIModal();
  } else {
    // 기존 MBTI 정보로 룰렛 개인화
    personalizeRoulette(savedMBTI);
  }
}

// MBTI 입력 모달
function showMBTIModal() {
  const modal = document.createElement('div');
  modal.innerHTML = `
    <div class="mbti-modal">
      <h2>MBTI를 알려주세요!</h2>
      <p>더 정확한 메뉴 추천을 위해 필요해요 😊</p>
      <select id="mbti-select">
        <option value="">선택하세요</option>
        <option value="INTJ">INTJ - 용의주도한 전략가</option>
        <option value="INTP">INTP - 논리적인 사색가</option>
        <option value="ENTJ">ENTJ - 대담한 통솔자</option>
        <option value="ENTP">ENTP - 논쟁을 즐기는 변론가</option>
        <option value="INFJ">INFJ - 선의의 옹호자</option>
        <option value="INFP">INFP - 열정적인 중재자</option>
        <option value="ENFJ">ENFJ - 정의로운 사회운동가</option>
        <option value="ENFP">ENFP - 재기발랄한 활동가</option>
        <option value="ISTJ">ISTJ - 청렴결백한 논리주의자</option>
        <option value="ISFJ">ISFJ - 용감한 수호자</option>
        <option value="ESTJ">ESTJ - 엄격한 관리자</option>
        <option value="ESFJ">ESFJ - 사교적인 외교관</option>
        <option value="ISTP">ISTP - 만능 재주꾼</option>
        <option value="ISFP">ISFP - 호기심 많은 예술가</option>
        <option value="ESTP">ESTP - 모험을 즐기는 사업가</option>
        <option value="ESFP">ESFP - 자유로운 연예인</option>
      </select>
      <button onclick="saveMBTI()">저장</button>
      <button onclick="skipMBTI()">나중에</button>
    </div>
  `;
  document.body.appendChild(modal);
}

// MBTI 저장
function saveMBTI() {
  const mbti = document.getElementById('mbti-select').value;
  if (mbti) {
    localStorage.setItem('userMBTI', mbti);
    personalizeRoulette(mbti);
    closeModal();
  }
}
```

### **5단계: 개인화 룰렛 설정**

```javascript
// 룰렛 개인화
function personalizeRoulette(mbti) {
  const userSettings = {
    mbti: mbti,
    hiddenMenus: [], // 숨긴 메뉴들
    favoriteMenus: [], // 즐겨찾기
    lastUpdate: new Date().toISOString()
  };
  
  localStorage.setItem('userRouletteSettings', JSON.stringify(userSettings));
  
  // 룰렛 UI 업데이트
  updateRouletteWithUserSettings(userSettings);
}

// X 버튼으로 메뉴 제거
function removeMenuItem(menuId) {
  const settings = JSON.parse(localStorage.getItem('userRouletteSettings') || '{}');
  
  if (!settings.hiddenMenus) {
    settings.hiddenMenus = [];
  }
  
  settings.hiddenMenus.push(menuId);
  localStorage.setItem('userRouletteSettings', JSON.stringify(settings));
  
  // 데이터 수집 (익명화)
  collectUserPreference({
    mbti: settings.mbti,
    action: 'remove',
    menuId: menuId,
    timestamp: new Date().toISOString()
  });
  
  // UI에서 제거
  document.getElementById(menuId).style.display = 'none';
}
```

---

## 🔒 보안 고려사항

1. **Client ID만 노출** (Secret은 서버에만)
2. **HTTPS 필수** (프로덕션 환경)
3. **개인정보는 로컬 스토리지**에만 저장
4. **데이터 수집시 익명화** 처리

---

## 📱 모바일 대응

```css
/* 구글 로그인 버튼 모바일 스타일 */
@media (max-width: 767px) {
  #google-signin-button {
    width: 100%;
    max-width: 300px;
    margin: 0 auto;
  }
  
  #user-info {
    position: fixed;
    top: 10px;
    right: 10px;
    background: white;
    padding: 5px;
    border-radius: 20px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  }
}
```

---

## 🚀 다음 단계

1. **Google Cloud Console**에서 OAuth 2.0 설정
2. **Client ID** 발급 받기
3. **HTML 파일**에 위 코드 통합
4. **테스트** 및 디버깅
5. **데이터 수집 백엔드** 구축 (Firebase 또는 custom)

---

## 💡 참고사항

- 구글 로그인은 **localhost**에서도 테스트 가능
- 실제 배포시 **도메인 추가** 필요
- **One Tap** 기능으로 로그인 편의성 극대화
- MBTI 데이터는 **선택사항**으로 처리

---

이 가이드를 따라 구현하면 구글 로그인 + MBTI 연동 + 개인화 룰렛이 완성됩니다! 🎉