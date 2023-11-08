import socket
import threading

# Server configuration
HOST = '127.0.0.1'
PORT = 65432

def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode('utf-8')
            if message:
                print(message)
        except:
            print("An error occurred.")
            sock.close()
            break

def write_messages(sock):
    while True:
        message = input("")
        sock.send(message.encode('utf-8'))

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    write_thread = threading.Thread(target=write_messages, args=(client_socket,))
    write_thread.start()

# Start the client
start_client()
