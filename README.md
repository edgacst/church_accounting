# 교회 재정 관리 시스템

Django 기반 교회 재정 관리 시스템입니다.

## 주요 기능

- 👥 **교인 관리**: 교인 정보 등록 및 관리
- 💰 **헌금 관리**: 헌금 입력, 조회, 세금계산서 발급
- 📊 **예산 관리**: 연간 예산 수립 및 지출 승인 시스템
- 📝 **지출 신청**: 부서별 지출 신청 및 결재 프로세스

## 설치 방법

### 1. 필요한 프로그램 설치
- Python 3.8 이상
- pip (Python 패키지 관리자)

### 2. 프로젝트 설정

```bash
# 가상환경 생성 (선택사항이지만 권장)
python -m venv venv

# 가상환경 활성화
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 필요한 패키지 설치
pip install django python-decouple

# 데이터베이스 설정
python manage.py migrate

# 관리자 계정 생성
python manage.py createsuperuser
```

### 3. 환경 설정 파일 생성

`.env.example` 파일을 복사하여 `.env` 파일을 만들고, 설정값을 입력하세요.

```bash
# Windows
copy .env.example .env

# Mac/Linux
cp .env.example .env
```

`.env` 파일에서 다음 값들을 수정하세요:
- `SECRET_KEY`: 새로운 비밀키 생성
- `DEBUG`: 개발 시 True, 운영 시 False
- `ALLOWED_HOSTS`: 실제 도메인 주소 입력

### 4. 서버 실행

```bash
python manage.py runserver
```

웹브라우저에서 http://localhost:8000 접속

## 보안 주의사항

⚠️ **중요**: 다음 파일들은 절대 공유하거나 업로드하지 마세요!
- `.env` - 비밀키와 설정 정보 포함
- `db.sqlite3` - 실제 데이터베이스 파일
- `media/` - 업로드된 파일들

## 배포 전 체크리스트

실제 서비스를 시작하기 전에 확인하세요:

- [ ] `.env` 파일에서 `DEBUG=False` 설정
- [ ] `ALLOWED_HOSTS`에 실제 도메인 추가
- [ ] 새로운 `SECRET_KEY` 생성
- [ ] 데이터베이스 백업 체계 구축
- [ ] HTTPS 인증서 설정
- [ ] 정기적인 백업 계획 수립

## 기술 스택

- **Backend**: Django 4.x
- **Database**: SQLite (개발용), PostgreSQL/MySQL 권장 (운영용)
- **Python**: 3.8+

## 라이선스

내부 사용 목적
