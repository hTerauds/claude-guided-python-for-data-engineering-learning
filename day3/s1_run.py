import sqlite3
from s1_pipeline import load_json, flatten_events, create_events_table, load_events_to_db, get_user_totals, get_most_common_type

if __name__ == "__main__":
    data = load_json('day2/events.json')
    events = flatten_events(data)
    conn = sqlite3.connect('day3/s1_db.db')
    create_events_table(conn)
    load_events_to_db(conn, events)
    totals = get_user_totals(conn)
    common = get_most_common_type(conn)
    print(common)
    conn.close()