import socket
import json

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5050

def print_flights(flights):
    if not flights:
        print("No results found.")
    elif isinstance(flights, dict) and 'error' in flights:
        print("Error:", flights['error'])
    else:
        for f in flights:
            print(json.dumps(f, indent=2))
            
            
def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_HOST, SERVER_PORT))

    welcome = client.recv(1024).decode()
    print(welcome, end='')
    username = input()
    client.sendall(username.encode())

    while True:
        print("\nChoose an option:")
        print("1 - View arrived flights")
        print("2 - View delayed flights")
        print("3 - View details of a specific flight")
        print("quit - Exit")

        option = input("Enter your choice: ").strip()
        if option == '3':
            code = input("Enter flight IATA code: ").strip().upper()
            message = f"3:{code}"
        else:
            message = option

        client.sendall(message.encode())
        if option.lower() == 'quit':
            break

        response = client.recv(8192).decode()
        try:
            result = json.loads(response)
            print_flights(result)
        except json.JSONDecodeError:
            print("[ERROR] Invalid response from server")

    client.close()
    print("Disconnected from server.")

if __name__ == "__main__":
      main()