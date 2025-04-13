import json

def display_logs():
    with open('logs.json', 'r') as f:
        logs = json.load(f)
        
    print(f"\nTotal log entries: {len(logs)}")
    print("\nShowing first 5 log entries:\n")
    
    for i, log in enumerate(logs[:5], 1):
        print(f"\nLog Entry #{i}")
        print(f"Timestamp: {log['timestamp']}")
        print(f"Service: {log['service']}")
        print(f"Level: {log['level']}")
        print(f"Message: {log['message']}")
        print(f"Response Time: {log['response_time']:.2f}s")
        print(f"Status Code: {log['status_code']}")
        print("-" * 50)

if __name__ == "__main__":
    display_logs()