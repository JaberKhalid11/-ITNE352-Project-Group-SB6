import socket
import threading
import json
import requests

API_KEY = "1a606ff09040ef8539b85c3e2ab198fb"
API_URL = "http://api.aviationstack.com/v1/flights"
JSON_FILE = "group_SB6.json"
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5050

def fetch_and_store_data(icao):
    params = {'access_key': API_KEY, 'arr_icao': icao, 'limit': 100}
    try:
        response = requests.get(API_URL, params=params)
        data = response.json().get('data', [])
        with open(JSON_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        return data
    except Exception as e:
        print(f"[ERROR] Failed to fetch API data: {e}")
        return []

def load_flight_data():
    try:
        with open(JSON_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def handle_client(conn, addr, client_name, flights):
    print(f"[CONNECTED] {client_name} ({addr})")
    try:
        while True:
            request = conn.recv(1024).decode()
            if not request:
                break
            print(f"[REQUEST] From {client_name}: {request}")

            if request == '1':
                result = [
                    {
                        'iata': f.get('flight', {}).get('iata'),
                        'dep_airport': f.get('departure', {}).get('airport'),
                        'arr_time': f.get('arrival', {}).get('scheduled'),
                        'terminal': f.get('arrival', {}).get('terminal'),
                        'gate': f.get('arrival', {}).get('gate')
                    }
                    for f in flights if f.get('flight_status') == 'landed']
                conn.sendall(json.dumps(result).encode())

            elif request == '2':
                result = [
                    {
                        'iata': f.get('flight', {}).get('iata'),
                        'dep_airport': f.get('departure', {}).get('airport'),
                        'dep_time': f.get('departure', {}).get('scheduled'),
                        'arr_time': f.get('arrival', {}).get('estimated'),
                        'terminal': f.get('arrival', {}).get('terminal'),
                        'gate': f.get('arrival', {}).get('gate'),
                        'delay': f.get('arrival', {}).get('delay')
                    }
                    for f in flights if f.get('arrival', {}).get('delay')]
                conn.sendall(json.dumps(result).encode())

            elif request.startswith('3:'):
                code = request[2:].strip()
                f = next((f for f in flights if f.get('flight', {}).get('iata') == code), None)
                if f:
                    result = {
                        'iata': f.get('flight', {}).get('iata'),
                        'dep_airport': f.get('departure', {}).get('airport'),
                        'dep_terminal': f.get('departure', {}).get('terminal'),
                        'dep_gate': f.get('departure', {}).get('gate'),
                        'arr_airport': f.get('arrival', {}).get('airport'),
                        'arr_terminal': f.get('arrival', {}).get('terminal'),
                        'arr_gate': f.get('arrival', {}).get('gate'),
                        'status': f.get('flight_status'),
                        'dep_time': f.get('departure', {}).get('scheduled'),
                        'arr_time': f.get('arrival', {}).get('scheduled')
                    }
                else:
                    result = {'error': 'Flight not found.'}
                conn.sendall(json.dumps(result).encode())

            elif request.lower() == 'quit':
                break
            else:
                conn.sendall(json.dumps({'error': 'Invalid request'}).encode())
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        conn.close()
        print(f"[DISCONNECTED] {client_name}")

def start_server():
    icao = input("Enter target airport ICAO code (e.g., OBBI): ").strip().upper()
    flights = fetch_and_store_data(icao)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_HOST, SERVER_PORT))
    server.listen(5)
    print(f"[SERVER] Listening on {SERVER_HOST}:{SERVER_PORT}")

    while True:
        conn, addr = server.accept()
        conn.sendall(b"Enter your name: ")
        client_name = conn.recv(1024).decode().strip()
        thread = threading.Thread(target=handle_client, args=(conn, addr, client_name, flights))
        thread.start()

if __name__ == '__main__':
    start_server()
    # server is ready to accept connections