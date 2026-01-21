import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

print('=== 교인 데이터 ===')
cursor.execute('SELECT id, member_id, korean_name, email FROM members_churchmember ORDER BY id')
rows = cursor.fetchall()
for row in rows:
    print(f'ID:{row[0]} | 교인번호:{row[1]} | 이름:{row[2]} | 이메일:{row[3]}')

print(f'\n총 {len(rows)}명의 교인')

conn.close()
