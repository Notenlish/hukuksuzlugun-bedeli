import sqlite3

con = sqlite3.connect("db.sqlite3")
cur = con.cursor()

result = cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
li = result.fetchall()
print(li)
result = cur.execute("SELECT * FROM trackedmetric")
print(result.fetchall())