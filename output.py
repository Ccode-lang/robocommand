# Simple socket server for robot.py output
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 5002))
s.listen(1)
connected = False

while True:
    if not connected:
        conn, addr = s.accept()
        connected = True
    data = conn.recv(1024)
    
    if not data:
        connected = False
        conn.close()

    if connected:
        print(data.decode())