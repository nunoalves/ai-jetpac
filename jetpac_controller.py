
import time
import socket
from jetpac_game_state import (
    HOST, PORT,
    send_command, send_key,
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

    # dumbly fire (at the direction the jetman is facing) if an alien is close... 
    # ...wgich most likely will fire wrong direction
    if (is_xy_position_safe(state.jetman["x"], state.jetman["y"], alien_positions)):
        # jetman is safe
        send_key(sock,"fire",False)
    else:
        # jetman is in danger
        send_key(sock,"fire",True)

    # dumbly move away from the closest alien:
    # ... dumb jetman has no idea of the platforms
    # ... dumb jetman also has no idea that moving to one edge of the screen will telport to the opposite.
    jet_x, jet_y = state.jetman["x"], state.jetman["y"]
    nearest = min(
        (pos for pos in alien_positions if pos[0] is not None),
        key=lambda pos: abs(pos[0] - jet_x) + abs(pos[1] - jet_y)
    )
    ax, ay = nearest

    dx = jet_x - ax
    dy = jet_y - ay

    if (dx < 0): 
        send_key(sock,"left",True)
        send_key(sock,"right",False)
    else:
        send_key(sock,"left",False)
        send_key(sock,"right",True)

    if (dy > 0):
        send_key(sock,"up",True)
    else:
        send_key(sock,"up",False)

