#!/usr/bin/env python3
"""
Windows VM Control CLI Tool
Intelligent middleware for CUA to control Windows VM mouse and keyboard
"""

import sys
import re
import time
import os
import threading
import requests
import platform
import shutil
import tempfile
import stat
import json
import zipfile
import subprocess
import paramiko
import getpass
from pathlib import Path
from typing import Optional, Tuple

# Version and Repository Info
__version__ = "1.0.0"
REPO = "nullvoider07/windows_actuation_control"

class VMController:
    """Smart CLI tool for controlling Windows VM via SSH"""
    
    # Mouse action keywords
    MOUSE_ACTIONS = {
        'move', 'left', 'right', 'middle', 'double', 
        'scroll_up', 'scroll_down', 'drag', 'here',
        'hold', 'release'
    }
    
    # Keyboard action keywords
    KEYBOARD_ACTIONS = {'type', 'press'}
    
    # Special keys that indicate keyboard command
    KEYBOARD_INDICATORS = {
        '{Enter}', '{Esc}', '{Tab}', '{Backspace}', '{BS}',
        '{Delete}', '{Del}', '{Space}', '{Up}', '{Down}',
        '{Left}', '{Right}', '{Home}', '{End}', '{PgUp}',
        '{PgDn}', '{F1}', '{F2}', '{F3}', '{F4}', '{F5}',
        '{F6}', '{F7}', '{F8}', '{F9}', '{F10}', '{F11}', '{F12}',
        '{LWin}', '{RWin}'
    }
    
    def __init__(self, host: str, username: str, port: int = 2222):
        """Initialize VM controller with connection details"""
        self.host = host
        self.username = username
        self.port = port
        self.ssh_client: Optional[paramiko.SSHClient] = None
        self.connected = False

    # Establish SSH connection    
    def connect(self, password: str) -> bool:
        """Establish persistent SSH connection"""
        try:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            print(f"[*] Connecting to {self.username}@{self.host}:{self.port}...")
            self.ssh_client.connect(
                hostname=self.host,
                port=self.port,
                username=self.username,
                password=password,
                look_for_keys=False,
                allow_agent=False
            )
            
            self.connected = True
            print(f"[✓] Connected successfully!")
            return True
            
        except paramiko.AuthenticationException:
            print("[✗] Authentication failed. Invalid credentials.")
            return False
        except paramiko.SSHException as e:
            print(f"[✗] SSH error: {e}")
            return False
        except Exception as e:
            print(f"[✗] Connection failed: {e}")
            return False
    
    # Close SSH connection
    def disconnect(self):
        """Close SSH connection"""
        if self.ssh_client:
            self.ssh_client.close()
            self.connected = False
            print("[*] Disconnected from VM")
    
    # Monitor connection health
    def _monitor_connection(self):
        """Background thread to monitor SSH connection health"""
        while self.connected:
            try:
                if self.ssh_client:
                    transport = self.ssh_client.get_transport()
                    if transport is None or not transport.is_active():
                        raise Exception("Transport closed")    
                    transport.send_ignore()
                time.sleep(3)
                
            except Exception:
                if self.connected:
                    print("\n\n[!] Connection to VM lost unexpectedly.")
                    print("[*] Shutting down...")
                    self.connected = False
                    os._exit(1)
                break
    
    # Smart command type detection
    def detect_command_type(self, command: str) -> Tuple[str, str]:
        """
        Smart detection of command type (mouse/keyboard)
        Returns: (type, command)
        """
        tokens = command.strip().split()
        
        if not tokens:
            return 'invalid', command
        
        # Check if starts with coordinates (numbers)
        if len(tokens) >= 2:
            try:
                int(tokens[0])
                int(tokens[1])
                # Has coordinates - likely mouse command
                if len(tokens) >= 3 and tokens[2] in self.MOUSE_ACTIONS:
                    return 'mouse', command
                elif len(tokens) == 2:
                    # Just coordinates, assume move
                    return 'mouse', f"{command} move"
            except ValueError:
                pass
        
        # Check for "here" keyword (mouse)
        if tokens[0] == 'here':
            if len(tokens) >= 2 and tokens[1] in self.MOUSE_ACTIONS:
                return 'mouse', command
            else:
                return 'invalid', command
        
        # Check for explicit keyboard actions
        if tokens[0] in self.KEYBOARD_ACTIONS:
            return 'keyboard', command
        
        # Check for modifier keys at start (e.g., ^, +, !, #)
        modifier_pattern = r'^[\^+!#]'
        if re.match(modifier_pattern, command):
            return 'keyboard', f"press {command}"
        
        # Check for keyboard indicators (special keys) - but not if already has 'press'
        if any(indicator in command for indicator in self.KEYBOARD_INDICATORS):
            if not command.startswith('press '):
                return 'keyboard', f"press {command}"
            return 'keyboard', command
        
        # If none of the above, check if first token is mouse action
        if tokens[0] in self.MOUSE_ACTIONS:
            return 'mouse', command
        
        # Default: assume it's text to type
        return 'keyboard', f"type {command}"
    
    # Execute command on VM
    def execute_command(self, command: str) -> bool:
        """Execute command on VM"""
        if not self.connected or self.ssh_client is None:
            print("[✗] Not connected to VM")
            return False
        
        # Detect command type
        cmd_type, processed_cmd = self.detect_command_type(command)
        
        if cmd_type == 'invalid':
            print(f"[✗] Invalid command: {command}")
            return False
        
        # Build the SSH command
        if cmd_type == 'mouse':
            remote_cmd = f'echo {processed_cmd} > C:\\mouse_cmd.txt'
            prefix = "[MOUSE]"
        else:
            escaped_cmd = processed_cmd.replace('^', '^^')
            remote_cmd = f'echo {escaped_cmd} > C:\\keyboard_cmd.txt'
            prefix = "[KEYBOARD]"
        
        try:
            # Execute command
            stdin, stdout, stderr = self.ssh_client.exec_command(remote_cmd)
            stdout.channel.recv_exit_status()  # Wait for completion
            
            # Enhanced feedback for drag operations
            if 'drag' in processed_cmd:
                parts = processed_cmd.split()
                if len(parts) >= 5:
                    print(f"{prefix} Drag: ({parts[0]},{parts[1]}) → ({parts[3]},{parts[4]})")
                else:
                    print(f"{prefix} Executed: {processed_cmd}")
            else:
                print(f"{prefix} Executed: {processed_cmd}")
                
            ui_opening_commands = [
                'press #r',
                'press #',
                'press !{Tab}',
                'press ^+{Esc}',
            ]
            
            # Check if this command opens a UI element
            for ui_cmd in ui_opening_commands:
                if ui_cmd in processed_cmd:
                    time.sleep(0.3)
                    break
            
            return True
            
        except Exception as e:
            print(f"[✗] Execution failed: {e}")
            return False
    
    # Batch mode execution
    def batch_mode(self, commands: list, delay: float = 0.1):
        """Execute a batch of commands with optional delays"""
        print(f"\n[*] Batch mode: Executing {len(commands)} commands...")
        
        for i, command in enumerate(commands, 1):
            if not command.strip():
                continue
            
            print(f"\n[{i}/{len(commands)}] ", end="")
            self.execute_command(command.strip())
            
            if i < len(commands):
                time.sleep(delay)
        
        print("\n[✓] Batch execution complete!")
    
    # Interactive mode
    def interactive_mode(self):
        """Interactive command loop"""
        print("\n" + "="*60)
        print("  Windows VM Control - Interactive Mode")
        print("="*60)
        print("\nCommands:")
        print("  Mouse:    <x> <y> <action>  (e.g., 500 500 right)")
        print("  Keyboard: type <text>       (e.g., type Hello)")
        print("  Keyboard: press <keys>      (e.g., press ^c)")
        print("  Special:  exit, quit        (disconnect)")
        print("  Special:  help              (show this help)")
        print("="*60 + "\n")
        
        monitor_thread = threading.Thread(target=self._monitor_connection, daemon=True)
        monitor_thread.start()

        while self.connected:
            try:
                user_input = input("VM> ").strip()
                
                if not user_input:
                    continue
                
                # Handle special commands
                if user_input.lower() in ['exit', 'quit']:
                    print("[*] Exiting...")
                    break
                
                if user_input.lower() == 'help':
                    self.show_help()
                    continue
                
                # Execute user command
                self.execute_command(user_input)
                
            except KeyboardInterrupt:
                print("\n[*] Interrupted. Type 'exit' to disconnect.")
            except EOFError:
                print("\n[*] EOF detected. Disconnecting...")
                break
        
        self.disconnect()
    
    # Show help information
    def show_help(self):
        """Display help information"""
        help_text = """
╔══════════════════════════════════════════════════════════╗
║                   COMMAND REFERENCE                      ║
╠══════════════════════════════════════════════════════════╣
║ MOUSE COMMANDS                                           ║
╠══════════════════════════════════════════════════════════╣
║ <x> <y> move           → Move cursor to coordinates      ║
║ <x> <y> left           → Move and left-click             ║
║ <x> <y> right          → Move and right-click            ║
║ <x> <y> double         → Move and double-click           ║
║ <x> <y> middle         → Move and middle-click           ║
║ <x> <y> scroll_up [n]  → Move and scroll up              ║
║ <x> <y> scroll_down [n]→ Move and scroll down            ║
║ <x> <y> drag <x2> <y2> → Drag from (x,y) to (x2,y2)      ║
║ here <action>          → Action at current position      ║
╠══════════════════════════════════════════════════════════╣
║ KEYBOARD COMMANDS                                        ║
╠══════════════════════════════════════════════════════════╣
║ type <text>            → Type literal text               ║
║ press <keys>           → Press keys/shortcuts            ║
║ {Enter}                → Press Enter (auto-detected)     ║
║ ^c                     → Ctrl+C (auto-detected)          ║
║                                                          ║
║ Modifiers: ^ (Ctrl), + (Shift), ! (Alt), # (Win)         ║
║ Special: {Enter}, {Esc}, {Tab}, {F1}-{F12}, etc.         ║
╠══════════════════════════════════════════════════════════╣
║ EXAMPLES                                                 ║
╠══════════════════════════════════════════════════════════╣
║ 960 540 right          → Right-click at center           ║
║ here left              → Left-click at current pos       ║
║ type Hello World       → Type text                       ║
║ press ^v               → Paste (Ctrl+V)                  ║
║ {Enter}                → Press Enter                     ║
║ {LWin}                 → Press Windows key (opens Start) ║
║ 200 200 drag 800 600   → Drag operation                  ║
╚══════════════════════════════════════════════════════════╝
        """
        print(help_text)

# Show version information
def show_version():
    """Show version information"""
    print("=" * 50)
    print(f"Windows Actuation Control v{__version__}")
    print("=" * 50)
    print(f"  * OS: {platform.system()} {platform.release()}")
    print(f"  * Architecture: {platform.machine()}")
    print("=" * 50)

# Update mechanism
def update_tool(check_only: bool = False):
    """Check for updates and install the latest version"""
    print("[*] Checking for updates...")
    print(f"    Current version: v{__version__}")
    
    try:
        # 1. Get latest release from GitHub
        release_url = f"https://api.github.com/repos/{REPO}/releases/latest"
        response = requests.get(release_url, timeout=10)
        response.raise_for_status()
        
        latest_release = response.json()
        latest_tag = latest_release['tag_name']
        
        # Handle 'win-v', 'v', or just number prefixes
        cleaned_tag = latest_tag.replace('win-', '')
        latest_version = cleaned_tag.lstrip('v')
        
        print(f"    Latest version:  v{latest_version}")
        
        if latest_version == __version__:
            print("[✓] You already have the latest version!")
            return
        
        print(f"\n[!] New version available: v{latest_version}")
        
        if check_only:
            print("    Run 'windows-actuation update' to install.")
            return

        confirm = input("\nDo you want to update now? [y/N] ").strip().lower()
        if confirm != 'y':
            print("[*] Update cancelled.")
            return

        # Construct filename (Assumes standard Windows asset naming)
        arch = 'x64' if platform.machine().endswith('64') else 'x86'
        file_name = f"windows-actuation-{latest_version}-win-{arch}.zip"
        
        download_url = f"https://github.com/{REPO}/releases/download/{latest_tag}/{file_name}"
        print(f"\n[*] Downloading {file_name}...")

        # Download
        download_response = requests.get(download_url, stream=True, timeout=30)
        download_response.raise_for_status()
        
        temp_dir = tempfile.mkdtemp()
        temp_file = os.path.join(temp_dir, file_name)
        
        with open(temp_file, 'wb') as f:
            for chunk in download_response.iter_content(chunk_size=8192):
                f.write(chunk)
                
        # Extract
        print("[*] Installing update...")
        with zipfile.ZipFile(temp_file, 'r') as zf:
            zf.extractall(temp_dir)

        # Replace Binary
        binary_name = 'windows-actuation.exe'
        extracted_bin = os.path.join(temp_dir, binary_name)
        
        if not os.path.exists(extracted_bin):
            # Check subfolders
            found = list(Path(temp_dir).rglob(binary_name))
            if found:
                extracted_bin = str(found[0])
            else:
                print(f"[✗] Error: Could not find '{binary_name}' in archive.")
                shutil.rmtree(temp_dir)
                return

        current_exe = sys.executable if getattr(sys, 'frozen', False) else __file__
        current_exe_path = Path(current_exe).resolve()

        try:
            # Windows requires renaming the running executable before replacement
            old_exe = current_exe_path.with_suffix('.old')
            if old_exe.exists():
                try: os.remove(old_exe)
                except: pass
            
            os.rename(current_exe_path, old_exe)
            shutil.copy2(extracted_bin, current_exe_path)
            
            print(f"\n[✓] Successfully updated to v{latest_version}!")
            print("[*] Please restart the tool.")
            
        except OSError as e:
            print(f"[✗] OS Error: {e}")
            print("[!] On Windows, you may need to close the tool manually to complete the update.")
        except Exception as e:
            print(f"[✗] Failed to replace binary: {e}")
                
        finally:
            shutil.rmtree(temp_dir)

    except Exception as e:
        print(f"[✗] Update failed: {e}")

# Uninstallation mechanism
def uninstall_tool():
    """Uninstall the tool from the system"""
    print("=" * 50)
    print("Windows Actuation Control - Uninstall")
    print("=" * 50)
    
    # 1. Confirm intent
    confirm = input("\nAre you sure you want to uninstall this tool? [y/N] ").strip().lower()
    if confirm != 'y':
        print("[*] Uninstall cancelled.")
        return

    # 2. Identify the file to remove
    if getattr(sys, 'frozen', False):
        target_path = Path(sys.executable).resolve()
    else:
        target_path = Path(__file__).resolve()

    print(f"\n[*] Target: {target_path}")

    try:
        # 3. Perform removal
        trash_path = target_path.with_suffix('.old_del')
        
        # Clean up previous debris if it exists
        if trash_path.exists():
            try: trash_path.unlink()
            except: pass
        
        # Rename current executable
        target_path.rename(trash_path)
        
        # Schedule deletion after process exits
        cmd = f'cmd /c ping 127.0.0.1 -n 3 > nul & del "{trash_path}"'
        subprocess.Popen(cmd, shell=True)
        
        print("[✓] Uninstallation initiated.")
        print("    The file will be removed automatically in a few seconds.")
        
        sys.exit(0)

    except Exception as e:
        print(f"[✗] Uninstall failed: {e}")
        print(f"    Please delete '{target_path.name}' manually.")

# Main entry point
def main():
    """Main entry point"""
    import argparse

    if len(sys.argv) > 1:
        if sys.argv[1] == 'version':
            show_version()
            sys.exit(0)
        elif sys.argv[1] == 'update':
            check_only = '--check-only' in sys.argv
            update_tool(check_only=check_only)
            sys.exit(0)
        elif sys.argv[1] == 'uninstall':
            uninstall_tool()
            sys.exit(0)
    
    parser = argparse.ArgumentParser(description='Windows VM Control CLI')
    parser.add_argument('-f', '--file', help='Execute commands from file (batch mode)')
    parser.add_argument('-c', '--command', help='Execute single command and exit')
    parser.add_argument('-d', '--delay', type=float, default=0.1, help='Delay between batch commands (seconds)')
    parser.add_argument('--host', default='localhost', help='Host (default: localhost)')
    parser.add_argument('--username', help='Username for SSH connection')
    parser.add_argument('--password', help='Password (not recommended, use prompt instead)')
    parser.add_argument('--port', type=int, default=2222, help='SSH port (default: 2222)')
    
    args = parser.parse_args()
    
    print("╔══════════════════════════════════════════════════════════╗")
    print("║         Windows VM Control CLI - CUA Integration        ║")
    print("╚══════════════════════════════════════════════════════════╝\n")
    
    # Get connection details
    host = input("Host (default: localhost): ").strip() or "localhost"
    username = input("Username: ").strip()
    
    if not username:
        print("[✗] Username is required")
        sys.exit(1)
    
    password = getpass.getpass("Password: ")
    
    # Create controller
    controller = VMController(host=host, username=username, port=2222)
    
    # Connect
    if not controller.connect(password):
        sys.exit(1)
    
    # Enter interactive mode
    controller.interactive_mode()

# Main entry point
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[*] Interrupted. Exiting...")
        sys.exit(0)