import socket

def start_client():
    host = '127.0.0.1'
    port = 5555

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect((host, port))
        message = input("Enter message to send: ")
        client_socket.send(message.encode())
        
        response = client_socket.recv(1024).decode()
        print(f"Server response: {response}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()