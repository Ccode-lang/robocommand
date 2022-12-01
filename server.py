import socket
import os
import sys
import threading
import importlib
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 5001))
s.listen(1)
runpro = False
connected = False



def roborun(code, addr):
    loops = []
    if code.loops("more"):
        loops = code.loops("list")
    code.before(addr)
    while True:
        global runpro
        if not runpro:
            break
        try:
            code.mainloop()
            for loop in loops:
                getattr(code, loop)()
        except Exception as e:
            print(type(e))
            print(e)
            runpro = False




while 1:
    if not connected:
        conn, addr = s.accept()
        connected = True
    data = conn.recv(1024)
    if not data:
        connected = False
        conn.close()
    if connected:
        if data.decode() == "quit":
            conn.send("conclose".encode())
            conn.close()
            connected = False
        elif data.decode().startswith("run "):
            try:
                robocode = __import__(data.decode()[4:], globals(), locals(), [], 0)
                pro = threading.Thread(target = roborun, args =(robocode, addr, ))
                importlib.reload(robocode)
                pro.start()
                runpro = True
            except:
                conn.send("failed to start".encode())
        elif data.decode().startswith("stop"):
            runpro = False
            pro.join()
        elif data.decode() == "quitserver":
            conn.send("conclose".encode())
            conn.close()
            s.close()
            sys.exit()
        elif data.decode().startswith("echo "):
            conn.send(data[5:])
        elif data.decode().startswith("upload "):
            filename = data.decode()[7:]
            file = open(filename, "a")
            while True:
                chunk = conn.recv(1024)
                print("test")
                print(chunk.decode())
                if not chunk.decode() == "EOF":
                    file.write(chunk.decode())
                else:
                    file.close()
                    break
        elif data.decode().startswith("rm "):
            filename = data.decode()[3:]
            try:
                os.remove(filename)
            except:
                conn.send("failed to remove file".encode())
        else:
            conn.send("unknown command".encode())
conn.close()