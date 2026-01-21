import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# offerings_offering 테이블 구조 확인
print('=== offerings_offering 테이블 구조 ===')
cursor.execute('PRAGMA table_info(offerings_offering)')
for row in cursor.fetchall():
    print(f'{row[1]} ({row[2]})')

conn.close()
