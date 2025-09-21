from flask import Flask, render_template, request, jsonify
from terminal import execute_terminal_command
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute():
    command = request.json.get('command', '')
    if not command:
        return jsonify({'output': 'No command provided', 'error': 'MISSING_COMMAND'})
    
    result = execute_terminal_command(command)
    # Add required fields to match specification
    response = {
        "command": command,
        "cwd": str(result.get("cwd", "")),
        "output": result.get("output", ""),
        "error": result.get("error", ""),
        "return_code": 0 if not result.get("error") else 1,
        "timestamp": datetime.datetime.now().isoformat()
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
