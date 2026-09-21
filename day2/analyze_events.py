import json
from collections import defaultdict, Counter

with open('day2/events.json') as f:
    data = json.load(f)

users = defaultdict(lambda:{'event_count':0,'total_duration_ms':0,'most_common':''})

for u in data['users']:
    ud = users[u['name']]
    ud['event_count']=len(u['events'])
    ud['total_duration_ms']=sum([e.get('duration_ms',0) for e in u['events']])
    ud['most_common']=Counter([e['type'] for e in u['events']]).most_common(1)[0][0]

users_report = [
    {'user': name, **stats}
    for name, stats in sorted(users.items(), key=lambda x: x[1]['total_duration_ms'], reverse=True)
]

with open('day2/summary_v1.json','w') as f:
    json.dump(users_report, f, indent=2)