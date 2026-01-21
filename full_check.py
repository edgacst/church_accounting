import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

print('=== 모든 교인의 이메일 확인 ===')
cursor.execute('SELECT id, member_id, korean_name, email FROM members_churchmember ORDER BY id')
members = cursor.fetchall()

for m in members:
    print(f'ID:{m[0]:2d} | 교인번호:{m[1]:6s} | 이름:{m[2]:10s} | 이메일:{m[3]}')

# 중복 이메일 체크
print('\n=== 중복 이메일 체크 ===')
cursor.execute('''
    SELECT email, COUNT(*) as cnt, GROUP_CONCAT(korean_name) as names
    FROM members_churchmember
    GROUP BY email
    HAVING COUNT(*) > 1
''')

duplicates = cursor.fetchall()
if duplicates:
    print('⚠️ 중복된 이메일 발견!')
    for d in duplicates:
        print(f'이메일: {d[0]} → {d[1]}명 ({d[2]})')
else:
    print('✅ 중복 없음')

print('\n=== 모든 사용자 계정 ===')
cursor.execute('SELECT id, username, email, is_staff FROM auth_user ORDER BY id')
users = cursor.fetchall()

for u in users:
    staff = '관리자' if u[3] else '일반'
    print(f'ID:{u[0]} | username:{u[1]:15s} | email:{u[2]:30s} | {staff}')

conn.close()
