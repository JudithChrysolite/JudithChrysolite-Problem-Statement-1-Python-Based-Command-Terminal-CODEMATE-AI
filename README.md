<<<<<<< HEAD
# Python Command Terminal with Flask Backend

A web-based terminal emulator with a Flask backend that provides secure execution of filesystem and system commands.

## Features

### File & Directory Commands
- `pwd` - Print current working directory
- `ls` - List files and directories
- `ls -l` - List files and directories in long format
- `cd <path>` - Change current directory (supports `cd ..` and `cd ~`)
- `mkdir <dirname>` - Create a directory
- `mkdir -p path/to/dir` - Create nested directories recursively
- `rmdir <dirname>` - Remove empty directory
- `rm <filename>` - Delete a file
- `rm -r <dirname>` - Remove directory recursively
- `touch <filename>` - Create an empty file or update timestamp
- `cat <filename>` - Display file contents
- `echo <text>` - Print text to terminal
- `clear` - Clear output area (handled on frontend)
- `exit` - End session

### Process & System Commands
- `ps` - List running processes (PID, name, username)
- `kill <pid>` - Terminate a process by PID
- `cpu` - Show CPU usage percentage
- `mem` - Show memory usage statistics
- `whoami` - Display current user
- `uptime` - Show system uptime

## Installation

1. Clone or download this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Start the Flask server:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to `http://localhost:5000`

## API Endpoint

The Flask backend exposes the following endpoint:

- `POST /execute` - Accepts JSON with a command and returns structured results:
  ```json
  {
    "command": "ls",
    "cwd": "/home/user",
    "output": "file1.txt\nfolder/",
    "error": "",
    "return_code": 0,
    "timestamp": "2025-09-21T12:34:56+05:30"
  }
  ```

## Security Notes

This implementation uses Python's `os`, `shutil`, and `psutil` modules to execute commands securely, avoiding direct shell injection vulnerabilities. All commands are parsed and validated before execution.

## Project Structure

```
.
├── app.py              # Flask application entry point
├── requirements.txt    # Python dependencies
├── terminal.py         # Terminal command execution logic
├── test_terminal.py    # Test script for terminal functionality
└── templates/
    └── index.html      # Web interface
```

## Error Handling

The application handles various error conditions:
- Invalid commands return "Command not found"
- Invalid file/directory operations return descriptive errors
- Permission denied errors are handled appropriately
- Non-empty directory removal shows "Directory is not empty" error
- Missing arguments for commands are handled properly

## Optional Features

- Command history display
- Real-time current working directory display
- Color-coded output (success/error)
- Terminal prompt styling
- Improved user experience with focused input and command history
=======
# Problem-Statement-1-Python-Based-Command-Terminal-CODEMATE-AI
>>>>>>> c4eccf80174571f155ffaae3610c48d59c90a422
