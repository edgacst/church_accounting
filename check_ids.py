import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

print('=== 교인 목록 (ID 순) ===')
cursor.execute('SELECT id, member_id, korean_name, email FROM members_churchmember ORDER BY id')
for row in cursor.fetchall():
    print(f'ID:{row[0]} | {row[1]} | {row[2]} | {row[3]}')

print('\n=== 사용자 목록 ===')
cursor.execute('SELECT username, email FROM auth_user')
for row in cursor.fetchall():
    print(f'{row[0]} | {row[1]}')

conn.close()
