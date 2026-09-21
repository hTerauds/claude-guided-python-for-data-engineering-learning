import sqlite3
from s2_pipeline import fetch_users, flatten_api_users, create_api_users_table, load_api_users_to_db, get_company_with_most_users

if __name__ == "__main__":
    data = fetch_users()
    flat_data = flatten_api_users(data)
    conn = sqlite3.connect('day3/p2_db.db')
    create_api_users_table(conn)
    load_api_users_to_db(conn,flat_data)
    print(get_company_with_most_users(conn))
    conn.close