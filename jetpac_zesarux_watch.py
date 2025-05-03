import socket
import time
import signal
import sys

# Settings
HOST = 'localhost'
PORT = 10000
DELAY_BETWEEN_QUERIES_IN_SEC=0.2

# Memory address of Jetpac's number of lives counter (from disassembly):
# https://phillipeaton.github.io/jetpac-disassembly/
NUMBER_LIVES_ADDR = 24049 

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
            
    buffer=buffer.replace("command>","")
    buffer=buffer.strip()
    return buffer
    
def send_command(sock, command):
    sock.sendall((command + "\n").encode())
    return wait_for_prompt(sock)

def get_byte_from_memory(sock, address):    
    command = f"read-memory {address} 1"
    result = send_command(sock, command)    

    if (len(result) != 2):
        return None
 
    return(result)

def main():
    print(f"Connecting to ZEsarUX at {HOST}:{PORT}...")
    with socket.create_connection((HOST, PORT)) as sock:
        print("Connected.")        
        while running:
            try:
                number_lives = get_byte_from_memory(sock, NUMBER_LIVES_ADDR)
                if (number_lives != None):
                    print(f"number_lives={number_lives}")
                time.sleep(DELAY_BETWEEN_QUERIES_IN_SEC)
            except Exception as e:
                print(f"Error: {e}")
                break
        print("Disconnected.")

if __name__ == "__main__":
    main()
    