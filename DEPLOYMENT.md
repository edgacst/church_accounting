# 프로덕션 배포 가이드

## 🌐 배포된 사이트
- **URL**: http://edga.pythonanywhere.com
- **호스팅**: PythonAnywhere

## 🚀 배포 전 체크리스트

### 1. 환경 변수 설정
`.env` 파일을 생성하고 다음 값들을 설정하세요:

```bash
SECRET_KEY=매우-복잡한-랜덤-문자열-50자-이상
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

**SECRET_KEY 생성 방법:**
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 2. 정적 파일 수집
```bash
python manage.py collectstatic
```

### 3. 데이터베이스 마이그레이션
```bash
python manage.py migrate
```

### 4. 관리자 계정 생성
```bash
python manage.py createsuperuser
```

---

## 📦 배포 옵션

### Option 1: PythonAnywhere (무료, 초보자 추천)

**장점:**
- 무료 플랜 제공
- Django 특화 호스팅
- 설정이 간단함

**배포 순서:**
1. [PythonAnywhere](https://www.pythonanywhere.com) 가입
2. **Web** 탭에서 **Add a new web app** 클릭
3. **Manual configuration** → **Python 3.14** 선택
4. **Files** 탭에서 프로젝트 업로드 또는 Git clone
5. **Bash console** 열기:
   ```bash
   # 가상환경 생성
   mkvirtualenv --python=/usr/bin/python3.14 myenv
   
   # 프로젝트 디렉토리로 이동
   cd /home/yourusername/church_accounting
   
   # 패키지 설치
   pip install -r requirements.txt
   
   # 정적 파일 수집
   python manage.py collectstatic
   
   # 마이그레이션
   python manage.py migrate
   ```
6. **Web** 탭에서 WSGI 설정:
   - **WSGI configuration file** 클릭
   - Django 섹션 주석 해제 및 경로 수정
   ```python
   import sys
   path = '/home/yourusername/church_accounting'
   if path not in sys.path:
       sys.path.append(path)
   
   os.environ['DJANGO_SETTINGS_MODULE'] = 'church_finance.settings'
   
   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```
7. **Static files** 섹션 설정:
   - URL: `/static/`
   - Directory: `/home/yourusername/church_accounting/staticfiles`
8. **Reload** 버튼 클릭

---

### Option 2: Heroku (유료, 전문가용)

**장점:**
- 자동 배포 (Git push로 배포)
- PostgreSQL 데이터베이스 제공
- SSL 인증서 자동

**배포 순서:**
1. [Heroku](https://www.heroku.com) 가입 및 CLI 설치
2. 프로젝트 루트에 `Procfile` 생성:
   ```
   web: gunicorn church_finance.wsgi
   ```
3. `runtime.txt` 생성:
   ```
   python-3.14.2
   ```
4. requirements.txt에 추가:
   ```
   gunicorn==21.2.0
   psycopg2-binary==2.9.9
   dj-database-url==2.1.0
   whitenoise==6.6.0
   ```
5. settings.py 수정 (Heroku용):
   ```python
   import dj_database_url
   
   DATABASES['default'] = dj_database_url.config(
       default=config('DATABASE_URL')
   )
   
   MIDDLEWARE = [
       'django.middleware.security.SecurityMiddleware',
       'whitenoise.middleware.WhiteNoiseMiddleware',  # 추가
       # ... 나머지
   ]
   ```
6. Heroku 배포:
   ```bash
   heroku login
   heroku create your-app-name
   git push heroku main
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   ```

---

### Option 3: VPS (AWS, DigitalOcean 등)

**장점:**
- 완전한 제어
- 확장성 좋음
- 프로덕션 환경에 적합

**필요한 것:**
- Nginx (웹 서버)
- Gunicorn (WSGI 서버)
- PostgreSQL (데이터베이스)
- Supervisor (프로세스 관리)

**배포 순서:**
1. 서버 접속 및 패키지 설치:
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv nginx postgresql
   ```
2. 프로젝트 클론 및 설정:
   ```bash
   cd /var/www
   git clone your-repo-url church_accounting
   cd church_accounting
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install gunicorn
   ```
3. Gunicorn 설정 (`/etc/systemd/system/church.service`):
   ```ini
   [Unit]
   Description=Church Accounting Gunicorn
   After=network.target
   
   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/var/www/church_accounting
   Environment="PATH=/var/www/church_accounting/venv/bin"
   ExecStart=/var/www/church_accounting/venv/bin/gunicorn \
             --workers 3 \
             --bind unix:/var/www/church_accounting/church.sock \
             church_finance.wsgi:application
   
   [Install]
   WantedBy=multi-user.target
   ```
4. Nginx 설정 (`/etc/nginx/sites-available/church`):
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;
       
       location /static/ {
           alias /var/www/church_accounting/staticfiles/;
       }
       
       location /media/ {
           alias /var/www/church_accounting/media/;
       }
       
       location / {
           proxy_pass http://unix:/var/www/church_accounting/church.sock;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```
5. 서비스 시작:
   ```bash
   sudo systemctl start church
   sudo systemctl enable church
   sudo systemctl restart nginx
   ```

---

## 🔒 보안 체크리스트

- [ ] DEBUG=False 설정
- [ ] SECRET_KEY를 환경 변수로 분리
- [ ] ALLOWED_HOSTS에 도메인 추가
- [ ] HTTPS 인증서 설치 (Let's Encrypt)
- [ ] 데이터베이스 백업 자동화
- [ ] 방화벽 설정 (포트 80, 443만 개방)
- [ ] 관리자 비밀번호 강력하게 설정

---

## 📊 배포 후 확인사항

1. **정적 파일 로딩 확인**
   - CSS, JavaScript, 이미지가 제대로 로드되는지 확인

2. **파일 업로드 테스트**
   - 영수증 이미지 업로드 기능 테스트

3. **PDF 다운로드 테스트**
   - 지출결의서 PDF 생성 확인 (한글 폰트 확인)

4. **권한 테스트**
   - 일반 사용자 / 관리자 권한 분리 확인

5. **성능 모니터링**
   - 응답 속도 확인
   - 에러 로그 확인

---

## 🆘 문제 해결

### 정적 파일이 로드되지 않음
```bash
python manage.py collectstatic --clear
```

### 데이터베이스 연결 오류
```bash
python manage.py migrate --run-syncdb
```

### 500 에러 발생
- DEBUG=True로 임시 설정하여 에러 확인
- 로그 파일 확인 (`/var/log/nginx/error.log`)

### 한글 폰트가 PDF에 안 나옴
- 서버에 Malgun Gothic 폰트 설치 필요
- 또는 NanumGothic 같은 오픈소스 한글 폰트 사용

```bash
# Ubuntu/Debian
sudo apt install fonts-nanum
```

---

## 📞 지원

문제가 발생하면 다음 정보를 확인하세요:
- Django 버전: 6.0.1
- Python 버전: 3.14.2
- 프로젝트 구조: church_finance (메인 앱)
- 앱: members, offerings, budget
