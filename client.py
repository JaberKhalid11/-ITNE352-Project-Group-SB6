import socket 
import tkinter as tk
from tkinter import messagebox,scrolledtext
from PIL import Image, ImageTk 


# information for the server:
host ="127.0.0.1"
port=4096

#creat the socket and connecting to the server 
client_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host,port))

#sending the user name :
name=input("please enter your name : ")
client_socket.send(name.encode())

# creat the GUI widow 
window=tk.Tk()
window.title(" the filght info")
window.geometry("600x500")
window.resizable(False,False)

# adding the logo 
logo_image=Image.open("uob_logo.png")
logo_image=logo_image.resize((100,100))
logo_photo=ImageTk.PhotoImage(logo_image)
logo_label=tk.Label(window, image=logo_photo)
logo_label,image=logo_photo # to make sure the photo will not delete 
logo_label.pack(pady=5)


## sending the user name for the server.
def send_name():
  name=name_entery.get().strip()
  if not name:
    messagebox.showwarning("the name is not correct!","please enter the right name")
    return 
  client_socket.send(name.encode())
  name_frame.pack_forget()
  main_menu.pack(pady=20)

# ----the menu that will show----

# the arriver
def send_arrived():
  client_socket.send("ARRIVED".encode())
  display_response()

# the delay
def send_delayed():
  client_socket.send("DELAYED".encode())
  display_response()

#the details 
def send_details():
  code=iata_entry.get().strip().upper()
  if not code :
    messagebox.showwarning("the IATA code is wrong! or missing!","please enter the right IATA")
    return
  client_socket.send(f"Details:{code}".encode())
  display_response()

# the messge respponse form the server
def display_response():
  respponse=client_socket.recv(4096).decode()
  output_text.insert(tk.END,f"{respponse}\n")
  output_text.see(tk.END)

# QUIT the app
def quit_app():
  client_socket.send("QUIT".encode())
  client_socket.close()
  window.destroy()

## the name the user will type it.
name_frame=tk.frame(window)
tk.Label(name_frame, text="please enter the name:",font=("Arial",14)).pack(pady=10)
name_entery=tk.Entry(name_frame,font=("Arial",14),width=40)
name_entery.pack()
tk.Button(name_frame,text="connect",font=("Arial",14),command=send_name).pack(pady=10)
name_frame.pack(pady=20)

#the menu main fram the will contain function
main_menu =tk.fram(window)

# the buttons for the requset that the user will press 
tk.Label(main_menu ,text="the main menu",font=("Arial",14,"bold")).pack(pady=5)
tk.Button(main_menu,text="Show the Arrived filghts",font=("Arial",12) ,width=30,command=send_arrived).pack(pady=5)
tk.Button(main_menu,text="Show the Delayed filghts",font=("Arial",12) ,width=30,command=send_delayed).pack(pady=5)


# enter the IATA and the details of it.
iata_frame=tk.Frame(main_menu)
tk.Label(iata_frame ,text="IATA code",font=("Arial",14)).pack(side=tk.LEFT)
iata_entry=tk.Entry(iata_frame,font=("Arial",14),width=15)
iata_entry.pack(side=tk.LEFT,padx=5)
tk.Button(iata_frame,text="Show the Flight Details",font=("Arial",14),command=send_details).pack(side=tk.LEFT)
iata_frame.pack(pady=10)

#the output
output_text= scrolledtext.ScrolledText(main_menu, width=80 , height=20 ,font=("Arial",12))
output_text.pack(pady=10)

# start the app
window.mainloop()











  
  
  
  
  
  
