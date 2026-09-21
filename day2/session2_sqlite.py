import sqlite3, json
#load data from json
with open('day2/events.json') as f:
    events_data = json.load(f)

conn = sqlite3.connect('day2/session2_database.db')
cur = conn.cursor()
#Creates a table events with columns user, type, duration_ms
cur.execute('''
    CREATE TABLE IF NOT EXISTS events (
        user TEXT,
        type TEXT,
        duration_ms INTEGER
    )
''')

#Flattens the nested JSON into a flat list 
# of (user, type, duration_ms) tuples — one row per event,
#  not per user. 
# (Hint: nested list comprehension, 
# or a plain double loop — whichever reads clearer to you.)
events = list()
for u in events_data['users']:
    for e in u['events']:
        events.append((u['name'], e['type'], e.get('duration_ms', 0)))
events_lc = [(u['name'], e['type'], e.get('duration_ms', 0)) 
             for u in events_data['users'] 
             for e in u['events']]
print (events==events_lc)
cur.execute("DELETE FROM events")
conn.commit() #is this necesary?
cur.executemany("INSERT INTO events VALUES (?, ?, ?)", events_lc)
conn.commit()
conn.close()