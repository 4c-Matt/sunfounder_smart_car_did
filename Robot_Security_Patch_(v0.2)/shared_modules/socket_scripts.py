###################################################################
# socket_scripts

# HANDLES CORE CLIENT/SERVER COMMUNICATION 

# Utilises socket

###################################################################

# MODULE IMPORT

from socket import *
import time

###################################################################

# Client Socket

def socket_client(HOST, PORT, data):
    print "SOCKET CLIENT"
    BUFSIZ = 1024             # buffer size
    ADDR = (HOST, PORT)

##    tcpCliSock = socket(AF_INET, SOCK_STREAM)   # Create a socket
##    tcpCliSock.connect(ADDR)
##    tcpCliSock.send(data)
    tcpCliSock = socket(AF_INET, SOCK_STREAM)
    
    connected = "false"
    retry_count = 0
    while connected == "false":
        try:
            tcpCliSock.connect(ADDR)
            connected = "true"
        except error:
            if retry_count <= 2: #Will go through 3 times
                print "Retrying connection..."
                time.sleep(2)
                retry_count = retry_count + 1
            else:
                print "ERROR! CONNECTION FAILED! PLEASE RESTART PROGRAM"
                exit()

    tcpCliSock.send(data)
###################################################################    

# Host Socket

def socket_host(PORT):
    print "SOCKET HOST"
  
    HOST = ''           # The variable of HOST is null, so the function bind( ) can be bound to all valid addresses.
    BUFSIZ = 1024       # Size of the buffer
    ADDR = (HOST, PORT)

    tcpSerSock = socket(AF_INET, SOCK_STREAM)    # Create a socket.

    tcpSerSock.bind(ADDR)    # Bind the IP address and port number of the server. 
    tcpSerSock.listen(1)     # The parameter of listen() defines the number of connections permitted at one time. Once the 
                             # connections are full, others will be rejected. 

    tcpSerSock.settimeout(10)

    try:
        data_recieved = False
        while data_recieved == False:
                #print "Waiting for connection..."

                tcpCliSock, addr = tcpSerSock.accept()
                        
                while True:
                    try:
                        data =''
                        data = tcpCliSock.recv(BUFSIZ)
                        if not (data == ''):
                            data_recieved = True
                            break
                        if not data:
                            print "Session closed by client"
                            break
                    except KeyboardInterrupt:
                        print "Socket Exception Triggered, waiting 1 second..."
                        time.sleep(1)
                        #FIX THIS THIS WILL CAUSE HANGS!!!!!!!!!!!!!!!!!!!!!!
    except timeout:
        print "#####\nERROR!!!\nSHUTTING DOWN SOCKET SERVER\n#####"
        tcpSerSock.close()
        quit()
        
    #print "Shutting down server..."
    tcpSerSock.close()
    return data

###################################################################
