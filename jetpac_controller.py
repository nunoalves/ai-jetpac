
import time
import socket
from jetpac_game_state import (
    HOST, PORT,
    read_game_state, send_command,
    JETMAN_SLOT_ADDR, X_POS_SLOT_OFFSET, Y_POS_SLOT_OFFSET
)

# Safe distance (from aliens) threshold
SAFE_DISTANCE = 40

def write_jetman_position(sock, x, y):
    send_command(sock, f"write-memory {JETMAN_SLOT_ADDR + X_POS_SLOT_OFFSET} {x}")
    send_command(sock, f"write-memory {JETMAN_SLOT_ADDR + Y_POS_SLOT_OFFSET} {y}")

def is_xy_position_safe(jetman_x, jetman_y, alien_positions):
    for alien_x, alien_y in alien_positions:
        if alien_x is None or alien_y is None or jetman_x is None or jetman_y is None:
            continue
        if abs(alien_x - jetman_x) < SAFE_DISTANCE and abs(alien_y - jetman_y) < SAFE_DISTANCE:
            return False
    return True
    
def is_jetman_safe(sock, state):
    alien_positions = [(a["x"], a["y"]) for a in state.aliens]

    if (is_xy_position_safe(state.jetman["x"], state.jetman["y"], alien_positions)):
        print("SAFE")
    else:
        print("DANGER")
