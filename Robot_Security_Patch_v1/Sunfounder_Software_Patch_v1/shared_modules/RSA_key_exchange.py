###################################################################
# RSA key exchange

# RSA ENCRYPTION ROUTINE FOR USE WHEN EXCHANGING THE SESSION KEY

###################################################################

import shared_modules.socket_scripts as socket_scripts
import shared_modules.crypto as crypto
import shared_modules.auth as auth

def RSA_client(ip, port):

    print "Generating and exchanging session key..."
    
    #SK1#
    private_key, public_key = crypto.keypair()

    #SK2#
    #port = 21566
    socket_scripts.socket_client(ip, port, public_key)

    #SK5#
    #port = 21567
    encrypted_session_key = socket_scripts.socket_host(port)

    #SK6#
    session_key = crypto.session_key_decrypt(private_key, encrypted_session_key)

    print "Session key = ", session_key

    return session_key


def RSA_server(ip, port):
    
    print "Generating and exchanging session key..."

    #SK1
    private_key, public_key = crypto.keypair()

    #SK2#
    #port = 21566
    client_public_key = socket_scripts.socket_host(port)

    #SK3#
    session_key = crypto.generate_session_key()

    #SK4#
    encrypted_session_key = crypto.session_key_encrypt(client_public_key, session_key)

    #SK5#
    #ip = "192.168.1.2"
    #port = 21567
    socket_scripts.socket_client(ip, port, encrypted_session_key)

    print "Session key = ", session_key

    return session_key


def RSA_routine(ip, port, device_type):
    if device_type == "server":
        key = RSA_server(ip, port)
    elif device_type == "client":
        key = RSA_client(ip, port)
    return key
    
