# Kitties

고양이 사진을 자유롭게 올리는 사이트입니다.

## 기능

- 태그를 이용해서 사진을 검색할 수 있습니다.
- 사진에 좋아요를 누를 수 있습니다. 사진은 좋아요 순서대로 사용자에게 먼저 보여집니다.
- 사진을 업로드하고, 태그와 비밀번호를 지정할 수 있습니다.
- 비밀번호를 이용해서 사진을 지울 수 있습니다.
- 사진을 다운로드 받을 수 있습니다.

## API 구조

### Image 관련

- POST `/image` -> 이미지를 업로드 합니다.
- PUT `/image` -> 이미지를 수정합니다.
- DELETE `/image/:filename` -> 이미지를 삭제합니다.
- GET `/image/:filename` -> 이미지를 브라우저로 보냅니다.
- GET `/image/:filename/download` -> 이미지를 다운로드 할 수 있게 보냅니다.

### Like 관련

- POST `/image/:filename/like` -> 세션 기반으로 좋아요를 추적하고, DB에 좋아요 수를 반영합니다.
- POST `/image/:filename/dislike` -> 세션에서 좋아요를 삭제하고, DB에 좋아요 수를 반영합니다.

### tag 관련

- GET `/` -> 고양이 사진이 나오는 홈 페이지입니다.
- GET `/search/:tag` -> 고양이 사진을 태그 기반으로 검색합니다.

## 기술

- Flask: 경량 웹 프레임워크입니다.
- MongoDB: 도큐먼트 기반 NoSQL Database System 입니다.
- HTML, CSS, JS: 사용자 인터페이스를 구축하기 위한 웹 기술입니다.

## 패키지 구조

```
📁 프로젝트 루트 디렉토리 (Flask 기반 "kitties" 웹사이트)
├── 📁 static                 # 정적 파일 (CSS, JS, 이미지 등) 저장 폴더
│   ├── 📁 styles             # 스타일(CSS) 파일을 저장하는 폴더
│   └── 📁 js                 # JavaScript 파일을 저장하는 폴더
├── 📁 templates              # HTML 템플릿을 저장하는 폴더 (Flask의 Jinja2 템플릿 엔진 사용)
│   └── index.html            # 웹사이트의 메인 페이지
├── app.py                    # Flask 애플리케이션의 메인 엔트리 파일
├── getcats                   # 양이 이미지를 가져오는 스크립트
├── note.ipynb                # pymongo 연습용 파일
├── requirements.txt          # 프로젝트 의존성 목록 (pip install -r requirements.txt 로 설치 가능)
├── README.md                 # 프로젝트 설명 및 사용법이 포함된 문서
```

## 실행 방법

**1. Clone repository**

```
git clone https://github.com/AlpacaMale/kitties
```

**2. Change directory**

```
cd kitties
```

**3. Install dependency**

```
pip install -r requirements.txt
```

**4. Set up environment**

```
MONGODB_URL='mongodb://host:port/'
SECRET_KEY="your-secret-key"
ADMIN_PASSWD="your-password"
```

**5. Run flask server**

```
flask run
```

## 스크린샷

![kitties site screenshot](/overview.bmp)
