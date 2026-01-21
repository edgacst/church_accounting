import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

print('=== 교인 목록 ===')
cursor.execute('SELECT member_id, korean_name, email, offering_number FROM members_churchmember')
for row in cursor.fetchall():
    print(f'{row[0]} | {row[1]} | {row[2]} | 봉투:{row[3]}')

print('\n=== 헌금 목록 ===')
cursor.execute('''
    SELECT m.korean_name, ot.name, o.amount, o.offering_date
    FROM offerings_offering o
    JOIN members_churchmember m ON o.member_id = m.id
    JOIN offerings_offeringtype ot ON o.offering_type_id = ot.id
''')
for row in cursor.fetchall():
    print(f'{row[0]} | {row[1]} | {row[2]}원 | {row[3]}')

conn.close()
