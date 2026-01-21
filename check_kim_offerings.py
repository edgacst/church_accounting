import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# 김기철의 헌금 내역
print('=== 김기철 (member_id=001)의 헌금 내역 ===')
cursor.execute('''
    SELECT o.id, o.offering_date, o.offering_type, o.amount, m.korean_name
    FROM offerings_offering o
    JOIN members_churchmember m ON o.member_id = m.id
    WHERE m.member_id = '001'
    ORDER BY o.offering_date DESC
''')
rows = cursor.fetchall()
for row in rows:
    print(f'ID:{row[0]} | 날짜:{row[1]} | 종류:{row[2]} | 금액:{row[3]:,}원 | 교인:{row[4]}')

if rows:
    total = sum(row[3] for row in rows)
    print(f'\n총 {len(rows)}건, 합계: {total:,}원')
else:
    print('헌금 내역 없음')

# 이승아의 헌금 내역도 확인
print('\n=== 이승아 (member_id=000002)의 헌금 내역 ===')
cursor.execute('''
    SELECT o.id, o.offering_date, o.offering_type, o.amount, m.korean_name
    FROM offerings_offering o
    JOIN members_churchmember m ON o.member_id = m.id
    WHERE m.member_id = '000002'
    ORDER BY o.offering_date DESC
''')
rows2 = cursor.fetchall()
for row in rows2:
    print(f'ID:{row[0]} | 날짜:{row[1]} | 종류:{row[2]} | 금액:{row[3]:,}원 | 교인:{row[4]}')

if rows2:
    total2 = sum(row[3] for row in rows2)
    print(f'\n총 {len(rows2)}건, 합계: {total2:,}원')
else:
    print('헌금 내역 없음')

conn.close()
