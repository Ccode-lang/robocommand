# Import all libraries
import socket
import os
import sys
import threading
import importlib

# Make a socketserver
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 5001))
s.listen(1)

# Gloabl variables
runpro = False
connected = False


# Function to run robot.py
def roborun(code, addr):
    loops = []
    if code.loops("more"):
        loops = code.loops("list")
    code.before(addr)
    while True:
        global runpro
        if not runpro:
            code.after()
            break
        try:
            code.mainloop()
            for loop in loops:
                getattr(code, loop)()
        except Exception as e:
            print(type(e))
            print(e)
            runpro = False



# Main loop
while 1:
    # Accept connection if not already connected to a client
    if not connected:
        conn, addr = s.accept()
        connected = True
    # Receive single packet from client
    data = conn.recv(1024)

    # If data does not exist the client has disconnected
    if not data:
        connected = False
        conn.close()
    
    # Main code
    if connected:
        # Quit the client
        if data.decode() == "quit":
            conn.send("conclose".encode())
            conn.close()
            connected = False
        # Run robot.py based file in new thread
        elif data.decode().startswith("run "):
            try:
                robocode = __import__(data.decode()[4:], globals(), locals(), [], 0)
                pro = threading.Thread(target = roborun, args =(robocode, addr, ))
                importlib.reload(robocode)
                pro.start()
                runpro = True
            except:
                conn.send("failed to start".encode())
        # Stop robot.py thread
        elif data.decode().startswith("stop"):
            runpro = False
            pro.join()
        # Quit both server and client
        elif data.decode() == "quitserver":
            conn.send("conclose".encode())
            conn.close()
            s.close()
            runpro = False
            pro.join()
            sys.exit()
        # Echo command to test connection
        elif data.decode().startswith("echo "):
            conn.send(data[5:])
        # Handle uploads from client
        elif data.decode().startswith("upload "):
            filename = data.decode()[7:]
            file = open(filename, "a")
            # Receive chunks of file and save them
            while True:
                chunk = conn.recv(1024)
                print("test")
                print(chunk.decode())
                if not chunk.decode() == "EOF":
                    file.write(chunk.decode())
                else:
                    file.close()
                    break
        # Ls comman for file management
        elif data.decode() == "ls":
            files = ""
            fileslist = os.listdir()
            for file in fileslist:
                files += file + "\n"

            #TODO: if many files are included in the list it cuts off because of the the client's buffer size.
            conn.send(files.encode())
        # Remove files for file management
        elif data.decode().startswith("rm "):
            filename = data.decode()[3:]
            try:
                os.remove(filename)
            except:
                conn.send("failed to remove file".encode())
        # Handle unknown command
        else:
            conn.send("unknown command".encode())
conn.close()