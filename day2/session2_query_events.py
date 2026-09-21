import sqlite3, csv

conn = sqlite3.connect('day2/session2_database.db')
cur = conn.cursor()

cur.execute("SELECT user, COUNT(*), SUM(duration_ms) FROM events GROUP BY user ORDER BY SUM('duration_ms') DESC")
users_totals = cur.fetchall()
cur.execute("SELECT type, COUNT(*) FROM events GROUP BY type ORDER BY COUNT(*) DESC LIMIT 1")
common_type = cur.fetchone()
cur.execute("SELECT user, type, duration_ms FROM events WHERE duration_ms > 100")
events_over_100ms = cur.fetchall()
conn.close()
with open ('day2/session2_summary.csv', 'w', newline='') as summaryFile:
    writer = csv.writer(summaryFile)
    writer.writerow(['user', 'number_of_events', 'total_events_duration_ms'])
    writer.writerows(users_totals)
