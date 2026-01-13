# Windows Actuation Control - Complete Documentation

**Version:** 1.0.0  
**Last Updated:** January 2026  
**Developer:** Kartik (NullVoider)

---

## Table of Contents

1. [Overview](#overview)
2. [Key Features](#key-features)
3. [Capability Summary](#capability-summary)
4. [Technical Specifications](#technical-specifications)
5. [Installation & Setup](#installation--setup)
6. [Usage Modes](#usage-modes)
7. [Syntax Reference](#syntax-reference)
8. [Examples](#examples)
9. [Troubleshooting](#troubleshooting)
10. [Appendix](#appendix)

---

## Overview

The Windows Actuation Control is an intelligent middleware tool designed for Computer Use Agents (CUA) to remotely control Windows virtual machines via SSH. It uses a file-based command queue system with AutoHotkey v2 watcher services for reliable mouse and keyboard automation.

### Architecture

```
┌─────────────────┐         SSH          ┌──────────────────────┐
│  Client Machine │ ◄─────────────────►  │      Windows VM      │
│  (Python CLI)   │     Port 2222        │                      │
└─────────────────┘                      │  ┌────────────────┐  │
                                         │  │ mouse_cmd.txt  │  │
                                         │  └────────────────┘  │
                                         │  ┌────────────────┐  │
                                         │  │keyboard_cmd.txt│  │
                                         │  └────────────────┘  │
                                         │  ┌────────────────┐  │
                                         │  │ AHK Watchers   │  │
                                         │  │ (Background)   │  │
                                         │  └────────────────┘  │
                                         └──────────────────────┘
```

**How It Works:**
1. Windows Actuation Control CLI connects via SSH and writes commands to text files (`C:\mouse_cmd.txt`, `C:\keyboard_cmd.txt`)
2. AutoHotkey watcher services poll these files every 50ms
3. When a command is detected, AHK executes it and deletes the file
4. This bypasses SSH session isolation issues on Windows

---

## Key Features

### 🎯 **Core Advantages**
- ✅ **File-Based Queue** - Bypasses SSH session 0 limitations
- ✅ **Auto-Start on Boot** - Watchers run automatically via Task Scheduler
- ✅ **Zero UI Required** - Pure command-line interface
- ✅ **SSH-Secured** - All communication over encrypted SSH
- ✅ **Smart Detection** - Automatically detects command type (mouse/keyboard)
- ✅ **Batch Processing** - Execute multiple commands from files
- ✅ **Interactive Mode** - Real-time control with command prompt
- ✅ **Cross-Platform Client** - Runs on any system with Python 3.x

### 🛡️ **Reliability Features**
- Single-instance protection (prevents duplicate watchers)
- Silent execution (no popup windows)
- Error-tolerant (crashes don't affect watcher loop)
- Stabilization delays (500ms keyboard, 200ms mouse)
- Smooth dragging (speed 50 for natural movement)

---

## Capability Summary

### 🖱️ Mouse Control Capabilities

| Capability | Description | Performance |
|------------|-------------|-------------|
| **Movement** | Move cursor to exact coordinates | Instant (0ms animation) |
| **Clicking** | Left, right, middle, double clicks | 100% reliable |
| **Dragging** | Smooth click-drag-release operations | Speed 50 (natural) |
| **Scrolling** | Up/down scrolling with custom amounts | 3 notches default |
| **Hold/Release** | Manual drag control (hold, move, release) | Full control |
| **Here Actions** | Actions at current cursor position | Position-aware |

**Supported Actions:**
- `move` - Move cursor only
- `left` - Left-click
- `right` - Right-click (context menu)
- `middle` - Middle-click
- `double` - Double left-click
- `scroll_up [n]` - Scroll up N notches (default: 3)
- `scroll_down [n]` - Scroll down N notches (default: 3)
- `drag` - Click-drag-release operation
- `hold` - Press and hold mouse button
- `release` - Release mouse button
- `here <action>` - Perform action at current position

### ⌨️ Keyboard Control Capabilities

| Capability | Description | Support Level |
|------------|-------------|---------------|
| **Text Typing** | Type arbitrary text (literal characters) | Full |
| **Modifiers** | Ctrl (^), Shift (+), Alt (!), Win (#) | All supported |
| **Navigation Keys** | Arrows, Home, End, PgUp, PgDn | Full support |
| **Special Keys** | Enter, Tab, Esc, Space, Delete, Backspace | All functional |
| **Function Keys** | F1-F12 | Hardware-dependent |
| **Shortcuts** | Multi-modifier combinations | Unlimited |

**Supported Actions:**
- `type <text>` - Type literal text (safe for passwords, special chars)
- `press <keys>` - Press keys with modifiers and special keys

**Modifier Syntax:**
- `^` - Ctrl
- `+` - Shift  
- `!` - Alt
- `#` - Windows key

**Special Keys:**
- `{Enter}`, `{Esc}`, `{Tab}`, `{Space}`
- `{Backspace}`, `{BS}`, `{Delete}`, `{Del}`
- `{Up}`, `{Down}`, `{Left}`, `{Right}`
- `{Home}`, `{End}`, `{PgUp}`, `{PgDn}`
- `{F1}` through `{F12}`
- `{LWin}`, `{RWin}` (Windows key)

### 🔧 System Features

| Feature | Description |
|---------|-------------|
| **Auto-Start** | Watchers start automatically via Task Scheduler |
| **User Session** | Runs in user session (not Session 0) |
| **File-Based Queue** | Bypasses SSH session isolation issues |
| **Silent Execution** | No UI dialogs or windows |
| **Error Handling** | Crashes don't affect watcher loop |
| **Single-Instance** | Prevents duplicate watchers |
| **Fast Polling** | 50ms interval for responsive control |
| **Command Logging** | All executed commands logged to output |

---

## Technical Specifications

### System Requirements

**Server (Windows VM):**
- Windows 10 or Windows 11
- AutoHotkey v2.0+ installed
- SSH server enabled (OpenSSH or alternative)
- User session must be logged in (not locked)
- Administrative privileges (for Task Scheduler setup)

**Client (Control Machine):**
- Python 3.7 or later
- `paramiko` library (SSH client)
- Network access to Windows VM

### Dependencies

```bash
# Server-side (Windows VM)
# Download AutoHotkey v2 from: https://www.autohotkey.com/
# Install to: C:\Program Files\AutoHotkey\v2\

# Place scripts in: C:\Program Files\AutoHotkey\
# - mouse_control.ahk
# - keyboard_control.ahk

# Client-side (Control Machine)
pip install paramiko
```

### Performance Metrics

| Operation | Latency | Throughput |
|-----------|---------|------------|
| Mouse Move | ~20-50ms | 50-100 ops/sec |
| Click | ~30-60ms | 30-50 ops/sec |
| Type Character | ~10-20ms | 50+ chars/sec |
| Scroll | ~50-100ms | 20-30 ops/sec |
| Keyboard Shortcut | ~40-80ms | 20-40 ops/sec |
| Drag Operation | ~200-400ms | 5-10 ops/sec |

*Note: Includes network overhead. Stabilization delays built-in for reliability.*

### Timing Specifications

| Parameter | Value | Purpose |
|-----------|-------|---------|
| Polling Interval | 50ms | File check frequency |
| Keyboard Stabilization | 500ms | Wait before typing |
| Mouse Stabilization | 200ms | Wait after movement |
| Key Delay | 50ms | Inter-key delay |
| Drag Speed | 50 | Smooth dragging (0-100 scale) |
| Post-Action Sleep | 100ms | Safety delay |

---

## Installation & Setup

### Step 1: Install AutoHotkey v2

1. **Download AutoHotkey v2:**
   - Visit: https://www.autohotkey.com/
   - Download AutoHotkey v2 (NOT v1.1)
   - Run installer, select default installation path

2. **Verify Installation:**
   ```powershell
   Test-Path "C:\Program Files\AutoHotkey\v2\AutoHotkey.exe"
   # Should return: True
   ```

### Step 2: Install Control Scripts

1. **Download Scripts:**
   - `mouse_control.ahk`
   - `keyboard_control.ahk`

2. **Place Scripts in AutoHotkey Directory:**
   ```powershell
   # Copy to:
   C:\Program Files\AutoHotkey\mouse_control.ahk
   C:\Program Files\AutoHotkey\keyboard_control.ahk
   ```

3. **Verify Placement:**
   ```powershell
   Test-Path "C:\Program Files\AutoHotkey\mouse_control.ahk"
   Test-Path "C:\Program Files\AutoHotkey\keyboard_control.ahk"
   # Both should return: True
   ```

### Step 3: Enable SSH Server

#### Option A: OpenSSH (Windows 10/11 Built-in)

```powershell
# Install OpenSSH Server
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0

# Start SSH service
Start-Service sshd

# Set to auto-start on boot
Set-Service -Name sshd -StartupType 'Automatic'

# Verify it's running
Get-Service sshd
# Status should be: Running

# Allow SSH through firewall (if needed, but compulsory for Windows 11)
New-NetFirewallRule -Name sshd -DisplayName 'OpenSSH Server (sshd)' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22
```

#### Option B: Custom SSH Port (2222)

If using port 2222 instead of default 22:

```powershell
# Edit SSH config
notepad C:\ProgramData\ssh\sshd_config

# Change line:
# Port 22
# To:
Port 2222

# Restart SSH service
Restart-Service sshd

# Update firewall rule
New-NetFirewallRule -Name sshd-2222 -DisplayName 'OpenSSH Server (Port 2222)' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 2222
```

### Step 4: Configure Auto-Start (Task Scheduler)

#### Windows 10 Setup

**Mouse Watcher:**
```powershell
$MouseArg = '/c start /min "" "C:\Program Files\AutoHotkey\v2\AutoHotkey.exe" "C:\Program Files\AutoHotkey\mouse_control.ahk" watcher'
$ActionMouse = New-ScheduledTaskAction -Execute "cmd.exe" -Argument $MouseArg
$Trigger = New-ScheduledTaskTrigger -AtLogOn -User "AgentUser"
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit 0 -Hidden
$Principal = New-ScheduledTaskPrincipal -UserId "AgentUser" -LogonType Interactive -RunLevel Highest
Register-ScheduledTask -TaskName "MouseControlWatcher" -Action $ActionMouse -Trigger $Trigger -Settings $Settings -Principal $Principal
```

**Keyboard Watcher:**
```powershell
$KeyboardArg = '/c start /min "" "C:\Program Files\AutoHotkey\v2\AutoHotkey.exe" "C:\Program Files\AutoHotkey\keyboard_control.ahk" watcher'
$ActionKey = New-ScheduledTaskAction -Execute "cmd.exe" -Argument $KeyboardArg
$Trigger = New-ScheduledTaskTrigger -AtLogOn -User "AgentUser"
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit 0 -Hidden
$Principal = New-ScheduledTaskPrincipal -UserId "AgentUser" -LogonType Interactive -RunLevel Highest
Register-ScheduledTask -TaskName "KeyboardControlWatcher" -Action $ActionKey -Trigger $Trigger -Settings $Settings -Principal $Principal
```

#### Windows 11 Setup

**Mouse Watcher:**
```powershell
$MouseArg = '/c start /min "" "C:\Program Files\AutoHotkey\v2\AutoHotkey.exe" "C:\Program Files\AutoHotkey\mouse_control.ahk" watcher'
$ActionMouse = New-ScheduledTaskAction -Execute "cmd.exe" -Argument $MouseArg
$CurrentUser = "$env:USERDOMAIN\$env:USERNAME"
$Trigger = New-ScheduledTaskTrigger -AtLogOn -User $CurrentUser
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit 0 -Hidden
$Principal = New-ScheduledTaskPrincipal -UserId $CurrentUser -LogonType Interactive -RunLevel Highest
Register-ScheduledTask -TaskName "MouseControlWatcher" -Action $ActionMouse -Trigger $Trigger -Settings $Settings -Principal $Principal -Description "Monitors for remote mouse control commands"
```

**Keyboard Watcher:**
```powershell
$KeyboardArg = '/c start /min "" "C:\Program Files\AutoHotkey\v2\AutoHotkey.exe" "C:\Program Files\AutoHotkey\keyboard_control.ahk" watcher'
$ActionKey = New-ScheduledTaskAction -Execute "cmd.exe" -Argument $KeyboardArg
$CurrentUser = "$env:USERDOMAIN\$env:USERNAME"
$Trigger = New-ScheduledTaskTrigger -AtLogOn -User $CurrentUser
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit 0 -Hidden
$Principal = New-ScheduledTaskPrincipal -UserId $CurrentUser -LogonType Interactive -RunLevel Highest
Register-ScheduledTask -TaskName "KeyboardControlWatcher" -Action $ActionKey -Trigger $Trigger -Settings $Settings -Principal $Principal -Description "Monitors for remote keyboard control commands"
```

### Step 5: Start Watchers Immediately

```powershell
# Start both watchers
Start-ScheduledTask -TaskName "MouseControlWatcher"
Start-ScheduledTask -TaskName "KeyboardControlWatcher"

# Verify they're running
Get-Process | Where-Object {$_.ProcessName -eq "AutoHotkey"}
# Should see 2 AutoHotkey processes
```

### Step 6: Install Python Client Dependencies

```bash
# On control machine
pip install paramiko
```

### Step 7: Download & Install

**Option A: One-Line Installer (Recommended)**
This automatically detects your OS, downloads the latest binary, and adds it to your PATH.

* **Linux & macOS:**
    ```bash
    curl -fsSL https://raw.githubusercontent.com/nullvoider07/windows_actuation_control/main/install/install.sh | bash
    ```

* **Windows (PowerShell):**
    ```powershell
    irm https://raw.githubusercontent.com/nullvoider07/windows_actuation_control/main/install/install.ps1 | iex
    ```

**Option B: Manual Download**
If you prefer, download the standalone binary for your OS directly from the [Releases Page](https://github.com/nullvoider07/windows_actuation_control/releases).

### Troubleshooting Installation

**If Watchers Don't Start:**
```powershell
# Check Task Scheduler tasks exist
Get-ScheduledTask | Where-Object {$_.TaskName -like "*ControlWatcher*"}

# Check last run result
Get-ScheduledTaskInfo -TaskName "MouseControlWatcher"
Get-ScheduledTaskInfo -TaskName "KeyboardControlWatcher"

# Remove and re-create if needed
Unregister-ScheduledTask -TaskName "MouseControlWatcher" -Confirm:$false
Unregister-ScheduledTask -TaskName "KeyboardControlWatcher" -Confirm:$false
# Then re-run registration commands
```

**If AutoHotkey Not Found:**
```powershell
# Verify AutoHotkey v2 is installed
Get-ItemProperty "C:\Program Files\AutoHotkey\v2\AutoHotkey.exe" | Select-Object VersionInfo
```

---

## Usage Modes

### 1. Interactive Mode (Default)

```bash
python3 windows_actuation_control.py --username AgentUser --host localhost --port 2222
```

**Features:**
- Real-time command execution
- Command history
- Auto-detection of command types
- `help` command for quick reference
- `exit` or `quit` to disconnect

**Example Session:**
```
VM> 960 540 left
[MOUSE] Executed: 960 540 left

VM> type Hello World
[KEYBOARD] Executed: type Hello World

VM> press ^c
[KEYBOARD] Executed: press ^c

VM> exit
[*] Exiting...
[*] Disconnected from VM
```

### 2. Single Command Mode

```bash
python3 windows_actuation_control.py -c "960 540 right" --username AgentUser --host localhost --port 2222
```

**Use Cases:**
- Quick one-off operations
- Scripting integrations
- API-like execution
- Automated workflows

**Examples:**
```bash
# Right-click at position
python3 windows_actuation_control.py -c "960 540 right" --username AgentUser

# Type text
python3 windows_actuation_control.py -c "type Hello World" --username AgentUser

# Press shortcut
python3 windows_actuation_control.py -c "press ^v" --username AgentUser
```

### 3. Batch Mode (File Execution)

```bash
python3 windows_actuation_control.py -f commands.txt -d 0.5 --username AgentUser --host localhost --port 2222
```

**File Format:** (`commands.txt`)
```
# This is a comment - ignored by the parser
# Empty lines are also ignored

# Open Run dialog and launch Notepad
press #r
type notepad
press {Enter}

# Wait for Notepad to open (use -d flag for delays)
# Then type some text
type Hello from batch mode!
press {Enter}
type This is line 2
```

**Batch Mode Options:**
- `-f` / `--file` - Specify command file path
- `-d` / `--delay` - Delay in seconds between commands (default: 0.1)

---

## Syntax Reference

### Mouse Commands

#### Basic Format
```
<x> <y> <action> [parameters]
```

#### Actions Reference

| Command | Syntax | Description | Example |
|---------|--------|-------------|---------|
| **Move** | `<x> <y> move` | Move cursor to coordinates | `500 400 move` |
| **Left Click** | `<x> <y> left` | Move and left-click | `960 540 left` |
| **Right Click** | `<x> <y> right` | Move and right-click | `960 540 right` |
| **Middle Click** | `<x> <y> middle` | Move and middle-click | `960 540 middle` |
| **Double Click** | `<x> <y> double` | Move and double-click | `640 360 double` |
| **Hold** | `<x> <y> hold` | Press and hold mouse button | `500 500 hold` |
| **Release** | `<x> <y> release` | Release mouse button | `700 700 release` |
| **Drag** | `<x> <y> drag <x2> <y2>` | Drag from (x,y) to (x2,y2) | `100 100 drag 500 500` |
| **Scroll Up** | `<x> <y> scroll_up [n]` | Scroll up N notches | `960 540 scroll_up 5` |
| **Scroll Down** | `<x> <y> scroll_down [n]` | Scroll down N notches | `960 540 scroll_down 10` |

**Notes:**
- Coordinates are in screen pixels (e.g., 1920x1080)
- Mouse moves instantly (0ms animation)
- 200ms stabilization delay after movement
- Default scroll amount: 3 notches
- Drag speed: 50 (smooth, natural movement)

#### "Here" Actions (Current Position)

| Command | Syntax | Description |
|---------|--------|-------------|
| **Here + Left** | `here left` | Click at current position |
| **Here + Right** | `here right` | Right-click at current position |
| **Here + Double** | `here double` | Double-click at current position |
| **Here + Middle** | `here middle` | Middle-click at current position |
| **Here + Scroll** | `here scroll_down 5` | Scroll at current position |
| **Here + Drag** | `here drag 800 600` | Drag from current to (800,600) |

### Keyboard Commands

#### Basic Format
```
<action> <content>
```

#### Actions

| Command | Syntax | Description | Example |
|---------|--------|-------------|---------|
| **Type** | `type <text>` | Type literal text | `type Hello World` |
| **Press** | `press <keys>` | Press key/shortcut | `press ^c` |

#### Navigation Keys

```
{Enter}                      - Enter key
{Esc}                        - Escape key
{Tab}                        - Tab key
{Space}                      - Space bar
{Backspace}  or {BS}         - Backspace (delete left)
{Delete}     or {Del}        - Delete key (delete right)
{Up}                         - Arrow up
{Down}                       - Arrow down
{Left}                       - Arrow left
{Right}                      - Arrow right
{Home}                       - Home (jump to line start)
{End}                        - End (jump to line end)
{PgUp}                       - Page up
{PgDn}                       - Page down
```

#### Function Keys

```
{F1}, {F2}, {F3}, {F4}, {F5}, {F6}
{F7}, {F8}, {F9}, {F10}, {F11}, {F12}
```

#### Windows-Specific Keys

```
{LWin}                       - Left Windows key
{RWin}                       - Right Windows key
```

#### Modifier Syntax

| Symbol | Modifier | Example | Description |
|--------|----------|---------|-------------|
| `^` | Ctrl | `^c` | Ctrl+C (Copy) |
| `+` | Shift | `+a` | Shift+A (uppercase) |
| `!` | Alt | `!{F4}` | Alt+F4 (Close window) |
| `#` | Windows | `#r` | Win+R (Run dialog) |

#### Multi-Modifier Combinations

```
^+{Esc}                      - Ctrl+Shift+Esc (Task Manager)
!{Tab}                       - Alt+Tab (Window switcher)
#+s                          - Win+Shift+S (Screenshot tool)
^!{Delete}                   - Ctrl+Alt+Delete
```

### Auto-Detection Rules

The CLI automatically detects command types:

| Input Pattern | Detected As | Example |
|---------------|-------------|---------|
| `<num> <num>` | Mouse move | `500 400` → `500 400 move` |
| `<num> <num> <action>` | Mouse action | `500 400 right` |
| `here <action>` | Mouse at current pos | `here left` |
| `type <text>` | Keyboard typing | `type Hello` |
| `press <keys>` | Keyboard shortcut | `press ^c` |
| `^<char>` | Keyboard shortcut | `^c` → `press ^c` |
| `{Key}` | Special key press | `{Enter}` → `press {Enter}` |
| `<plain text>` | Type text | `Hello` → `type Hello` |

---

## Examples

### Basic Mouse Operations

```bash
# Move cursor to center of 1920x1080 screen
960 540 move

# Left-click at position
960 540 left

# Right-click to open context menu
960 540 right

# Double-click to open file/folder
640 360 double

# Middle-click (open link in new tab)
500 300 middle

# Click at current cursor position
here left
```

### Scrolling

```bash
# Scroll down in a browser (default 3 notches)
960 540 scroll_down

# Scroll up with custom amount (10 notches)
960 540 scroll_up 10

# Scroll at current cursor position
here scroll_down 5
```

### Drag & Drop

```bash
# Drag a file from (300,300) to (700,700)
300 300 drag 700 700

# Manual drag (for complex paths)
500 500 hold
# ... do something else if needed ...
700 700 release

# Drag from current position
here drag 800 600
```

### Text Typing

```bash
# Type simple text
type Hello World

# Type with special characters (literal)
type Price: $100 @ 50% off!

# Type passwords (safe - no key interpretation)
type MySecureP@ss123!

# Type code with special chars
type if (x > 5) { return true; }

# Type email
type user@example.com
```

### Keyboard Shortcuts

```bash
# Copy (Ctrl+C)
press ^c

# Paste (Ctrl+V)
press ^v

# Select All (Ctrl+A)
press ^a

# Cut (Ctrl+X)
press ^x

# Undo (Ctrl+Z)
press ^z

# Redo (Ctrl+Y)
press ^y

# Save (Ctrl+S)
press ^s

# Find (Ctrl+F)
press ^f

# New Tab (Ctrl+T)
press ^t

# Close Tab (Ctrl+W)
press ^w
```

### Windows System Shortcuts

```bash
# Open Run dialog (Win+R)
press #r

# Lock screen (Win+L)
press #l

# Task Manager (Ctrl+Shift+Esc)
press ^+{Esc}

# Alt+Tab (Window switcher)
press !{Tab}

# Close window (Alt+F4)
press !{F4}

# Screenshot tool (Win+Shift+S) - Windows 11
press #+s

# Quick Settings (Win+A) - Windows 11
press #a

# Notifications (Win+N) - Windows 11
press #n

# Widgets (Win+W) - Windows 11
press #w

# Desktop (Win+D)
press #d

# File Explorer (Win+E)
press #e
```

### Navigation

```bash
# Press Enter
press {Enter}

# Press Tab (move to next field)
press {Tab}

# Press Escape
press {Esc}

# Arrow navigation
press {Up}
press {Down}
press {Left}
press {Right}

# Jump to beginning/end of line
press {Home}
press {End}

# Page navigation
press {PgUp}
press {PgDn}

# Delete characters
press {Backspace}
press {Delete}

# Refresh page (F5)
press {F5}
```

### Complex Workflows

#### Example 1: Open Notepad and Type Text
```bash
# 1. Open Run dialog
press #r

# 2. Type "notepad"
type notepad

# 3. Press Enter to launch
press {Enter}

# 4. Type some text
type Hello from Windows automation!

# 5. Press Enter for new line
press {Enter}

# 6. Type more text
type This is line 2
```

#### Example 2: Copy Text and Paste to Another Window
```bash
# 1. Select all text in current window
press ^a

# 2. Copy
press ^c

# 3. Switch window (Alt+Tab)
press !{Tab}

# 4. Paste
press ^v
```

#### Example 3: Right-Click Menu Navigation
```bash
# 1. Right-click at coordinates
500 500 right

# 2. Navigate menu with arrow keys
press {Down}
press {Down}

# 3. Select option
press {Enter}
```

#### Example 4: Drag and Drop File
```bash
# 1. Click on file
300 400 left

# 2. Drag to destination folder
300 400 drag 800 200
```

#### Example 5: Fill Web Form
```bash
# 1. Click first input field
500 300 left

# 2. Type username
type john.doe@example.com

# 3. Tab to next field
press {Tab}

# 4. Type password
type MySecureP@ss123

# 5. Press Enter to submit
press {Enter}
```

#### Example 6: Take Screenshot and Save
```bash
# 1. Open screenshot tool (Win+Shift+S)
press #+s

# 2. Click and drag to select area
300 300 drag 1600 900

# 3. Open Paint (Win+R, then type mspaint)
press #r
type mspaint
press {Enter}

# 4. Paste screenshot
press ^v

# 5. Save file
press ^s
```

#### Example 7: Search in File Explorer
```bash
# 1. Open File Explorer (Win+E)
press #e

# 2. Click search box
1400 100 left

# 3. Type search term
type *.pdf

# 4. Press Enter to search
press {Enter}
```

### Batch File Examples

#### Example 1: Open Calculator and Perform Calculation

**File:** `calculator.txt`
```
# Open Run dialog
press #r

# Type calc
type calc

# Press Enter
press {Enter}

# Type calculation (assumes Calculator is in standard mode)
type 123
press +
type 456
press {Enter}
```

**Execute:**
```bash
python3 windows_actuation_control.py -f calculator.txt -d 1.0 --username AgentUser
```

#### Example 2: Create Text File on Desktop

**File:** `create_file.txt`
```
# Open Notepad
press #r
type notepad
press {Enter}

# Type content
type This is a test file
press {Enter}
type Created via automation
press {Enter}
type Line 3 with special chars: $100 @ 50%

# Save file (Ctrl+S)
press ^s

# Type filename in save dialog
type test_automation.txt

# Save to Desktop
press {Tab}
press {Tab}
type Desktop
press {Enter}
```

**Execute:**
```bash
python3 windows_actuation_control.py -f create_file.txt -d 1.5 --username AgentUser
```

#### Example 3: Browser Automation

**File:** `browser_test.txt`
```
# Open browser (assumes Edge/Chrome set as default)
press #r
type msedge
press {Enter}

# Wait for browser to open
# Navigate to URL (Ctrl+L to focus address bar)
press ^l

# Type URL
type https://www.example.com
press {Enter}

# Scroll down page
960 540 scroll_down 10

# Click a link at specific position
500 600 left
```

**Execute:**
```bash
python3 windows_actuation_control.py -f browser_test.txt -d 2.0 --username AgentUser
```

---

## Troubleshooting

### Common Issues

#### 1. "Connection refused" or "SSH not connecting"

**Problem:** Can't connect via SSH

**Solutions:**
```powershell
# Verify SSH service is running
Get-Service sshd
# Status should be: Running

# If not running, start it
Start-Service sshd

# Verify it's set to auto-start
Get-Service sshd | Select-Object StartType
# Should be: Automatic

# Check firewall rules
Get-NetFirewallRule -Name sshd
# Should exist and be enabled

# Test SSH locally first
ssh username@localhost -p 2222
```

#### 2. "Commands not executing" or "Nothing happens"

**Problem:** Commands sent but no visible effect

**Solutions:**
```powershell
# Check if watchers are running
Get-Process | Where-Object {$_.ProcessName -eq "AutoHotkey"}
# Should see 2 AutoHotkey processes

# If not running, start them
Start-ScheduledTask -TaskName "MouseControlWatcher"
Start-ScheduledTask -TaskName "KeyboardControlWatcher"

# Check for command files (should be deleted after execution)
Test-Path C:\mouse_cmd.txt
Test-Path C:\keyboard_cmd.txt
# Both should return: False (files are deleted after execution)

# Test watchers manually
Start-Process "C:\Program Files\AutoHotkey\v2\AutoHotkey.exe" -ArgumentList "C:\Program Files\AutoHotkey\mouse_control.ahk","watcher"
```

#### 3. "Watcher tasks fail at boot"

**Problem:** Scheduled tasks show errors in Task Scheduler

**Solutions:**
```powershell
# Check task status
Get-ScheduledTaskInfo -TaskName "MouseControlWatcher"
Get-ScheduledTaskInfo -TaskName "KeyboardControlWatcher"

# Check last run result (should be 0 for success)
# If not 0, unregister and re-create tasks

# Remove tasks
Unregister-ScheduledTask -TaskName "MouseControlWatcher" -Confirm:$false
Unregister-ScheduledTask -TaskName "KeyboardControlWatcher" -Confirm:$false

# Re-create using setup commands from Installation section
# Make sure to use CORRECT username (replace "AgentUser" with your actual username)
```

#### 4. "AutoHotkey not found" error

**Problem:** Task Scheduler can't find AutoHotkey

**Solutions:**
```powershell
# Verify AutoHotkey v2 is installed
Test-Path "C:\Program Files\AutoHotkey\v2\AutoHotkey.exe"
# Should return: True

# If False, reinstall AutoHotkey v2
# Download from: https://www.autohotkey.com/

# Verify scripts exist
Test-Path "C:\Program Files\AutoHotkey\mouse_control.ahk"
Test-Path "C:\Program Files\AutoHotkey\keyboard_control.ahk"
# Both should return: True
```

#### 5. "Mouse moves but doesn't click"

**Problem:** Cursor moves to position but click doesn't register

**Solutions:**
- Increase stabilization delay in `mouse_control.ahk` (change `Sleep 200` to `Sleep 500`)
- Ensure target window is not requesting admin privileges
- Check if UAC prompts are blocking clicks
- Try using `here left` after manual cursor positioning

#### 6. "Keyboard shortcuts not working"

**Problem:** `press ^c`, `press ^v` etc. don't work

**Solutions:**
```powershell
# Verify keyboard watcher is running
Get-Process | Where-Object {$_.ProcessName -eq "AutoHotkey"} | Select-Object Id, ProcessName, StartTime

# Test keyboard manually
echo "press ^c" > C:\keyboard_cmd.txt
# Should disappear within 50ms if watcher is working

# Check for caret escape issues in SSH
# Make sure command uses: echo press ^^c (double caret)
# Python CLI handles this automatically
```

#### 7. "Drag operation jerky or too fast"

**Problem:** Dragging doesn't look smooth

**Solutions:**
- Adjust drag speed in `mouse_control.ahk`
- Change `MouseMove dest_x, dest_y, 50` to lower number (e.g., `25` for smoother)
- Increase sleeps before/after drag
- Check CPU usage - high CPU can cause stuttering

#### 8. "Text typing has special characters showing as keys"

**Problem:** Typing `$100` shows as `{Shift}4100`

**Solutions:**
- Use `type` command instead of `press`: `type $100` (NOT `press $100`)
- The `type` action sends literal characters safely
- The `press` action interprets special syntax like `{Shift}`, `^`, etc.

#### 9. "Commands delayed or slow"

**Problem:** Noticeable lag between commands

**Solutions:**
- Reduce batch delay: `python3 ... -f commands.txt -d 0.05`
- Check network latency: `ping your-vm-ip`
- Verify VM has adequate resources (CPU, RAM)
- Check if antivirus is scanning AutoHotkey processes

#### 10. "Permission denied" errors

**Problem:** Can't write to `C:\mouse_cmd.txt` or `C:\keyboard_cmd.txt`

**Solutions:**
```powershell
# Verify user has write permissions
$acl = Get-Acl "C:\"
$acl.Access | Where-Object {$_.IdentityReference -like "*$env:USERNAME*"}

# If needed, ensure user session is active (not locked)
# Commands only work when user is logged in

# Test write permission
echo "test" > C:\test.txt
# Should succeed without errors
```

### Debug Mode

**Enable Verbose Logging:**

1. **Modify AutoHotkey scripts** to show tooltips:

```autohotkey
; Add this to ExecuteCommand function in mouse_control.ahk
ToolTip "Executing: " action " at " x "," y
Sleep 1000
ToolTip
```

2. **Monitor command files:**
```powershell
# Watch for file creation/deletion
while ($true) {
    if (Test-Path C:\mouse_cmd.txt) {
        Get-Content C:\mouse_cmd.txt
    }
    if (Test-Path C:\keyboard_cmd.txt) {
        Get-Content C:\keyboard_cmd.txt
    }
    Start-Sleep -Milliseconds 100
}
```

3. **Test watchers directly:**
```powershell
# Run watcher in visible window (not minimized)
Start-Process "C:\Program Files\AutoHotkey\v2\AutoHotkey.exe" -ArgumentList "C:\Program Files\AutoHotkey\mouse_control.ahk","watcher" -NoNewWindow -Wait
```

### Getting Help

If issues persist:
1. Verify AutoHotkey v2 is installed (NOT v1.1)
2. Test scripts manually (run .ahk files directly)
3. Check Windows Event Viewer for errors
4. Verify SSH connection works independently
5. Review Python CLI output for error messages

---

## Appendix

### Complete Command Reference Card

```
MOUSE COMMANDS
--------------
<x> <y> move               - Move cursor
<x> <y> left               - Left-click
<x> <y> right              - Right-click
<x> <y> middle             - Middle-click
<x> <y> double             - Double-click
<x> <y> drag <x2> <y2>     - Drag from (x,y) to (x2,y2)
<x> <y> hold               - Hold button
<x> <y> release            - Release button
<x> <y> scroll_up [n]      - Scroll up N notches
<x> <y> scroll_down [n]    - Scroll down N notches
here <action>              - Action at cursor

KEYBOARD COMMANDS
-----------------
type <text>                - Type text (literal)
press <keys>               - Press keys/shortcuts

MODIFIERS
---------
^                          - Ctrl
+                          - Shift
!                          - Alt
#                          - Windows key

SPECIAL KEYS
------------
{Enter}, {Tab}, {Esc}, {Space}
{Backspace}, {BS}, {Delete}, {Del}
{Up}, {Down}, {Left}, {Right}
{Home}, {End}, {PgUp}, {PgDn}
{F1}-{F12}
{LWin}, {RWin}

COMMON SHORTCUTS
----------------
^c         - Copy
^v         - Paste
^x         - Cut
^a         - Select All
^z         - Undo
^y         - Redo
^s         - Save
^f         - Find
#r         - Run dialog
#l         - Lock screen
#e         - File Explorer
!{Tab}     - Window switcher
!{F4}      - Close window
^+{Esc}    - Task Manager
```

### System Compatibility

| Feature | Windows 10 | Windows 11 |
|---------|------------|------------|
| Mouse Control | ✅ Full | ✅ Full |
| Keyboard Control | ✅ Full | ✅ Full |
| Auto-Start | ✅ Works | ✅ Works |
| SSH Support | ✅ Built-in | ✅ Built-in |
| Task Scheduler | ✅ Compatible | ✅ Compatible |
| Win+X Shortcuts | ✅ Supported | ✅ Enhanced |
| Snap Layouts | ⚠️ Limited | ✅ Full |
| Widgets | ❌ N/A | ✅ Win+W |
| Quick Settings | ⚠️ Different | ✅ Win+A |

### Resolution Support

**Tested Resolutions:**
- 1920x1080 (Full HD) - Primary target
- 1280x720 (HD) - Supported
- 2560x1440 (2K) - Supported
- 3840x2160 (4K) - Supported

**Note:** Coordinates are absolute pixels. Adjust commands for your screen resolution.

### Known Limitations

1. **Session 0 Isolation** - Commands only work in user session (not system session)
2. **UAC Prompts** - Cannot interact with elevated permission dialogs
3. **Secure Desktop** - Cannot control lock screen, Ctrl+Alt+Del screen
4. **Full-Screen Apps** - May not work in exclusive full-screen mode
5. **Admin Windows** - Cannot click on windows running with higher privileges
6. **Sleep/Hibernate** - Watchers stop when system sleeps
7. **Fast User Switching** - Only works for currently logged-in user

### Performance Tuning

**For Faster Execution:**
```autohotkey
; In mouse_control.ahk, reduce sleep times:
Sleep 100  ; Change to: Sleep 50
Sleep 200  ; Change to: Sleep 100

; In keyboard_control.ahk:
Sleep 500  ; Change to: Sleep 250
SetKeyDelay 50, 50  ; Change to: SetKeyDelay 25, 25
```

**For More Reliable Execution:**
```autohotkey
; Increase stabilization delays:
Sleep 200  ; Change to: Sleep 300
Sleep 500  ; Change to: Sleep 750
```

### Alternative Access Methods

Besides SSH, the Windows VM can be accessed via:

1. **noVNC** (Web-based VNC) - Visual desktop access
2. **RDP** (Remote Desktop Protocol) - Native Windows remote access
3. **Direct Console** - Physical or hypervisor console access

The automation tools work with all access methods as they operate at the OS level.

---

## About This Project

This Windows Actuation Control tool was built from scratch to enable reliable remote automation of Windows environments. The file-based queue system was specifically designed to overcome SSH session isolation challenges on Windows, making it a robust solution for Computer Use Agents.

Every feature, every delay, and every line of code was iteratively tested and refined for maximum reliability. The combination of Python CLI, AutoHotkey watchers, and Task Scheduler auto-start creates a seamless automation experience.

If you find this tool useful, encounter bugs, or have feature requests, feel free to reach out directly via [X (formerly Twitter)](https://x.com/nullvoider07).

---

**Last Updated:** January 13, 2026  
**Developer:** Kartik (NullVoider)

---

**End of Documentation**