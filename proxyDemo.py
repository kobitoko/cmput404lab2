import socket
import os

# Client --> proxy --> server(google)
#    ^--------' ^--------' 

# dont follow redirects so no -iL
#curl -v 127.0.0.1:8000

# wait for client to connect to us first.
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 0 address means listen on any address that I can listen on this computer
# a port less than 1024 needs root.
clientSocket.bind(("0.0.0.0", 8000))

# parameter: how many connection the OS should hold. (Any more connection will be refused).
clientSocket.listen(5)

# Tell OS that the socket can be reused immediately. If you get Socket is in use error.
clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

while(1):
    (incomingSocket, address) = clientSocket.accept()
    print("We got a connection from %s!" %(str(address)))

    part = incomingSocket.recv(1024)
    pid = os.fork()
    if(pid==0): # we must be the child (clone) process, so we will handle proxying for this client
    
        googleSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        googleSocket.connect(("www.google.com",80))

        # Creates a deadlock because we only send the first 1024bytes:
        # curl -v 127.0.0.1:8000 -H "Host: www.google.ca"
        # Can solve this by making both sockets non-blocking
        # Tells the OS never to just hang here.
        incomingSocket.setblocking(0)
        googleSocket.setblocking(0)
                

        # Loop to receive things:
        while(1):
            # forwards client to google
            # skip the mesages of socket.error: [Errno 11] Resource temporarily unavailable
            skip = False
            try:
                part = incomingSocket.recv(1024)
            except socket.error, exception:
                if(exception.errno == 11):
                    skip = True
                else: # if it's not error 11, then continue crashing
                    raise
            if(not skip):
                if(len(part) > 0):
                    print "> " + part
                    googleSocket.sendall(part)
                else: # part will be "" when the connection is done and we can exit.
                    exit(0)
                    
            # forwards from google to client.
            skip = False
            try:
                part = googleSocket.recv(1024)
            except socket.error, exception:
                if(exception.errno == 11):
                    skip = True
                else:
                    raise
            if(not skip):
                if(len(part) > 0):
                    print "> " + part
                    incomingSocket.sendall(part)
                else:
                    exit(0)

