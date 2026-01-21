import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# sal0421 사용자 정보
print('=== sal0421 사용자 정보 ===')
cursor.execute('SELECT id, username, email FROM auth_user WHERE username = "sal0421"')
user = cursor.fetchone()
print(f'ID:{user[0]} | username:{user[1]} | email:{user[2]}')

username = user[1]
email = user[2]

# 이 사용자로 찾아지는 교인 (views.py의 쿼리와 동일)
print(f'\n=== ChurchMember 검색 (email={email} OR korean_name={username}) ===')
cursor.execute('''
    SELECT id, member_id, korean_name, email 
    FROM members_churchmember 
    WHERE email = ? OR korean_name = ?
    ORDER BY id
''', (email, username))

members = cursor.fetchall()
for m in members:
    print(f'ID:{m[0]} | 교인번호:{m[1]} | 이름:{m[2]} | 이메일:{m[3]}')

print(f'\n총 {len(members)}명 검색됨')
if members:
    first_member = members[0]
    print(f'\n.first() 결과: {first_member[2]} ({first_member[1]})')
    
    # 이 교인의 헌금 내역
    print(f'\n=== {first_member[2]}의 헌금 내역 ===')
    cursor.execute('''
        SELECT id, offering_date, amount 
        FROM offerings_offering 
        WHERE member_id = ?
        ORDER BY offering_date DESC
    ''', (first_member[0],))
    
    offerings = cursor.fetchall()
    for o in offerings:
        print(f'날짜:{o[1]} | 금액:{o[2]:,}원')
    
    if offerings:
        total = sum(o[2] for o in offerings)
        print(f'합계: {total:,}원')

conn.close()
