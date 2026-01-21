import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# 김기철 이메일 변경
cursor.execute("UPDATE members_churchmember SET email = 'sal0421@gmail.com' WHERE member_id = '001'")
conn.commit()

print('✓ 김기철 이메일 변경 완료!')

# 확인
cursor.execute('SELECT korean_name, email FROM members_churchmember WHERE member_id = "001"')
row = cursor.fetchone()
print(f'확인: {row[0]} - {row[1]}')

conn.close()
