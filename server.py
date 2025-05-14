import socket
import threading
import requests
import json

def fetch_flight_data(icao):
    response = requests.get(
        "http://api.aviationstack.com/v1/flights",
        params={"access_key": "1a606ff09040ef8539b85c3e2ab198fb", "arr_icao": icao, "limit": 100}
    )
    flights = response.json().get("data", [])
    with open("group_SB6.json", "w") as f:
        json.dump(flights, f, indent=4)
    return flights

def handle_client(conn, addr, client_name, flights):
    print(f"[CONNECTED] {client_name} ({addr})")
    try:
        while True:
            request = conn.recv(1024).decode()
            if not request:
                break

            if request == '1':
                # Arrived flights
                result = [
                    {
                        'iata': f.get('flight', {}).get('iata'),
                        'dep_airport': f.get('departure', {}).get('airport'),
                        'arr_time': f.get('arrival', {}).get('scheduled'),
                        'terminal': f.get('arrival', {}).get('terminal'),
                        'gate': f.get('arrival', {}).get('gate')
                    }
                    for f in flights if f.get('flight_status') == 'landed'
                ]
                conn.sendall(json.dumps(result).encode())

            elif request == '2':
                # Delayed flights
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
                    for f in flights if f.get('arrival', {}).get('delay')
                ]
                conn.sendall(json.dumps(result).encode())

            elif request.startswith('3:'):
                # Specific flight details
                code = request[2:].strip().upper()
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
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 5050))
    server.listen(5)
    print("[SERVER] Listening...")

    while True:
        conn, addr = server.accept()
        conn.sendall(b"Enter your name: ")
        client_name = conn.recv(1024).decode().strip()
        print(f"[NEW CONNECTION] {client_name} ({addr})")
        thread = threading.Thread(target=handle_client, args=(conn, addr, client_name, flights))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()