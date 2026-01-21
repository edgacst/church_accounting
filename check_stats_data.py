import sqlite3
from datetime import datetime

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

year = 2026

print(f'=== {year}년 헌금 데이터 ===')
cursor.execute('''
    SELECT strftime('%m', offering_date) as month, COUNT(*), SUM(amount)
    FROM offerings_offering
    WHERE strftime('%Y', offering_date) = ?
    GROUP BY month
    ORDER BY month
''', (str(year),))

offerings = cursor.fetchall()
if offerings:
    for row in offerings:
        print(f'{row[0]}월: {row[1]}건, {int(row[2]):,}원')
else:
    print('헌금 데이터 없음')

print(f'\n=== {year}년 지출 데이터 (승인됨) ===')
cursor.execute('''
    SELECT strftime('%m', transaction_date) as month, COUNT(*), SUM(amount)
    FROM budget_budgettransaction
    WHERE strftime('%Y', transaction_date) = ? AND status = 'approved'
    GROUP BY month
    ORDER BY month
''', (str(year),))

expenses = cursor.fetchall()
if expenses:
    for row in expenses:
        print(f'{row[0]}월: {row[1]}건, {int(row[2]):,}원')
else:
    print('지출 데이터 없음')

print(f'\n=== 헌금 유형별 ===')
cursor.execute('''
    SELECT ot.name, COUNT(o.id), SUM(o.amount)
    FROM offerings_offering o
    JOIN offerings_offeringtype ot ON o.offering_type_id = ot.id
    WHERE strftime('%Y', o.offering_date) = ?
    GROUP BY ot.id
''', (str(year),))

types = cursor.fetchall()
if types:
    for row in types:
        print(f'{row[0]}: {row[1]}건, {int(row[2]):,}원')
else:
    print('헌금 유형 데이터 없음')

conn.close()
