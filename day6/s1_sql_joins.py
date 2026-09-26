import requests, sqlite3
users = requests.get('https://jsonplaceholder.typicode.com/users').json()
posts = requests.get('https://jsonplaceholder.typicode.com/posts').json()
comments = requests.get('https://jsonplaceholder.typicode.com/comments').json()
conn = sqlite3.connect('day6/s1_data.db')
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, name TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS posts (id INTEGER, user_id INTEGER, title TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS comments (id INTEGER, post_id INTEGER, body TEXT)")

flat_users = [(u['id'], u['name']) for u in users]
flat_posts = [(p['id'], p['userId'], p['title']) for p in posts]
flat_comments = [(c['id'], c['postId'], c['body']) for c in comments]
cur.execute("DELETE FROM users")
cur.execute("DELETE FROM posts")
cur.execute("DELETE FROM comments")
cur.executemany("INSERT INTO users VALUES (?, ?)", flat_users)
cur.executemany("INSERT INTO posts VALUES (?, ?, ?)", flat_posts)
cur.executemany("INSERT INTO comments VALUES (?, ?, ?)",flat_comments)
posts_with_author = cur.execute("SELECT u.name, p.title FROM users u JOIN posts p ON u.id = p.user_id LIMIT 10")
#Post count per user, including any user with zero posts 
# (there shouldn't be any in this dataset, 
# but write it as a LEFT JOIN anyway — good habit):
count_per_user = cur.execute('''
    SELECT u.name, COUNT(p.id) as post_count 
    FROM users u LEFT JOIN posts p ON u.id = p.user_id
    GROUP BY u.name ORDER BY post_count DESC 
''').fetchall()
user_with_fewest_posts = cur.execute('''
    SELECT u.name, COUNT(p.id) as posts_count 
    FROM users u LEFT JOIN posts p ON u.id = p.user_id
    GROUP BY u.name ORDER BY posts_count ASC LIMIT 1
''').fetchall()
user_with_most_comments = cur.execute('''
    SELECT u.name, COUNT(c.id) as comments_count
    FROM users u LEFT JOIN posts p ON u.id = p.user_id
    LEFT JOIN comments c ON p.id = c.post_id
    GROUP BY u.name ORDER BY comments_count DESC LIMIT 1
''').fetchone()
user_by_comments_count = cur.execute('''
    SELECT u.name, COUNT(c.id) as comments_count
    FROM users u LEFT JOIN posts p ON u.id = p.user_id
    LEFT JOIN comments c ON p.id = c.post_id
    GROUP BY u.name ORDER BY comments_count DESC
''').fetchall()
if user_by_comments_count [0][1] == user_by_comments_count[1][1]:
    print(f"There are no single user who have most comments becouse there are multiple users with {user_by_comments_count [0][1]} comments (most comments that one user have)")
else:
    print(f'{user_with_most_comments[0]} have {user_with_most_comments[1]} comments, and that is the most comments between all users')
print(f'{user_with_fewest_posts[0][0]} have {user_with_fewest_posts[0][1]} posts, and that is the fewest number of posts between all users')
