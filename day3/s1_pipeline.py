import json
def load_json(path):
    """Load and return JSON data from a file."""
    with open(path) as f:
        return json.load(f)

def flatten_events(data):
    """Return a flat list of (user, type, duration_ms) tuples from nested JSON.
    """
    return [(u['name'], e['type'], e.get('duration_ms',0))
                 for u in  data['users']
                 for e in u['events']]

def create_events_table(conn):
    """Create the events table if it doesn't exist."""
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS events (
        user TEXT,
        type TEXT,
        duration_ms INTEGER)''')
    conn.commit()


def load_events_to_db(conn, events):
    """Delete existing rows and insert the given events - events must be list of tuples."""
    cur = conn.cursor()
    cur.execute("DELETE FROM events")
    cur.executemany("INSERT INTO events VALUES (?, ?, ?)", events)
    conn.commit()

def get_user_totals(conn):
    """Return (user, event_count, total_duration_ms) sorted by duration descending."""
    cur = conn.cursor()
    cur.execute("SELECT user, COUNT(*), SUM(duration_ms) FROM events GROUP BY user ORDER BY SUM('duration_ms') DESC")
    return cur.fetchall()
def get_most_common_type(conn):
    """Return most common event type from events table"""
    cur = conn.cursor()
    cur.execute("SELECT type, COUNT(*) FROM events GROUP BY type ORDER BY COUNT(*) DESC LIMIT 1")
    return cur.fetchone()