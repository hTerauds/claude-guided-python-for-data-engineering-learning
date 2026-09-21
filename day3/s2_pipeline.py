import requests
def fetch_users(url='https://jsonplaceholder.typicode.com/users'):
    """Fetch users from the API and return the parsed JSON (list of dicts)."""
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def flatten_api_users(users):
    """Return a flat list of (name, city, company_name) tuples."""
    return[(u['name'], u['address']['city'], u['company']['name']) for u in users
    ]
    
def create_api_users_table(conn):
    """Create the users table if it doesn't exist."""
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS api_users (
        name TEXT,
        city TEXT,
        company_name TEXT)''')
    conn.commit()

def load_api_users_to_db(conn, events):
    """Delete existing rows and insert the given users from API - users must be list of tuples."""
    cur = conn.cursor()
    cur.execute("DELETE FROM api_users")
    cur.executemany("INSERT INTO api_users VALUES (?, ?, ?)", events)
    conn.commit()

def get_company_with_most_users(conn):
    """Return (name, city, company_name) grouped by company sorted by count of users descending."""
    cur = conn.cursor()
    cur.execute("SELECT company_name, COUNT(*) FROM api_users GROUP BY company_name ORDER BY COUNT(*) DESC")
    return cur.fetchall()