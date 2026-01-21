import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

print('=== 사용자 정보 ===')
cursor.execute('SELECT username, email, is_staff, is_superuser FROM auth_user')
for row in cursor.fetchall():
    print(f'{row[0]} | {row[1]} | staff={row[2]} | super={row[3]}')

print('\n=== 교인 정보 ===')
cursor.execute('SELECT id, member_id, korean_name, email, tax_issuance_consent FROM members_churchmember')
for row in cursor.fetchall():
    print(f'ID:{row[0]} | {row[1]} | {row[2]} | {row[3]} | 동의={row[4]}')

conn.close()
