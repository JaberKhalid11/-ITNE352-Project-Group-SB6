# -ITNE352-Project-Group-SB6
## Project Title
Multithreaded Flight Arrival Client/Server System

## Project Description
This project is a Python program that shows live flight information using a simple client and server system. The server connects to an online flight API and collects flight data for a selected airport. The client has a user-friendly window where users can click buttons to see arrived flights, delayed flights, or search for flight details using the IATA code. The system supports many users at the same time using threads. It helps students learn how to build real networking apps using sockets, threads, and graphical interfaces in Python.

## Semester
Semester(2) 2024-2025

## Group
- Group: SB6
- Course Code: ITNE 352
- Section: [2]
- Student Names and IDs:
  - [Jaber Khalid] - [202207991]
  - [Ameer Sabah] - [202201411]

---

## Table of Contents
- [Project Title](#Project Title)
- [Project Description](#Project Description)
-  [Semester](#Semester)
-  [Group](#Group)
- [Requirements](#requirements)
- [How to Run](#how-to-run)
- [Scripts](#scripts)
- [Additional Concept](#additional-concept)
- [Acknowledgments](#acknowledgments)
- [Conclusion](#conclusion)
- [Resources](#resources)

---

## Requirements

To run this project, you need:
- Python 3
- `requests` library (install using `pip install requests`)
- Internet connection to fetch live flight data

---

## How to Run

1. Open two terminals.
2. In the **first terminal**, run the server:
python server.py
- It will ask for the ICAO airport code (for example, type `OBBI` for Bahrain).
- After fetching the data, the server will wait for client connections.
3. In the **second terminal**, run the client:
python client.py
4. The client window will open:
- Enter your name and click **Connect**
- Use the buttons to:
- **Show Arrived Flights** - shows flights that have landed
- **Show Delayed Flights** - shows flights with delays
- **Get Details** - enter a flight IATA code and click to see full details
- Click **Quit** to close the client app and disconnect from the server

---

## Scripts

### server.py
- Starts the server and asks for airport ICAO code
- Connects to aviationstack API and fetches 100 flight records
- Saves data in a JSON file named `SB6.json`
- Accepts many clients using threads
- Handles 3 types of requests from clients:
- `ARRIVED` - Lists landed flights
- `DELAYED` - Shows flights with delay info
- `Details:<IATA>` - Shows details of one flight
  
### client.py

- Connects to the server using TCP socket
- Uses a GUI (Tkinter) to make it user-friendly
- Sends user's name to the server
- Has buttons to send different types of flight requests
- Displays the response clearly in a scrollable text box
- Has a Quit button to close the app

---

## Additional Concept: GUI

We used a simple GUI (Graphical User Interface) in the client program using Tkinter.
It allows the user to interact with the system easily.
The user does not need to write any commands - they can just click buttons and enter flight codes.
This makes the system easier to use and understand.

---

## Acknowledgments

Thanks to:
- Dr. Mohammed Almeer for the project task and support
- aviationstack.com for providing free API flight data
- Python documentation and community tutorials that helped us
  
---

## Conclusion

This project helped us understand how to build a network program using Python.
We learned about sockets, threads, APIs, and GUI design.
Now we know how to create a server that can talk to many clients at the same time and show real-time flight
info.

---

## Resources

- https://aviationstack.com/documentation
- https://realpython.com/python-sockets/
- https://docs.python.org/3/library/tk.html

