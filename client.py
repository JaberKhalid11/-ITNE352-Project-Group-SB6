import socket 

# information for the server:
host ="127.0.0.1"
port=4096

#creat the socket and connecting to the server 
client_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host,port))

#sending the user name :
name=input("please enter your name : ")
client_socket.send(name.encode())

## the main loop.

while True:
  print("\n-----main menu----")
  print("1. Show Arrived flghts")
  print("2. Show Delayed Flights")
  print("3. Show Specific Flight Details")
  print("4.Quit")

choice = input("Please Enter your choice form (1 to 4) :").strip()

if choice =="1":
  client_socket.send("Arrived".encode())
elif choice =="2":
  client_socket.send("Delayed".encode())
elif choice =="3":
  code=input("please Enter the flight IATA code").strip().upper()
  client_socket.send(f"DETAILS:{code}".encode())
elif choice =="4":
  client_socket.send("Quit".encode())
  break
else:
  print("Invalid choice. please tyy again.")
  continue
# the server have resivce and respnce.

responce =client_socket.recv(10000).decode()
print(f"------ the server respnce-----")
print(responce)

# closing the connection. 
client_socket.close()
pritn("disconet from the server")
  
