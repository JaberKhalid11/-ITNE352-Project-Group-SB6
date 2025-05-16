# client.py
import socket
import tkinter as tk
from tkinter import messagebox, scrolledtext


# Connect to server
host = "127.0.0.1"
port = 5050
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))


# GUI setup
window = tk.Tk()
window.title("Flight Info")
window.geometry("600x500")
window.resizable(False, False)


# Send user name
def send_name():
    name = name_entry.get().strip()
    if not name:
        messagebox.showwarning("Name missing", "Enter your name")
        return
    client_socket.send(name.encode())
    name_frame.pack_forget()
    menu_frame.pack()


# Request: Arrived flights
def request_arrived():
    client_socket.send("ARRIVED".encode())
    show_response()


# Request: Delayed flights
def request_delayed():
    client_socket.send("DELAYED".encode())
    show_response()


# Request: Flight details by IATA code
def request_details():
    code = iata_entry.get().strip().upper()
    if not code:
        messagebox.showwarning("Missing IATA", "Enter flight IATA code")
        return
    client_socket.send(f"Details:{code}".encode())
    show_response()


# Show server reply
def show_response():
    reply = client_socket.recv(4096).decode()
    output.insert(tk.END, reply + "\n\n")
    output.see(tk.END)


# Quit app
def quit_app():
    client_socket.send("QUIT".encode())
    client_socket.close()
    window.destroy()


# Entry for name
name_frame = tk.Frame(window)
tk.Label(name_frame, text="Enter your name:", font=("Arial", 14)).pack(pady=10)
name_entry = tk.Entry(name_frame, font=("Arial", 14), width=30)
name_entry.pack()
tk.Button(name_frame, text="Connect", font=("Arial", 14), command=send_name).pack(pady=10)
name_frame.pack(pady=20)


# Main menu
menu_frame = tk.Frame(window)
tk.Label(menu_frame, text="Main Menu", font=("Arial", 14, "bold")).pack(pady=5)
tk.Button(menu_frame, text="Show Arrived Flights", width=30, command=request_arrived).pack(pady=5)
tk.Button(menu_frame, text="Show Delayed Flights", width=30, command=request_delayed).pack(pady=5)


# IATA code input
iata_frame = tk.Frame(menu_frame)
tk.Label(iata_frame, text="IATA Code:", font=("Arial", 12)).pack(side=tk.LEFT)
iata_entry = tk.Entry(iata_frame, font=("Arial", 12), width=15)
iata_entry.pack(side=tk.LEFT, padx=5)
tk.Button(iata_frame, text="Get Details", command=request_details).pack(side=tk.LEFT)
iata_frame.pack(pady=10)


# Output area
output = scrolledtext.ScrolledText(menu_frame, width=70, height=15, font=("Arial", 11))
output.pack(pady=10)
tk.Button(menu_frame, text="Quit", command=quit_app).pack(pady=10)


# Start app
window.mainloop()
