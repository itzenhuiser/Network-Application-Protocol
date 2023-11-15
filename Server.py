import socket
import threading


HOST = '192.168.4.25'  
PORT = 65432        

clients = []

def format_message(message_type, username, message_body):
    message_header = f"{message_type}:{username}:{len(message_body)}"
    return f"{message_header}|{message_body}"


def client_thread(conn, addr):
    handshake_message = format_message("HSK", "Server", "Hello, client")
    conn.send(handshake_message.encode('utf-8'))

    print(f"Connected by {addr}")

    name_msg = conn.recv(1024).decode('utf-8')
    msg_header ,_ = name_msg.split("|")
    _, screen_name ,_ = msg_header.split(":")
    broadcast(f"{screen_name} has joined the chat", conn, screen_name)


    while True:
        try:
            message = conn.recv(1024).decode('utf-8')
            _,msg_body = message.split("|")
            if message:
                print(f"{screen_name}: {msg_body}")
                broadcast(msg_body, conn, screen_name)
            else:
                remove(conn)
                break
        except:
            continue

def broadcast(message, connection, name):
    for client in clients:
        if client != connection:
            try:
                broadcast_message = format_message("MSG",name, message)
                client.send(broadcast_message.encode('utf-8'))
            except:
                client.close()
                remove(client)
                broadcast_message = format_message("MSG",name, name + " has disconnected")

def remove(connection):
    if connection in clients:
        clients.remove(connection)

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Server is listening on {HOST}:{PORT}...")

    while True:
        conn, addr = server_socket.accept()
        clients.append(conn)
        t = threading.Thread(target=client_thread, args=(conn, addr))
        t.start()

start_server()