import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

print('=== 사용자 목록 ===')
cursor.execute('SELECT username, email FROM auth_user')
for row in cursor.fetchall():
    print(f'{row[0]} - {row[1]}')

print('\n=== 교인 목록 ===')
cursor.execute('SELECT member_id, korean_name, email FROM members_churchmember ORDER BY id')
for row in cursor.fetchall():
    print(f'{row[0]} | {row[1]} - {row[2]}')

print('\n=== 매핑 확인 ===')
cursor.execute('''
    SELECT u.username, u.email as user_email, m.korean_name, m.email as member_email
    FROM auth_user u
    LEFT JOIN members_churchmember m ON u.email = m.email
''')
for row in cursor.fetchall():
    if row[2]:
        print(f'{row[0]} ({row[1]}) → {row[2]} ({row[3]})')
    else:
        print(f'{row[0]} ({row[1]}) → 연결 안됨')

conn.close()
