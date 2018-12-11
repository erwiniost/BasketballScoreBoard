# load additional Python modules
import socket
import time

# create TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# retrieve local hostname
local_hostname = socket.gethostname()

# get fully qualified hostname
local_fqdn = socket.getfqdn()

# get the according IP address
ip_address = socket.gethostbyname(local_hostname)

# bind the socket to the port 23456, and connect
server_address = (ip_address, 23456)
sock.connect(server_address)
print ("connecting to %s (%s) with %s" % (local_hostname, local_fqdn, ip_address))



while 1:
    input_var = input("Enter something: ")
    print("you entered " + input_var)
    opcion, valor = input_var.split("|")
    if opcion == 'quit':
        break
    new_data = str(input_var).encode("utf-8")
    sock.sendall(new_data)

# close connection
sock.close()