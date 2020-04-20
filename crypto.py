###################################################################

# HANDLES ALL ENCRYPTION AND DECRYPTION #

# Utilises PyCryptodome:  https://github.com/Legrandin/pycryptodome

####################################################################

#RSA - Asymmetric Key Encryption for session key


def keypair():
    # Generates public and private RSA keys
    from Crypto.PublicKey import RSA

    key = RSA.generate(2048)

    private_key = key.export_key()
    public_key = key.publickey().export_key()
 
    return private_key, public_key


def generate_session_key():
    from Crypto.Random import get_random_bytes
    key = get_random_bytes(16)
    return key


def session_key_encrypt(recipient_key, session_key):
    
    from Crypto.PublicKey import RSA
    from Crypto.Cipher import AES, PKCS1_OAEP

    #Encrypt the session key with the public RSA key
    cipher_rsa = PKCS1_OAEP.new(RSA.import_key(recipient_key))
    enc_session_key = cipher_rsa.encrypt(session_key)

    return enc_session_key


def session_key_decrypt(private_key, encrypted_session_key):
    
    from Crypto.PublicKey import RSA
    from Crypto.Cipher import AES, PKCS1_OAEP

    # Decrypt the session key with the private RSA key
    cipher_rsa = PKCS1_OAEP.new(RSA.import_key(private_key))
    session_key = cipher_rsa.decrypt(encrypted_session_key)

    return session_key

##########################################

# AES - Symmetric key encryption for robot movement commands

def AES_encrypt(raw_data, key):

    from Crypto.Cipher import AES

    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(raw_data)

    encrypted_data = cipher.nonce, tag, ciphertext

    return encrypted_data

def AES_decrypt(encrypted_data, key):
    from Crypto.Cipher import AES

    nonce = encrypted_data[0]
    tag = encrypted_data[1]
    ciphertext = encrypted_data[2]
     
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
    
    return decrypted_data

###########################################

# Socket scripts - for every case where data needs to be transmitted
#                  to and from the client

from socket import *

def socket_client(HOST, PORT, data):
    
    BUFSIZ = 1024             # buffer size
    ADDR = (HOST, PORT)

    tcpCliSock = socket(AF_INET, SOCK_STREAM)   # Create a socket
    tcpCliSock.connect(ADDR)  

    tcpCliSock.send(data)

def socket_host(PORT):  
  
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
                    data =''
                    data = tcpCliSock.recv(BUFSIZ)
                    if not (data == ''):
                        data_recieved = True
                        break
                    if not data:
                        print "Session closed by client"
                        break
    except timeout:
        print "#####\nERROR!!!\nConnection timed out :(\n#####"
        
    #print "Shutting down server..."
    tcpSerSock.close()
    return data

#############################################
