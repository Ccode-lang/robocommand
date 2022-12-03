import socket
import sys
from time import sleep
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(0.2)
args = sys.argv
# Bind the socket to the port
server_address = (args[1], 5001)
s.connect(server_address)

while True:
    # Send data
    message = input()
    s.send(message.encode())

    if message.startswith("upload "):
        filename = message[7:]
        upload = True
        try:
            file = open(filename, "r")
        except:
            upload = False
            
        if upload:
            while chunk := file.read(514):
                sleep(.1)
                s.send(chunk.encode())

                file.close()

        s.send("EOF".encode())

    try:
        data = s.recv(1024)
    except:
        data = b""
    
    if data.decode() == "conclose":
        sys.exit()

    print(data.decode())