import socket
from time import sleep
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(0.2)


#define your variables here


counter = 0

server_address = ""




def mainloop():
    global counter
    sleep(.07)
    s.send(str(counter).encode())
    counter += 1

def before(addr):
    print(addr)
    global server_address
    server_address = (addr[0], 5002)
    global counter
    counter = 0
    s.connect(server_address)
    s.send("hello".encode())

def loops(arg):
    return False