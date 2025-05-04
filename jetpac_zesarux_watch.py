import socket
import time
import signal
import sys

# Settings
HOST = 'localhost'
PORT = 10000
DELAY_BETWEEN_QUERIES_IN_SEC=0.2

# All these addresses are taken from  Jetpac's disassembly:
# https://phillipeaton.github.io/jetpac-disassembly/
JETMAN_LIVES_ADDR = 0x5DF1
JETMAN_SLOT_ADDR  = 0x5D00
GAME_LEVEL_ADDR   = 0x5DF0
ALIEN_SLOTS_ADDR  = [
    0x5D50,
    0x5D58,
    0x5D60,
    0x5D68,
    0x5D70,
    0x5D78,
]

DIRECTION_SLOT_OFFSET        = 0
X_POS_SLOT_OFFSET            = 1 # (0x00=full-right 0xFF=full-left)
Y_POS_SLOT_OFFSET            = 2 # (0x29=full-up    0xB7=full-down)
COLOR_ATTR_SLOT_OFFSET       = 3
MOVING_DIRECTION_SLOT_OFFSET = 4
X_SPEED_SLOT_OFFSET          = 5 
Y_SPEED_SLOT_OFFSET          = 6 
SPRITE_HEIGHT_SLOT_OFFSET    = 7

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

class GameState:
    def __init__(self):
        self.jetman = {"x": None, "y": None, "x_speed": None, "y_speed": None}
        self.aliens = [{"x": None, "y": None, "x_speed": None, "y_speed": None} for _ in range(len(ALIEN_SLOTS_ADDR))]
        self.lives = None
        self.level = None
        
def read_game_state(sock):
    state = GameState()
    
    # Jetman data
    state.lives = get_byte_from_memory(sock, JETMAN_LIVES_ADDR)
    state.level = get_byte_from_memory(sock, GAME_LEVEL_ADDR)    
    state.jetman["x"] = get_byte_from_memory(sock, JETMAN_SLOT_ADDR + X_POS_SLOT_OFFSET)
    state.jetman["y"] = get_byte_from_memory(sock, JETMAN_SLOT_ADDR + Y_POS_SLOT_OFFSET)
    state.jetman["x_speed"] = get_byte_from_memory(sock, JETMAN_SLOT_ADDR + X_SPEED_SLOT_OFFSET)
    state.jetman["y_speed"] = get_byte_from_memory(sock, JETMAN_SLOT_ADDR + Y_SPEED_SLOT_OFFSET)

    # Alien positions
    for i, base_addr in enumerate(ALIEN_SLOTS_ADDR):
        state.aliens[i]["x"] = get_byte_from_memory(sock, base_addr + X_POS_SLOT_OFFSET)
        state.aliens[i]["y"] = get_byte_from_memory(sock, base_addr + Y_POS_SLOT_OFFSET)
        state.aliens[i]["x_speed"] = get_byte_from_memory(sock, base_addr + X_SPEED_SLOT_OFFSET)
        state.aliens[i]["y_speed"] = get_byte_from_memory(sock, base_addr + Y_SPEED_SLOT_OFFSET)

    return state

def print_game_state(state):
    out = []
    
    # Jetman
    if state.jetman["x"] is not None and state.jetman["y"] is not None and state.jetman["x_speed"] is not None and state.jetman["y_speed"] is not None:
        out.append(f"Jetman:({state.jetman['x']:2},{state.jetman['y']:2},{state.jetman['x_speed']:2},{state.jetman['y_speed']:2})")
    else:
        out.append("Jetman:(--,--,--,--)")
    
    # Lives
    if state.lives is not None:
        out.append(f"Lives:{state.lives}")
    else:
        out.append("Lives:??")

    # Level
    if state.level is not None:
        out.append(f"Lvl:{state.level}")
    else:
        out.append("Lvl:??")

    # Aliens
    alien_strs = []
    for i, alien in enumerate(state.aliens):
        x = alien["x"]
        y = alien["y"]
        x_speed = alien["x_speed"]
        y_speed = alien["y_speed"]
        if x is not None and y is not None and x_speed is not None and y_speed is not None:
            alien_strs.append(f"{i+1}:({x:2},{y:2},{x_speed:2},{y_speed:2})")
        else:
            alien_strs.append(f"{i+1}:(--,--,--,--)")
    
    out.append("Aliens: " + " ".join(alien_strs))

    # Final output
    print(" | ".join(out))    


def main():
    print(f"Connecting to ZEsarUX at {HOST}:{PORT}...")
    with socket.create_connection((HOST, PORT)) as sock:
        print("Connected.")        
        while running:
            try:
                # Here is a sample line to get the contents of a specific location  
                #jetman_lives = get_byte_from_memory(sock, JETMAN_LIVES_ADDR)
                
                state = read_game_state(sock)
                print_game_state(state)
                                  
                time.sleep(DELAY_BETWEEN_QUERIES_IN_SEC)
            except Exception as e:
                print(f"Error: {e}")
                break
        print("Disconnected.")

if __name__ == "__main__":
    main()
    