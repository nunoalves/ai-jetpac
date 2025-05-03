"""
ZX Spectrum Snapshot Memory Dumper via ZEsarUX (12.0) Remote Debugger
--------------------------------------------------------------

This script connects to the ZEsarUX emulator's remote debugger interface and 
allows a user to dump the entire 64 KB memory of a ZX Spectrum game to binary 
files on demand. When the user presses a key from '1' to '9', the script sends 
a `save-binary` command to ZEsarUX, saving the current memory contents to a file 
named `memory_dump_<key>.bin`.

This is primarily intended for Jetpac memory analysis, but is compatible with 
any Spectrum game running in ZEsarUX (12.0).

Typical use case:
- Capture memory state snapshots at critical gameplay moments
- Compare dumps to reverse engineer game logic or variable usage

Dependencies:
- ZEsarUX running with remote debugger enabled (`--remote-debug 1`)
- `keyboard` Python package (`pip install keyboard`)

Author: Nuno Alves
Date: 2025-May-03
"""

import socket
import keyboard
import time
import signal

HOST = 'localhost'
PORT = 10000

running = True

# Handle Ctrl+C to exit cleanly
def handle_sigint(sig, frame):
    global running
    print("\nTerminating...")
    running = False

signal.signal(signal.SIGINT, handle_sigint)
    
def wait_for_prompt(sock):
    buffer = ""
    sock.settimeout(1.0)
    while True:
        try:
            chunk = sock.recv(1024).decode(errors="ignore")
            buffer += chunk
            if "command>" in buffer:
                break
        except socket.timeout:
            break
    return buffer

def send_command(sock, command):
    sock.sendall((command + "\n").encode())
    return wait_for_prompt(sock)

def main():
    print("Connecting to ZEsarUX debugger...")
    with socket.create_connection((HOST, PORT)) as sock:
        print("Connected. Press 1 to 9 to save binary dumps.")
        wait_for_prompt(sock)  # flush startup prompt

        while running:
            for key in map(str, range(1, 10)):
                if keyboard.is_pressed(key):
                    filename = f"memory_dumpNuno Alves_{key}.bin"
                    command = f"save-binary {filename} 0 0"
                    print(f"Key '{key}' pressed! Sending command: {command}")
                    result = send_command(sock, command)
                    time.sleep(1.0)  # debounce so key isn't triggered repeatedly

        print("Disconnected.")

if __name__ == "__main__":
    main()