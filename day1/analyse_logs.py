import csv
from collections import defaultdict, Counter

userLogs = []
usersData = defaultdict(lambda: {'actions': [], 'commonAction': '', 'userActionsDuration': 0})

with open('day1/logs.csv', newline='') as csvFile:
    reader = csv.reader(csvFile, delimiter=',')
    header = next(reader)  # skip header row explicitly instead of checking d[0]!='timestamp' every row

    for d in reader:
        try:
            userLogs.append({
                'timestamp': d[0],
                'user': d[1],
                'action': d[2],
                'duration_ms': int(d[3])
            })
        except (IndexError, ValueError):
            # IndexError: row has fewer columns than expected (malformed row)
            # ValueError: duration_ms is missing, empty, or not a valid integer
            print(f"Skipping bad row: {d}")
            continue

for ul in userLogs:
    ud = usersData[ul['user']]
    ud['userActionsDuration'] += ul['duration_ms']
    ud['actions'].append(ul['action'])

for ud in usersData.values():
    mc = Counter(ud['actions']).most_common(1)
    ud['commonAction'] = f'Most common action is {mc[0][0]} and it appears {mc[0][1]} times in user logs.'

sorted_users = sorted(usersData.items(), key=lambda x: x[1]['userActionsDuration'], reverse=True)

with open('day1/summary.csv', 'w', newline='') as summaryFile:
    writer = csv.writer(summaryFile)
    writer.writerow(['user', 'action_count', 'total_duration_ms', 'common_action'])
    for user, ud in sorted_users:
        writer.writerow([user, len(ud['actions']), ud['userActionsDuration'], ud['commonAction']])

print(f"Summary written for {len(sorted_users)} users -> day1/summary.csv")