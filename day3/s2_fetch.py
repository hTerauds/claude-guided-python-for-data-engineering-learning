import requests

def fetch_posts(userID, url='https://jsonplaceholder.typicode.com/posts'):
    """Fetch posts from the API with parameter and return the parsed JSON (list of dicts)."""
    response = requests.get(url, params={'userId':userID})
    response.raise_for_status()
    print(response.url)
    return response.json()
    
api_posts = fetch_posts(1)

print(api_posts)