from django.contrib.admin.views.decorators import staff_member_required
from django.http import FileResponse, HttpResponse
from django.conf import settings
import os

@staff_member_required
def backup_sqlite_db(request):
    db_path = os.path.join(settings.BASE_DIR, 'db.sqlite3')
    if os.path.exists(db_path):
        response = FileResponse(open(db_path, 'rb'), as_attachment=True, filename='db.sqlite3')
        return response
    return HttpResponse('DB 파일이 존재하지 않습니다.', status=404)
