# import needed libraries
import socket
import sys
from time import sleep


# Start a socket and connect to server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(0.2)
args = sys.argv
server_address = (args[1], 5001)
s.connect(server_address)

while True:
    # Send data
    message = input()
    s.send(message.encode())


    # Handle upload command
    if message.startswith("upload "):
        filename = message[7:]

        # Handle missing file
        upload = True
        try:
            file = open(filename, "r")
        except:
            upload = False
        # Send file in chunks
        if upload:
            while chunk := file.read(514):
                sleep(.1)
                s.send(chunk.encode())

                file.close()

        s.send("EOF".encode())

    # Data returned by server
    try:
        data = s.recv(1024)
    except:
        data = b""
    
    # Conection closed
    if data.decode() == "conclose":
        sys.exit()

    # Output the returned data
    print(data.decode())