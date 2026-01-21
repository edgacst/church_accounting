import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# sal0421 사용자 이메일 확인
cursor.execute("SELECT email FROM auth_user WHERE username = 'sal0421'")
row = cursor.fetchone()
if row:
    sal_email = row[0]
    print(f'sal0421 이메일: {sal_email}')
    
    # 김기철 교인의 이메일을 sal0421 이메일로 업데이트
    cursor.execute("UPDATE members_churchmember SET email = ? WHERE member_id = '001'", (sal_email,))
    conn.commit()
    print(f'✓ 김기철 교인의 이메일을 {sal_email}로 변경했습니다.')
    
    # 확인
    cursor.execute("SELECT korean_name, email FROM members_churchmember WHERE member_id = '001'")
    row = cursor.fetchone()
    print(f'확인: {row[0]} - {row[1]}')
else:
    print('sal0421 사용자를 찾을 수 없습니다.')

conn.close()
