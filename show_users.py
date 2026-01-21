import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

print('=== 사용자 계정 데이터 ===')
cursor.execute('SELECT id, username, email, is_staff, is_superuser FROM auth_user ORDER BY id')
rows = cursor.fetchall()
for row in rows:
    print(f'ID:{row[0]} | 사용자명:{row[1]} | 이메일:{row[2]} | staff:{row[3]} | superuser:{row[4]}')

print(f'\n총 {len(rows)}명의 사용자')

conn.close()
