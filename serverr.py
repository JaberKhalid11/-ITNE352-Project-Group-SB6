# server.py
import socket
import threading
import json
import requests
import os


# Setup server
host = "127.0.0.1"
port = 5050
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(5)
print("[SERVER STARTED] Waiting for clients...")


# Get airport ICAO code and fetch data
icao_code = input("Enter ICAO code: ").strip().upper()
file_name = "SB6.json"  

if not os.path.exists(file_name):
    print("[INFO] Getting data from API...")
    url = "http://api.aviationstack.com/v1/flights"
    params = {'access_key': '375026d7df2905c47ad49fb346e4e0a6', 'arr_icao': icao_code, 'limit': 100}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        with open(file_name, "w") as f:
            json.dump(response.json(), f, indent=4)
        print("[INFO] Data saved.")
    else:
        print("[ERROR] Failed to get data.")
        exit()


# Load data
with open(file_name, "r") as f:
    flights = json.load(f).get("data", [])


# Handle each client
def handle_client(client_socket, addr):
    try:
        name = client_socket.recv(1024).decode().strip()
        print(f"[CONNECTED] {name} from {addr}")

        while True:
            msg = client_socket.recv(1024).decode().strip()
            if msg == "QUIT":
                print(f"[DISCONNECTED] {name}")
                break

            print(f"[REQUEST] {name}: {msg}")
            reply = ""

            if msg == "ARRIVED":
                for flight in flights:
                    if flight.get("flight_status") == "landed":
                        reply += f"Flight: {flight['flight']['iata']}\n"
                        reply += f"From: {flight['departure']['airport']}\n"
                        reply += f"To: {flight['arrival']['airport']}\n"
                        reply += f"Terminal: {flight['arrival'].get('terminal', 'N/A')}\n"
                        reply += f"Gate: {flight['arrival'].get('gate', 'N/A')}\n\n"
                if not reply:
                    reply = "No arrived flights found."

            elif msg == "DELAYED":
                for flight in flights:
                    delay = flight.get("arrival", {}).get("delay", 0)
                    if delay and delay > 0:
                        reply += f"Flight: {flight['flight']['iata']}\n"
                        reply += f"From: {flight['departure']['airport']}\n"
                        reply += f"To: {flight['arrival']['airport']}\n"
                        reply += f"Departure Time: {flight['departure'].get('scheduled', 'N/A')}\n"
                        reply += f"Arrival Time: {flight['arrival'].get('scheduled', 'N/A')}\n"
                        reply += f"Delay: {delay} minutes\n"
                        reply += f"Terminal: {flight['arrival'].get('terminal', 'N/A')}\n"
                        reply += f"Gate: {flight['arrival'].get('gate', 'N/A')}\n\n"
                if not reply:
                    reply = "No delayed flights found."

            elif msg.startswith("Details:"):
                code = msg.split(":")[1].strip().upper()
                for flight in flights:
                    if flight['flight']['iata'] == code:
                        reply += f"Flight: {code}\n"
                        reply += f"From: {flight['departure']['airport']}\n"
                        reply += f"Gate: {flight['departure'].get('gate', 'N/A')}\n"
                        reply += f"Terminal: {flight['departure'].get('terminal', 'N/A')}\n"
                        reply += f"To: {flight['arrival']['airport']}\n"
                        reply += f"Gate: {flight['arrival'].get('gate', 'N/A')}\n"
                        reply += f"Terminal: {flight['arrival'].get('terminal', 'N/A')}\n"
                        reply += f"Status: {flight.get('flight_status', 'N/A')}\n"
                        reply += f"Departure Time: {flight['departure'].get('scheduled', 'N/A')}\n"
                        reply += f"Arrival Time: {flight['arrival'].get('scheduled', 'N/A')}\n"
                        break
                if not reply:
                    reply = f"No flight found with IATA code {code}."

            else:
                reply = "Invalid request."

            client_socket.send(reply.encode())

    except Exception as e:
        print("[ERROR]", e)
    finally:
        client_socket.close()
        

# Start listening
def start_server():
    while True:
        client, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client, addr))
        thread.start()

start_server()
