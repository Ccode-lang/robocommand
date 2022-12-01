#define your variables here


counter = 0




def mainloop():
    global counter
    print(str(counter))
    counter += 1

def before(addr):
    print(addr)
    global counter
    counter = 0

def loops(arg):
    return False