import socket
import threading
import json
import requests  # type: ignore 
import os 



###creat the TCP server
host="127.0.0.1"
port=4096

# featch data 
api_key="375026d7df2905c47ad49fb346e4e0a6"
url="http://api.aviationstack.com/v1/flights"

if not os.path.exists("SB6.jason"):
    params = {
            'access_key': api_key,
            'arr_icao': icao_code.strip().upper(),
            'limit': 100
        }
print("[INFO] SB5.json not found. Fetching data from API")
response = requests.get(api_key, params=params)
if response.status_code == 200:
    with open("SBS.json","w") as file :
        json.dump(response.json(),file,indent=4)
        print("[INFO] SB6.json created successfully.")
else:
    print("ERROR: Failed to fetch data from API.")
    exit()

#load the data 
with open ("SB6","r")
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
            if request.upper()=="ARRIVED":
                for flight in flights :
                    if flight.get("flight_status") == "landed":
                        response += "Flight": {flight['flight']['iata']}+"\n"
                        response += "From": {flight['departure']['airport']}+"\n"
                        response += "Arrival": {flight['arrival']['airport']}\n"
                        response += "Terminal": {flight['arrival'].get('terminal')}+"\n"
                        response += "Gate": {flight['arrival'].get('gate')}+"\n"

 
                        
                if not response:
                    response ="not arrived flight founded. "
                    
            elif request.upper()== "DELAYED":
                for flight in flights :
                    delay =flight["arraival"].get["delay"]
                    if delay >0:
                    response += "Flight": (flight['flight']['iata']) + "\n"
                    response += "from": (flight["leaving"]["airport"]) + "\n"
                    response += "Arrival": (flight["arrival"]["airport"]) + "\n"
                    response += "Terminal: " (flight["arrival"]["terminal"]) + "\n"
                    response += "gate": (flight["arrival"]["gate"]) + \"n"
                    
                    

                if not response :
                    response = "No delayed flights are found."
                else:
                    response = "There are delayed flights found."

elif request.uppre().startswith("DETAILS:"):



                 
                    


                    

           


                    
                        
                    




                
                
            
        
    
        








    
