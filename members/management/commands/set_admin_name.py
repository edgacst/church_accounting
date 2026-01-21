from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Set the admin user's name to '최고관리자' (last_name+first_name)"

    def handle(self, *args, **options):
        User = get_user_model()
        try:
            admin = User.objects.filter(is_superuser=True, username='admin').first()
            if admin:
                admin.last_name = '최고'
                admin.first_name = '관리자'
                admin.save()
                self.stdout.write(self.style.SUCCESS("Admin user's name updated to '최고관리자'"))
            else:
                self.stdout.write(self.style.ERROR("Admin user with username 'admin' not found."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))