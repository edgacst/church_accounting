import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

print('=== 변경 전 ===')
cursor.execute('SELECT id, member_id, korean_name, email FROM members_churchmember ORDER BY id')
for row in cursor.fetchall():
    print(f'{row[2]:10s} | 이메일: {row[3]}')

# 이메일 교환
# 김기철: sal0421@gmail.com → admin@church.local
# 이승아: admin@church.local → sal0421@gmail.com

cursor.execute('UPDATE members_churchmember SET email = ? WHERE member_id = ?', ('admin@church.local', '001'))
cursor.execute('UPDATE members_churchmember SET email = ? WHERE member_id = ?', ('sal0421@gmail.com', '000002'))

conn.commit()

print('\n=== 변경 후 ===')
cursor.execute('SELECT id, member_id, korean_name, email FROM members_churchmember ORDER BY id')
for row in cursor.fetchall():
    print(f'{row[2]:10s} | 이메일: {row[3]}')

print('\n✅ 연결 확인:')
print('sal0421 (sal0421@gmail.com) → 이승아')
print('admin (admin@church.local) → 김기철')

conn.close()
