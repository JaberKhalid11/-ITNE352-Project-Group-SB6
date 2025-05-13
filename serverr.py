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






    
