import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

print('=== 모든 사용자 ===')
cursor.execute('SELECT id, username, email, is_active FROM auth_user')
for row in cursor.fetchall():
    print(f'ID:{row[0]} | {row[1]} | {row[2]} | 활성:{row[3]}')

# sal0421 완전 삭제
cursor.execute("DELETE FROM auth_user WHERE username = 'sal0421'")
conn.commit()

print('\n✓ sal0421 사용자 삭제 완료!')

print('\n=== 삭제 후 사용자 목록 ===')
cursor.execute('SELECT id, username, email FROM auth_user')
for row in cursor.fetchall():
    print(f'ID:{row[0]} | {row[1]} | {row[2]}')

conn.close()
