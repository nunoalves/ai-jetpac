import socket
import time
import signal
from jetpac_game_state import HOST, PORT, read_game_state, print_game_state
from jetpac_controller import is_jetman_safe

# Modes
ENABLE_WATCH = False
ENABLE_AI_CONTROL = True
CONTROL_LOOP_PERIOD_IN_SECONDS = 0.2

running = True

# Handle Ctrl+C to exit cleanly
def handle_sigint(sig, frame):
    global running
    print("\nTerminating...")
    running = False

signal.signal(signal.SIGINT, handle_sigint)

def main():
    print(f"Connecting to ZEsarUX at {HOST}:{PORT}...")
    with socket.create_connection((HOST, PORT)) as sock:
        print("Connected.")

        while running:
            state = read_game_state(sock)

            if ENABLE_WATCH:
                print_game_state(state)

            if ENABLE_AI_CONTROL:
                is_jetman_safe(sock, state)

            time.sleep(CONTROL_LOOP_PERIOD_IN_SECONDS)

if __name__ == "__main__":
    main()
