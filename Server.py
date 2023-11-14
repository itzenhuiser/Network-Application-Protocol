import socket
import threading

# Server configuration
HOST = '172.17.9.51'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

# Client management
clients = []

def format_message(message_type, message_body):
    message_header = f"{message_type}:{len(message_body)}"
    return f"{message_header}|{message_body}"


def client_thread(conn, addr):

    handshake_message = format_message("HSK", "Hello, client")
    conn.send(handshake_message.encode('utf-8'))

    print(f"Connected by {addr}")
    while True:
        try:
            message = conn.recv(1024).decode('utf-8')
            if message:
                print(f"{addr} says: {message}")
                broadcast(message, conn)
            else:
                remove(conn)
                break
        except:
            continue

def broadcast(message, connection):
    for client in clients:
        if client != connection:
            try:
                # When broadcasting a message
                broadcast_message = format_message("MSG", message)
                client.send(broadcast_message.encode('utf-8'))
            except:
                client.close()
                remove(client)

def remove(connection):
    if connection in clients:
        clients.remove(connection)

def start_server():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Server is listening on {HOST}:{PORT}...")

    while True:
        conn, addr = server_socket.accept()
        clients.append(conn)
        t = threading.Thread(target=client_thread, args=(conn, addr))
        t.start()

# Start the server
start_server()
