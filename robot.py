# Import needed libraries
import socket
from time import sleep

# Make socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(0.2)


# Define your global variables here


counter = 0

server_address = ""




def mainloop():
    # The main loop counts
    global counter
    sleep(.07)
    s.send(str(counter).encode())
    counter += 1

def before(addr):
    # Initialize connection to output.py
    print(addr)
    global server_address
    server_address = (addr[0], 5002)
    global counter
    counter = 0
    s.connect(server_address)
    s.send("hello".encode())

def after():
    # Send output "done" to output.py
    s.send("done".encode())

# A function used by server.py to run all the other loops
def loops(arg):
    return ["loop1"]

# A test loop
def loop1():
    s.send("test".encode())