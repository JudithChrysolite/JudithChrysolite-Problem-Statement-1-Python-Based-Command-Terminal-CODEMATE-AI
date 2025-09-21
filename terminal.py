import os
import shutil
import json
import subprocess
import psutil
from pathlib import Path
from datetime import datetime

class FileSystemTerminal:
    def __init__(self):
        self.current_path = Path.cwd()
    
    def execute_command(self, command):
        """Execute a command and return result as dictionary"""
        try:
            parts = command.strip().split()
            if not parts:
                return {"output": "", "error": None}
            
            cmd = parts[0].lower()
            args = parts[1:]
            
            # File & Directory Commands
            if cmd == "ls":
                return self._ls(args)
            elif cmd == "cd":
                return self._cd(args)
            elif cmd == "pwd":
                return self._pwd()
            elif cmd == "mkdir":
                return self._mkdir(args)
            elif cmd == "rm":
                return self._rm(args)
            elif cmd == "rmdir":
                return self._rmdir(args)
            elif cmd == "touch":
                return self._touch(args)
            elif cmd == "cat":
                return self._cat(args)
            elif cmd == "echo":
                return self._echo(args)
            elif cmd == "clear":
                return self._clear()
            elif cmd == "exit":
                return self._exit()
            
            # Process & System Commands
            elif cmd == "ps":
                return self._ps()
            elif cmd == "kill":
                return self._kill(args)
            elif cmd == "cpu":
                return self._cpu()
            elif cmd == "mem":
                return self._mem()
            elif cmd == "whoami":
                return self._whoami()
            elif cmd == "uptime":
                return self._uptime()
            else:
                return {"output": f"Command '{cmd}' not recognized", "error": "COMMAND_NOT_FOUND"}
                
        except Exception as e:
            return {"output": str(e), "error": "EXECUTION_ERROR"}
    
    def _ls(self, args):
        """List directory contents"""
        try:
            # Handle -l flag
            long_format = False
            path = self.current_path
            
            if args:
                if args[0] == "-l":
                    long_format = True
                    if len(args) > 1:
                        path = self.current_path / args[1]
                else:
                    path = self.current_path / args[0]
            
            # If no path specified, use current directory
            if not args:
                path = self.current_path
            
            if not path.exists():
                if args:
                    return {"output": f"ls: cannot access '{args[0]}': No such file or directory", "error": "FILE_NOT_FOUND"}
                else:
                    return {"output": f"ls: cannot access '.': No such file or directory", "error": "FILE_NOT_FOUND"}
            
            if not path.is_dir():
                if args:
                    return {"output": f"ls: '{args[0]}': Not a directory", "error": "NOT_A_DIRECTORY"}
                else:
                    return {"output": f"ls: '{path.name}' is not a directory", "error": "NOT_A_DIRECTORY"}
            
            items = []
            try:
                for item in path.iterdir():
                    if long_format:
                        # In long format, we'd show more details, but for simplicity we'll just show name
                        if item.is_dir():
                            items.append(f"d  {item.name}")
                        else:
                            items.append(f"-  {item.name}")
                    else:
                        if item.is_dir():
                            items.append(f"{item.name}/")
                        else:
                            items.append(item.name)
            except PermissionError:
                return {"output": f"ls: cannot open directory '{path.name}': Permission denied", "error": "PERMISSION_DENIED"}
            
            return {"output": "\n".join(items), "error": None}
        except Exception as e:
            return {"output": str(e), "error": "EXECUTION_ERROR"}
    
    def _cd(self, args):
        """Change directory"""
        try:
            if not args:
                return {"output": "cd: missing argument", "error": "MISSING_ARGUMENT"}
            
            target = args[0]
            if target == "..":
                self.current_path = self.current_path.parent
            elif target == "~":
                self.current_path = Path.home()
            else:
                new_path = self.current_path / target
                if new_path.exists() and new_path.is_dir():
                    self.current_path = new_path
                else:
                    return {"output": f"cd: '{target}': No such file or directory", "error": "FILE_NOT_FOUND"}
            
            return {"output": str(self.current_path), "error": None}
        except Exception as e:
            return {"output": str(e), "error": "EXECUTION_ERROR"}
    
    def _pwd(self):
        """Print working directory"""
        return {"output": str(self.current_path), "error": None}
    
    def _mkdir(self, args):
        """Make directory"""
        try:
            if not args:
                return {"output": "mkdir: missing operand", "error": "MISSING_ARGUMENT"}
            
            recursive = False
            dirs = []
            for arg in args:
                if arg == "-p":
                    recursive = True
                else:
                    dirs.append(arg)
            
            for dirname in dirs:
                new_dir = self.current_path / dirname
                if recursive:
                    new_dir.mkdir(parents=True, exist_ok=True)
                else:
                    new_dir.mkdir(exist_ok=True)
            
            return {"output": "", "error": None}
        except Exception as e:
            return {"output": str(e), "error": "EXECUTION_ERROR"}
    
    def _rm(self, args):
        """Remove files/directories"""
        try:
            if not args:
                return {"output": "rm: missing operand", "error": "MISSING_ARGUMENT"}
            
            recursive = False
            files = []
            for arg in args:
                if arg == "-r":
                    recursive = True
                else:
                    files.append(arg)
            
            for filename in files:
                target = self.current_path / filename
                if target.exists():
                    if target.is_dir():
                        if recursive:
                            shutil.rmtree(target)
                        else:
                            return {"output": f"rm: cannot remove '{filename}': Is a directory", "error": "IS_A_DIRECTORY"}
                    else:
                        target.unlink()
                else:
                    return {"output": f"rm: cannot remove '{filename}': No such file or directory", "error": "FILE_NOT_FOUND"}
            
            return {"output": "", "error": None}
        except Exception as e:
            return {"output": str(e), "error": "EXECUTION_ERROR"}
    
    def _rmdir(self, args):
        """Remove empty directory"""
        try:
            if not args:
                return {"output": "rmdir: missing operand", "error": "MISSING_ARGUMENT"}
            
            for dirname in args:
                target = self.current_path / dirname
                if target.exists() and target.is_dir():
                    try:
                        target.rmdir()
                    except OSError as e:
                        if e.errno == 39:  # Directory not empty
                            return {"output": f"rmdir: failed to remove '{dirname}': Directory is not empty", "error": "DIRECTORY_NOT_EMPTY"}
                        else:
                            return {"output": str(e), "error": "EXECUTION_ERROR"}
                else:
                    return {"output": f"rmdir: failed to remove '{dirname}': No such file or directory", "error": "FILE_NOT_FOUND"}
            
            return {"output": "", "error": None}
        except Exception as e:
            return {"output": str(e), "error": "EXECUTION_ERROR"}
    
    def _touch(self, args):
        """Create empty file or update timestamp"""
        try:
            if not args:
                return {"output": "touch: missing file operand", "error": "MISSING_ARGUMENT"}
            
            for filename in args:
                target = self.current_path / filename
                target.touch(exist_ok=True)
            
            return {"output": "", "error": None}
        except Exception as e:
            return {"output": str(e), "error": "EXECUTION_ERROR"}
    
    def _cat(self, args):
        """Display file contents"""
        try:
            if not args:
                return {"output": "cat: missing file operand", "error": "MISSING_ARGUMENT"}
            
            contents = []
            for filename in args:
                target = self.current_path / filename
                if target.exists() and target.is_file():
                    with open(target, 'r') as f:
                        contents.append(f.read())
                else:
                    return {"output": f"cat: '{filename}': No such file or directory", "error": "FILE_NOT_FOUND"}
            
            return {"output": "\n".join(contents), "error": None}
        except Exception as e:
            return {"output": str(e), "error": "EXECUTION_ERROR"}
    
    def _echo(self, args):
        """Print text to terminal"""
        return {"output": " ".join(args), "error": None}
    
    def _clear(self):
        """Clear output area (handled on frontend)"""
        return {"output": "", "error": None}
    
    def _exit(self):
        """End session (clear server-side session context)"""
        # Reset to initial state
        self.current_path = Path.cwd()
        return {"output": "Session ended", "error": None}
    
    def _ps(self):
        """List running processes"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'username']):
                try:
                    processes.append(f"{proc.info['pid']:6d} {proc.info['name']:<20} {proc.info['username']}")
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    # Skip processes we can't access
                    continue
            return {"output": "\n".join(processes), "error": None}
        except Exception as e:
            return {"output": str(e), "error": "EXECUTION_ERROR"}
    
    def _kill(self, args):
        """Terminate a process by PID"""
        try:
            if not args:
                return {"output": "kill: missing operand", "error": "MISSING_ARGUMENT"}
            
            pid = int(args[0])
            try:
                process = psutil.Process(pid)
                process.terminate()
                return {"output": f"Process {pid} terminated", "error": None}
            except psutil.NoSuchProcess:
                return {"output": f"kill: {pid}: No such process", "error": "NO_SUCH_PROCESS"}
            except psutil.AccessDenied:
                return {"output": f"kill: {pid}: Operation not permitted", "error": "PERMISSION_DENIED"}
        except ValueError:
            return {"output": f"kill: invalid PID '{args[0]}'", "error": "INVALID_PID"}
        except Exception as e:
            return {"output": str(e), "error": "EXECUTION_ERROR"}
    
    def _cpu(self):
        """Show CPU usage percentage"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            return {"output": f"CPU Usage: {cpu_percent}%", "error": None}
        except Exception as e:
            return {"output": str(e), "error": "EXECUTION_ERROR"}
    
    def _mem(self):
        """Show memory usage statistics"""
        try:
            memory = psutil.virtual_memory()
            return {"output": f"Memory Usage:\nTotal: {memory.total // (1024**2)} MB\nAvailable: {memory.available // (1024**2)} MB\nUsed: {memory.used // (1024**2)} MB\nPercentage: {memory.percent}%", "error": None}
        except Exception as e:
            return {"output": str(e), "error": "EXECUTION_ERROR"}
    
    def _whoami(self):
        """Display current user"""
        try:
            return {"output": os.getlogin(), "error": None}
        except Exception as e:
            return {"output": str(e), "error": "EXECUTION_ERROR"}
    
    def _uptime(self):
        """Show system uptime"""
        try:
            # Get uptime in seconds
            uptime_seconds = psutil.boot_time()
            # Convert to readable format (this is simplified)
            return {"output": f"System Uptime: {uptime_seconds}", "error": None}
        except Exception as e:
            return {"output": str(e), "error": "EXECUTION_ERROR"}

# Global terminal instance
terminal = FileSystemTerminal()

def execute_terminal_command(command):
    """Wrapper function to execute command through terminal"""
    return terminal.execute_command(command)
