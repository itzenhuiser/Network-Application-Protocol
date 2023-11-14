import socket
import threading

# Server configuration
HOST = '172.17.9.51'
PORT = 65432

def format_message(message_type, username, message_body):
    message_header = f"{message_type}:{username}:{len(message_body)}"
    return f"{message_header}|{message_body}"


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

def write_messages(sock, username):
    while True:
        message = input("")
        # When sending a message
        formatted_message = format_message("MSG", username, message)
        sock.send(formatted_message.encode('utf-8'))


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    handshake_response = client_socket.recv(1024).decode('utf-8')
    print(f"Handshake message from server: {handshake_response}")

    screen_name = input("Enter your screen name: ")
    name_message = format_message("NAME", screen_name, "")
    client_socket.send(name_message.encode('utf-8'))

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    write_thread = threading.Thread(target=write_messages, args=(client_socket, screen_name))
    write_thread.start()

# Start the client
start_client()
