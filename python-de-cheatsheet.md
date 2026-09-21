# Python for Data Engineering — Patterns Cheat Sheet

Reusable idioms from Days 1-3. Keep this next to your code as a quick reference.

## Data structures

```python
from collections import defaultdict, Counter

# defaultdict: avoid "check if key exists, else create" boilerplate
data = defaultdict(lambda: {'count': 0, 'total': 0})
data[key]['count'] += 1   # creates the entry automatically on first use

# Counter: frequency counting
Counter(['login', 'login', 'click']).most_common(1)   # [('login', 2)]
```

**Rule of thumb:** if you're looping through a list to find the dict where some field matches, that list should probably be a dict keyed on that field instead.

## Comprehensions

```python
# List comprehension
durations = [e['duration_ms'] for e in events]

# Nested (mirrors nested for loops, outer loop first)
rows = [(u['name'], e['type']) for u in users for e in u['events']]

# With a filter
big = [e for e in events if e['duration_ms'] > 100]
```

## Safe access to dicts

```python
value = d.get('key', default)   # returns default if key missing — no crash
```

Use `.get()` when missing data is *expected* (optional fields). Use direct `d['key']` when missing data would mean something is actually broken and you *want* the crash.

## Error handling

```python
try:
    value = int(row[3])
except (IndexError, ValueError):
    # IndexError: row too short; ValueError: not a valid int
    continue
```

Prefer attempting the operation and catching what goes wrong over pre-checking every possible failure mode.

## Sorting

```python
sorted(items, key=lambda x: x[1]['total'], reverse=True)
```

`key=` tells `sorted()` what to compare by. `lambda x: ...` is a one-expression anonymous function (like a JS arrow function, but body-restricted to a single expression — no multi-line logic).

## JSON

```python
import json
data = json.loads(text)          # string -> Python
text = json.dumps(data, indent=2) # Python -> string
data = json.load(file_obj)        # file -> Python
json.dump(data, file_obj, indent=2)  # Python -> file
```

## Tuples vs lists

- Tuple `(a, b, c)` — immutable, fixed-shape; what SQL rows and `dict.items()` naturally are.
- List `[a, b, c]` — mutable, grows/shrinks.

## SQLite (`sqlite3`)

```python
import sqlite3
conn = sqlite3.connect('data.db')
cur = conn.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS t (a TEXT, b INTEGER)')
cur.executemany('INSERT INTO t VALUES (?, ?)', list_of_tuples)  # never f-string values into SQL
conn.commit()

cur.execute('SELECT a, SUM(b) FROM t GROUP BY a ORDER BY SUM(b) DESC')
rows = cur.fetchall()   # or .fetchone() for a single row
conn.close()
```

## HTTP requests

```python
import requests
r = requests.get(url, params={'key': 'value'})  # builds ?key=value safely
r.raise_for_status()   # raises on 4xx/5xx instead of silently continuing
data = r.json()
```

## Functions & structure

```python
def load_json(path):
    """One-line docstring describing what this returns."""
    with open(path) as f:
        return json.load(f)

if __name__ == "__main__":
    main()   # only runs when the file is executed directly, not when imported
```

## Git essentials

```bash
git status                  # what's changed
git add .
git commit -m "message"
git push
git config --global --list  # check current identity
```

`.gitignore` essentials for this kind of project:
```
*.db
__pycache__/
```
