import random
from datetime import datetime, timedelta
import json

def generate_logs(num_entries=1000):
    services = ['web', 'api', 'database', 'auth', 'cache']
    levels = ['INFO', 'WARNING', 'ERROR']
    messages = [
        'Request processed successfully',
        'Database connection timeout',
        'Authentication failed',
        'Cache miss',
        'High memory usage'
    ]

    logs = []
    start_time = datetime.now()

    for i in range(num_entries):
        timestamp = start_time + timedelta(seconds=i)
        log_entry = {
            'timestamp': timestamp.isoformat(),
            'service': random.choice(services),
            'level': random.choice(levels),
            'message': random.choice(messages),
            'response_time': random.uniform(0.1, 2.0),
            'status_code': random.choice([200, 201, 400, 401, 403, 500])
        }
        
        if random.random() < 0.05:  # 5% chance of anomaly
            log_entry.update({
                'response_time': random.uniform(5.0, 10.0),
                'status_code': 500,
                'level': 'ERROR'
            })
        
        logs.append(log_entry)
    
    return logs

if __name__ == "__main__":
    logs = generate_logs()
    with open('logs.json', 'w') as f:
        json.dump(logs, f, indent=2)
    print(f"Generated {len(logs)} log entries")