import socket

def start_client():
    host = '127.0.0.1'
    port = 5555

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect((host, port))
        print("Connected to server. Type 'exit' to quit")
        
        while True:
            message = input("Enter message: ")
            if message.lower() == 'exit':
                break
            
            client_socket.send(message.encode())
            response = client_socket.recv(1024).decode()
            print(f"Server response: {response}")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
        print("Connection closed")


if __name__ == "__main__":
    start_client()