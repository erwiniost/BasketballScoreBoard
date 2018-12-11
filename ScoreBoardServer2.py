# load additional Python module
import socket
import _thread
from tkinter import *
from tkinter import font
import pyglet

# create TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# retrieve local hostname
local_hostname = socket.gethostname()

# get fully qualified hostname
local_fqdn = socket.getfqdn()

# get the according IP address
ip_address = socket.gethostbyname(local_hostname)

# output hostname, domain name and IP address
print("working on %s (%s) with %s" % (local_hostname, local_fqdn, ip_address))

# bind the socket to the port 23456
server_address = (ip_address, 23456)
print('starting up on %s port %s' % server_address)
sock.bind(server_address)


def quit(*args):
	root.destroy()


root = Tk()
sound = pyglet.media.load(r'horn.mp3')

root.attributes("-fullscreen", True)
#root.geometry("640x480")
root.configure(background='black')
root.bind("<Escape>", quit)
root.bind("x", quit)

w, h = root.winfo_screenwidth(), root.winfo_screenheight()

fontSizeTimer = int(w * 0.18)
fontSizeFouls = int(w * 0.07)
fontSizePeriodo = int(w * 0.07)
fontSizeScore = int(w * 0.1)
fontSizeTitle = int(w * 0.022)

FONT_TIMER = font.Font(family='DJB Get Digital', size=fontSizeTimer)
FONT_SCORE = font.Font(family='DJB Get Digital', size=fontSizeScore)
FONT_FOULS = font.Font(family='DJB Get Digital', size=fontSizeFouls)
FONT_PERIODOS = font.Font(family='DJB Get Digital', size=fontSizePeriodo)
FONT_TITLES = font.Font(family='Arial', size=fontSizeTitle)
COLOR_BORDER = "white"

sideFrameSize = w * 0.20
midFrameSize = w * 0.6
frameTituloHeight = h * 0.05
frameTimerHeight = h * 0.05

print(w)

frameTitulo = Frame(root, bg="black", highlightbackground=COLOR_BORDER, highlightcolor=COLOR_BORDER, highlightthickness=2, height=frameTituloHeight)
frameTitulo.pack(fill=X, anchor=N, side=TOP)
labelTitulo = Label(frameTitulo, text="CAMPEONATO ABSS", font=FONT_TITLES, foreground="white", background="black")
labelTitulo.pack(padx=5, ipadx=5)

frameTimer = Frame(root, bg="black", highlightbackground=COLOR_BORDER, highlightcolor=COLOR_BORDER, highlightthickness=2, height=frameTimerHeight)
frameTimer.pack(fill=X, anchor=N, side=TOP)


state = False

# Our time structure [min, sec, centsec]
timer = [10, 0, 0]
# The format is padding all the
pattern = '{0:02d}:{1:02d}:{2:02d}'


lblTime = Label(frameTimer, text="10:00:00", font=FONT_TIMER, foreground="yellow", background="black", relief="groove")
lblTime.pack(fill=X)





def getConnected():
    # listen for incoming connections (server mode) with one connection at a time
    sock.listen(1)
    connection, client_address = sock.accept()

    try:
        # show who connected to us
        print('connection from', client_address)

            # receive the data in small chunks and print it
        while True:
            data = connection.recv(64)
            if data:
                dataStr = data.decode()
                opcion, valor = dataStr.split("|")
                if opcion == 'startclock':
                    start()
                elif opcion == 'stopclock':
                    pause()
                print ("Data: %s" % data)
            else:
                # no more data -- quit the loop
                print ("no more data.")
                break
    finally:
        # Clean up the connection
        connection.close()




# To start the kitchen timer
def start():
    global state
    state = True


# To pause the kitchen timer
def pause():
    global state
    state = False


def update_timeText():
    if state:
        global timer
        # Every time this function is called,
        # we will increment 1 centisecond (1/100 of a second)
        timer[2] -= 1

        # Every 100 centisecond is equal to 1 second
        if timer[2] <= 0:
            timer[2] = 99
            timer[1] -= 1
        # Every 60 seconds is equal to 1 min
        if timer[1] <= 0:
            timer[0] -= 1
            timer[1] = 59
        # We create our time string here
        timeString = pattern.format(timer[0], timer[1], timer[2])
        # Update the timeText Label box with the current time
        lblTime.configure(text=timeString)
        # Call the update_timeText() function after 1 centisecond
    root.after(10, update_timeText)




_thread.start_new(getConnected, ())
update_timeText()

root.mainloop()

