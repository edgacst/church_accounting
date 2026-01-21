from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = '관리자(admin) 계정을 자동으로 생성합니다.'

    def handle(self, *args, **options):
        User = get_user_model()
        username = 'admin'
        email = 'admin@example.com'
        password = 'admin1234'
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            self.stdout.write(self.style.SUCCESS(f"슈퍼유저({username}) 생성 완료!"))
        else:
            self.stdout.write(self.style.WARNING(f"이미 {username} 계정이 존재합니다."))
