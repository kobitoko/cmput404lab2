import socket

# Using Sockets from the OS to make clients.
# socket.AF_INET means use this socket to communicate to the internet
# socket.SOCK_STREAM means we want to use TCP!
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# this function tries to do C, hence 1 tuple as argument.
clientSocket.connect(("www.google.com",80))

# \r\n mean CR+LF which is windows new line
clientSocket.sendall("GET / HTTP/1.0\r\n\r\n")

# Loop to receive things:
while(1):
    # Ask for 1024bytes at a time.
    part = clientSocket.recv(1024)
    if(len(part) > 0):
        print part
    else: # part will be "" when the connection is done and we can exit.
        exit(0)

