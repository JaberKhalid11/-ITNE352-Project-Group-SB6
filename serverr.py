import socket
import threading
import json
import requests  
import os 
from asyncio import start_server



###creat the TCP server
host="127.0.0.1"
port=4096
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(5)
print("The server has been started.")


# featch data 
api_key="375026d7df2905c47ad49fb346e4e0a6"
url="http://api.aviationstack.com/v1/flights"

icao_code = input("Enter the ICAO code of the airport: ")
if not os.path.exists("SB6.json"):
    params = {
        'access_key': api_key,
        'arr_icao': icao_code.strip().upper(),
        'limit': 100
    }
    print("[INFO] SB6.json not found. Fetching data from API")
    response = requests.get(url, params=params)
    if response.status_code == 200:
        with open("SB6.json", "w") as file:
            json.dump(response.json(), file, indent=4)
            print("[INFO] SB6.json created successfully.")
    else:
        print("ERROR: Failed to fetch data from API.")
        exit()

#load the data 
file=open("SB6.json","r")
data=json.load(file)
flights=data.get("data",[])

def handle_client(client_socket, client_address):
    try:
        client_name = client_socket.recv(1024).decode().strip()
        print(f"Accepted connection from the client {client_name} from {client_address}")
        while True:
            request=client_socket.recv(1024).decode().strip()
            if request=="QUIT":
                print("Client disconnected")
                break

            print(f"Client {client_name} ({client_address}) requested: {request}")
            response = ""
            # the arrived flights
            if request.upper()=="ARRIVED":
                for flight in flights :
                    if flight.get("flight_status") == "landed":
                        response += f"Flight: {flight['flight']['iata']}\n"
                        response += f"From: {flight['departure']['airport']}\n"
                        response += f"Arrival: {flight['arrival']['airport']}\n"
                        response += f"Terminal: {flight['arrival'].get('terminal')}\n"
                        response += f"Gate: {flight['arrival'].get('gate')}\n"

 
                        
                if not response:
                    response ="not arrived flight founded. "
                    #the delayed flights
            elif request.upper()== "DELAYED":
                for flight in flights :
                    delay =flight["arraival"].get["delay"]
                    if delay >0:
                     response += f"Flight: {flight['flight']['iata']}\n"
                     response += f"from: {flight['departure']['airport']} \n"
                     response += f"Arrival: {flight['arrival']['airport']}\n"
                     response += f"Terminal:  {flight['arrival']['terminal']} \n"
                     response += f"gate: {flight['arrival']['gate']}\n"
                    
                if not response:
                    response = "No delayed flights are found."
                #the specific flight details
            elif request.upper().startswith("DETAILS:"):
                flight_number = request.split(":")[1].strip().upper()
                found = False

                for flight in flights:
                    if flight['flight']['iata'] == flight_number:
                        response += f"Flight: {flight['flight']['iata']}\n"
                        response += f"From: {flight['departure']['airport']}\n"
                        response += f"Arrival: {flight['arrival']['airport']}\n"
                        response += f"Terminal: {flight['arrival'].get('terminal', 'N/A')}\n"
                        response += f"Gate: {flight['arrival'].get('gate', 'N/A')}\n\n"
                        found = True
                        break
                    
                if not found:
                    response = f"No flight found with IATA code {flight_number}."
            else:
                response = "Invalid request."

            client_socket.send(response.encode())


            
    except Exception as e:
        print("Error:", e)
    finally:
        client_socket.close()

# starting the server 
def start_server():
    print("The server is on now and waiting for connections...")
    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

start_server()

            


                 
                    


                    

           


                    
                        
                    




                
                
            
        
    
        








    
