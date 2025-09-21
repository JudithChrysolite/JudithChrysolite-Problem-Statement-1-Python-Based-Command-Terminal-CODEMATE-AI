#!/usr/bin/env python3
"""
Test script for the Python terminal implementation
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from terminal import execute_terminal_command

def test_basic_commands():
    """Test basic terminal commands"""
    print("Testing basic terminal commands...")
    
    # Test pwd
    result = execute_terminal_command("pwd")
    print(f"pwd: {result}")
    
    # Test ls
    result = execute_terminal_command("ls")
    print(f"ls: {result}")
    
    # Test mkdir
    result = execute_terminal_command("mkdir test_folder")
    print(f"mkdir test_folder: {result}")
    
    # Test ls again to see the new folder
    result = execute_terminal_command("ls")
    print(f"ls after mkdir: {result}")
    
    # Test cd
    result = execute_terminal_command("cd test_folder")
    print(f"cd test_folder: {result}")
    
    # Test pwd again
    result = execute_terminal_command("pwd")
    print(f"pwd after cd: {result}")
    
    # Test touch
    result = execute_terminal_command("touch test_file.txt")
    print(f"touch test_file.txt: {result}")
    
    # Test ls to see the new file
    result = execute_terminal_command("ls")
    print(f"ls after touch: {result}")
    
    # Test cat on non-existent file
    result = execute_terminal_command("cat nonexistent.txt")
    print(f"cat nonexistent.txt: {result}")
    
    # Test echo
    result = execute_terminal_command("echo Hello World")
    print(f"echo Hello World: {result}")
    
    # Test cd back to parent
    result = execute_terminal_command("cd ..")
    print(f"cd ..: {result}")
    
    # Test rm
    result = execute_terminal_command("rm -r test_folder")
    print(f"rm -r test_folder: {result}")
    
    # Final ls
    result = execute_terminal_command("ls")
    print(f"ls after cleanup: {result}")

if __name__ == "__main__":
    test_basic_commands()
