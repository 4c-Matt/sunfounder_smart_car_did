# HANDLES ALL ENCRYPTION AND DECRYPTION #

#AES - Symmetric Key Encryption


def generate_session_key():
    from Crypto.Random import get_random_bytes
    key = get_random_bytes(16)
    return key

def encrypt(raw_data, key):

    from Crypto.Cipher import AES

    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(raw_data)

    encrypted_data = cipher.nonce, tag, ciphertext

    return encrypted_data

def decrypt(encrypted_data, key):
    from Crypto.Cipher import AES

    nonce = encrypted_data[0]
    tag = encrypted_data[1]
    ciphertext = encrypted_data[2]
     
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
    
    return decrypted_data

######TEST DATA SET#########
##key = new_key()
##print "\nThe key used for encryption is = ", key
##
##raw_data = "hello world"
##print "\nData to be encrypted = ", raw_data
##
##encrypted_data = encrypt(raw_data, key)
##print "\nEncrypted Data = ", encrypted_data
##
##decrypted_data = decrypt(encrypted_data, key)
##print "\nData decrypted = ", decrypted_data
############################


#AES - ASSYMETRIC KEY ENCRYPTION



def generate():
    from Crypto.PublicKey import RSA

    secret_code = "Nothing is true and everything is possible"
    key = RSA.generate(2048)
    encrypted_key = key.export_key(passphrase=secret_code, pkcs=8,
                                  protection="scryptAndAES256-CBC")

    file_out = open("rsa_key.bin", "wb")
    file_out.write(encrypted_key)

    print(key.publickey().export_key())


def read():
    from Crypto.PublicKey import RSA

    secret_code = "Nothing is true and everything is possible"
    encoded_key = open("rsa_key.bin", "rb").read()
    key = RSA.import_key(encoded_key, passphrase=secret_code)

    print(key.publickey().export_key())

##############################################
from socket import *

def socket_client(port, data):

    
    HOST =  '192.168.1.15'  #  # Server(Raspberry Pi) IP address
    PORT = port
    BUFSIZ = 1024             # buffer size
    ADDR = (HOST, PORT)

    tcpCliSock = socket(AF_INET, SOCK_STREAM)   # Create a socket
    tcpCliSock.connect(ADDR)  

    tcpCliSock.send(data)

def socket_host(port):
  
    HOST = ''           # The variable of HOST is null, so the function bind( ) can be bound to all valid addresses.
    PORT = port
    BUFSIZ = 1024       # Size of the buffer
    ADDR = (HOST, PORT)

    tcpSerSock = socket(AF_INET, SOCK_STREAM)    # Create a socket.

    tcpSerSock.bind(ADDR)    # Bind the IP address and port number of the server. 
    tcpSerSock.listen(1)     # The parameter of listen() defines the number of connections permitted at one time. Once the 
                             # connections are full, others will be rejected. 

    tcpSerSock.settimeout(5)

    try:
        data_recieved = False
        while data_recieved == False:
                print "Waiting for connection..."

                tcpCliSock, addr = tcpSerSock.accept()

                while True:
                    data =''
                    data = tcpCliSock.recv(BUFSIZ)
                    print "TEST data = ", data
                    if not (data == ''):
                        print "Data Recieved = ", data
                        data_recieved = True
                        print "Data recieved set to true"
                        break
                    if not data:
                        print "Session closed by client"
                        break
    except timeout:
        print "#####\nERROR!!!\nConnection timed out :(\n#####"
        
    print "Shutting down server..."
    tcpSerSock.close()
    return data

##############################################



def keypair():

    from Crypto.PublicKey import RSA
    key = RSA.generate(2048)

    private_key = key.export_key()
    

    public_key = key.publickey().export_key()
 

    return private_key, public_key


    
    #private_key = key.export_key()
    #file_out = open("private.pem", "wb")
    #file_out.write(private_key)

    #public_key = key.publickey().export_key()
    #file_out = open("public.pem", "wb")
    #file_out.write(public_key)



def session_key_encrypt(recipient_key, session_key):

    #Stage 4
 

    
    from Crypto.PublicKey import RSA
    from Crypto.Cipher import AES, PKCS1_OAEP

    print "\nrecipient key = ", RSA.import_key(recipient_key)
    print "session_key = ", session_key

    #Import recipient public key - MAKE ROUTINE
    #recipient_key = RSA.import_key(open("public_client.pem").read())


    #Encrypt the session key with the public RSA key
    cipher_rsa = PKCS1_OAEP.new(RSA.import_key(recipient_key))
    enc_session_key = cipher_rsa.encrypt(session_key)

    print "encrypted session key = ",enc_session_key,"\n"
    return enc_session_key


def session_key_decrypt(private_key, encrypted_session_key):

    #Stage 6
    
    from Crypto.PublicKey import RSA
    from Crypto.Cipher import AES, PKCS1_OAEP

    #import recipient private key
    #private_key = RSA.import_key(open("private_client.pem").read())

    # Decrypt the session key with the private RSA key
    cipher_rsa = PKCS1_OAEP.new(RSA.import_key(private_key))
    session_key = cipher_rsa.decrypt(encrypted_session_key)

    return session_key

        
### 1 #
##private_key, public_key = keypair()
##
##print "private key = ", private_key
##print "public key = ", public_key
##
### 2 #
##client_public_key = socket_host()
##socket_client(public_key)
##
### 3 #
##session_key = generate_session_key
##
### 4 #
##encrypted_session_key = session_key_encrypt(client_public_key, session_key)
##
### 5 #
##encrypted_session_key = socket_host()
##socket_client(encrypted_session_key)
##
### 6 #
##session_key = session_key_decrypt(private_key, encrypted_session_key)

def robot_routine():
    #1#
    print "Starting section 1"
    private_key, public_key = keypair()
    #print "private key = ", private_key
    #print "public key = ", public_key

    #2#
    print "Starting section 2"
    port = 21567
    client_public_key = socket_host(port)

    #3#
    print "Starting section 3"
    session_key = generate_session_key()

    #4#
    print "Starting section 4"
    encrypted_session_key = session_key_encrypt(client_public_key, session_key)

    #5#
    print "Starting section 5"
    port = 21568
    socket_client(port, encrypted_session_key)

    #6#
    print "Starting section 6"

    print "ROBOT ROUTINE COMPLETE!!!!!!!!!!"
    
def client_routine():
    #1#
    print "Starting section 1"
    private_key, public_key = keypair()
    #print "private key = ", private_key
    #print "public key = ", public_key

    #2#
    print "Starting section 2"
    port = 21567
    socket_client(port, public_key)

    #3#
    print "Starting section 3"

    #4#
    print "Starting section 4"

    #5#
    print "Starting section 5"
    port = 21568
    encrypted_session_key = socket_host(port)

    #6#
    print "Starting section 6"
    session_key = session_key_decrypt(private_key, encrypted_session_key)
    print "session key = ", session_key

    print "CLIENT ROUTINE COMPLETE!!!!!!!!!!"
