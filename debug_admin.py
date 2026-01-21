import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

print('=== admin 사용자 정보 ===')
cursor.execute("SELECT username, email FROM auth_user WHERE username = 'admin'")
row = cursor.fetchone()
if row:
    print(f'admin 이메일: {row[1]}')
    
    print('\n=== 교인 정보 ===')
    cursor.execute("SELECT id, member_id, korean_name, email FROM members_churchmember")
    for r in cursor.fetchall():
        print(f'ID:{r[0]} | {r[1]} | {r[2]} | {r[3]}')
        if r[3] == row[1]:
            print('  ↑ admin과 일치!')
    
    # 이승아의 이메일이 admin@church.local인지 확인
    cursor.execute("SELECT email FROM members_churchmember WHERE korean_name = '이승아'")
    lee_row = cursor.fetchone()
    if lee_row:
        print(f'\n이승아 이메일: {lee_row[0]}')
        print(f'admin 이메일: {row[1]}')
        print(f'일치 여부: {lee_row[0] == row[1]}')

conn.close()
