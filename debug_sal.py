import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

print('=== 사용자 정보 ===')
cursor.execute("SELECT username, email FROM auth_user WHERE username = 'sal0421'")
row = cursor.fetchone()
if row:
    print(f'sal0421 이메일: {row[1]}')
    
    print('\n=== 교인 정보 ===')
    cursor.execute("SELECT id, member_id, korean_name, email FROM members_churchmember")
    for r in cursor.fetchall():
        print(f'ID:{r[0]} | {r[1]} | {r[2]} | {r[3]}')
        if r[3] == row[1]:
            print('  ↑ sal0421과 일치!')

conn.close()
