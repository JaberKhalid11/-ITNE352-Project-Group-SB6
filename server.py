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

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 5050))
    server.listen(5)
    print("[SERVER] Listening...")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()