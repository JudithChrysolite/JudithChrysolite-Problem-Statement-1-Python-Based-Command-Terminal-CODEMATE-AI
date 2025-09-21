import requests
import json

# Test the API endpoint
url = "http://127.0.0.1:5000/execute"

# Test commands
test_commands = [
    "pwd",
    "ls",
    "echo Hello World",
    "whoami"
]

print("Testing Flask terminal API...")
print("=" * 40)

for command in test_commands:
    payload = {"command": command}
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        print(f"Command: {command}")
        print(f"Output: {result.get('output', 'No output')}")
        print(f"Error: {result.get('error', 'None')}")
        print(f"Return Code: {result.get('return_code', 'N/A')}")
        print("-" * 40)
    else:
        print(f"Error with command '{command}': {response.status_code}")

print("Test completed!")
