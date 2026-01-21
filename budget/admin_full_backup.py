from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.conf import settings
import os
import shutil
import zipfile
import tempfile
from io import BytesIO

@staff_member_required
def backup_db_and_media(request):
    db_path = os.path.join(settings.BASE_DIR, 'db.sqlite3')
    media_root = getattr(settings, 'MEDIA_ROOT', None)
    if not os.path.exists(db_path):
        return HttpResponse('DB 파일이 존재하지 않습니다.', status=404)
    with tempfile.TemporaryDirectory() as tmpdir:
        db_copy = os.path.join(tmpdir, 'db.sqlite3')
        shutil.copy2(db_path, db_copy)
        media_copy = os.path.join(tmpdir, 'media')
        if media_root and os.path.exists(media_root):
            shutil.copytree(media_root, media_copy)
        else:
            os.mkdir(media_copy)
        mem_zip = BytesIO()
        with zipfile.ZipFile(mem_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(db_copy, 'db.sqlite3')
            for root, dirs, files in os.walk(media_copy):
                for file in files:
                    abs_path = os.path.join(root, file)
                    rel_path = os.path.relpath(abs_path, tmpdir)
                    zipf.write(abs_path, rel_path)
            if not any(os.scandir(media_copy)):
                zipf.write(media_copy, 'media/')
        mem_zip.seek(0)
        response = HttpResponse(mem_zip.read(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="church_backup.zip"'
        return response
