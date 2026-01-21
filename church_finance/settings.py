# --- 슈퍼유저 자동 생성 코드 (임시, 배포 후 반드시 삭제!) ---
import django
from django.contrib.auth import get_user_model
import sys

if 'runserver' in sys.argv or 'gunicorn' in sys.argv:
    try:
        import os
        BASE_DIR = Path(__file__).resolve().parent.parent
        db_path = BASE_DIR / 'db.sqlite3'
        if os.path.exists(db_path):
            os.remove(db_path)
            print('db.sqlite3 파일 삭제 완료 (최초 1회만 사용, 배포 후 반드시 삭제!)')
        django.setup()
        from django.contrib.auth.models import Group
        User = get_user_model()
        # 기존 admin 삭제 및 슈퍼유저 생성
        admin_user = User.objects.filter(username='admin').first()
        if admin_user:
            admin_user.delete()
        User.objects.create_superuser('admin', 'admin@example.com', 'admin1234')
        print('슈퍼유저(admin) 새로 생성 완료')

        # 테스트용 일반 유저 생성 및 권한 부여
        test_user = User.objects.filter(username='testuser').first()
        if test_user:
            test_user.delete()
        test_user = User.objects.create_user('testuser', 'testuser@example.com', 'test1234')
        test_user.is_staff = True  # staff 권한 부여(관리자페이지 접근 가능)
        test_user.save()
        # 그룹(예: testers) 자동 생성 및 추가
        group, created = Group.objects.get_or_create(name='testers')
        test_user.groups.add(group)
        print('테스트유저(testuser) 생성 및 testers 그룹/권한 부여 완료')
    except Exception as e:
        print(f'Superuser/testuser creation skipped: {e}')
from pathlib import Path
from decouple import config, Csv

BASE_DIR = Path(__file__).resolve().parent.parent

# 환경 변수에서 비밀키와 설정 읽어오기
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='', cast=Csv())

# SQLite 데이터베이스
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

## 네이버 메일 SMTP 설정
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.naver.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'freecompr@naver.com'  # 네이버 전체 이메일 주소로 변경
EMAIL_HOST_PASSWORD = 'kim132457!!'   # 네이버 비밀번호로 변경
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'freecompr@naver.com'  # 네이버 전체 이메일 주소로 변경
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',  # 콤마 포맷팅을 위한 humanize 추가
    'members',
    'offerings', 
    'budget',
]
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # 이렇게 변경
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'church_finance.urls'


WSGI_APPLICATION = 'church_finance.wsgi.application'

# 비밀번호 검증 비활성화 (개발 환경)
AUTH_PASSWORD_VALIDATORS = []


LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # 배포 시 정적 파일 모음 위치
STATICFILES_DIRS = [BASE_DIR / 'static'] if (BASE_DIR / 'static').exists() else []

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# 파일 업로드 크기 제한 (10MB)
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/'  # 메인 대시보드
LOGOUT_REDIRECT_URL = 'login'
LOGIN_URL = 'login'

# 세션 설정 - 개발 환경용 단순화
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # 데이터베이스 세션
SESSION_COOKIE_AGE = 86400  # 24시간
SESSION_SAVE_EVERY_REQUEST = True  # 매 요청마다 세션 저장
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SECURE = False  # 개발 환경(HTTP)에서는 False

# CSRF 설정
CSRF_COOKIE_SAMESITE = 'Lax'  
CSRF_COOKIE_SECURE = False  # 개발 환경에서는 False
CSRF_USE_SESSIONS = False
CSRF_COOKIE_HTTPONLY = False  # JavaScript 접근 허용

# 프로덕션 환경 보안 설정 (DEBUG=False일 때만)
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = False  # Railway 환경에서는 무한 리디렉션 방지
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# Railway/Proxy 환경에서 HTTPS 인식
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

