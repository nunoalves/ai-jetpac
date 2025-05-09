import time
import socket
import time
import signal
from jetpac_game_state import HOST, PORT, GameState, print_game_state, send_key
from jetpac_controller import is_jetman_safe

# Modes
ENABLE_WATCH = True
ENABLE_AI_CONTROL = False
ENABLE_GAME_OVER_EXIT = False
CONTROL_LOOP_PERIOD_IN_SECONDS = 0.2

running = True

# Handle Ctrl+C to exit cleanly
def handle_sigint(sig, frame):
    global running
    print("\nTerminating...")
    running = False

signal.signal(signal.SIGINT, handle_sigint)

def main():
    global running

    print(f"Connecting to ZEsarUX at {HOST}:{PORT}...")
    with socket.create_connection((HOST, PORT)) as sock:
        print("Connected.")

        # ensure no other keys are pressed
        for btn in ("up","fire","left","right"):
            send_key(sock,btn,False)

        # start the game
        send_key(sock,"start",True)

        time.sleep(1)

        # game has started, let the "start" key go
        send_key(sock,"start",False)

        state = GameState()

        while running:

            state.refresh(sock)

            if ENABLE_WATCH:
                print_game_state(state)

            if ENABLE_AI_CONTROL:
                is_jetman_safe(sock, state)

            if ENABLE_GAME_OVER_EXIT and state.game_over:
                print("Game Over!")
                running = False

            time.sleep(CONTROL_LOOP_PERIOD_IN_SECONDS)

        for btn in ("up","fire","left","right"):
            send_key(sock,btn,False)

if __name__ == "__main__":
    main()
