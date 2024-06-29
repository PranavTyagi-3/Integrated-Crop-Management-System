import sqlite3

conn = sqlite3.connect('database.db')
cur = conn.cursor()

cur.execute('''
UPDATE records set yield=1200 where recordId=7''')

conn.commit()