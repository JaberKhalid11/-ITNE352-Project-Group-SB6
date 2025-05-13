import socket
import threading
# This is a simple TCP server that listens for incoming connections and handles them in a multithreaded manner.                                         

#multithreaded server

class ClientHandler(threading.Thread):
    def __init__(self, client_socket, address):
        super().__init__()
        self.client_socket = client_socket
        self.address = address


def run(self):
        print(f"New connection from {self.address}")
        try:
            while True:
                data = self.client_socket.recv(1024).decode()
                if not data:
                    break
                print(f"Received from {self.address}: {data}")
                response = f"Server received: {data}"
                self.client_socket.send(response.encode())
        except Exception as e:
            print(f"Error with {self.address}: {e}")
        finally:
            self.client_socket.close()
            print(f"Connection with {self.address} closed")


def start_server():
    host = '127.0.0.1'
    port = 5555

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        
        try:
            data = client_socket.recv(1024).decode()
            if data:
                print(f"Received: {data}")
                response = "Message received by server!"
                client_socket.send(response.encode())
        except Exception as e:
            print(f"Error: {e}")
        finally:
            client_socket.close()
            print("Connection closed")
            
            
if __name__ == "__main__":
    start_server()