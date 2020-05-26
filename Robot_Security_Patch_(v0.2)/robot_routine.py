version = 0.2

import shared_modules.socket_scripts as socket_scripts
import shared_modules.crypto as crypto
import server.tcp_server as tcp_server


def sk_exchange_robot(ip):
    
    print "Generating and exchanging session key..."

    #SK1
    private_key, public_key = crypto.keypair()

    #SK2#
    port = 21567
    client_public_key = socket_scripts.socket_host(port)

    #SK3#
    session_key = crypto.generate_session_key()

    #SK4#
    encrypted_session_key = crypto.session_key_encrypt(client_public_key, session_key)

    #SK5#
    #ip = "192.168.1.2"
    port = 21568
    socket_scripts.socket_client(ip, port, encrypted_session_key)

    print "Login Session key = ", session_key

    return session_key


print "#"*20,"\nROBOT ROUTINE\nVersion:",version,"\n","#"*20
print "IP SETUP:"
ip = raw_input("What is the ip address of the CLIENT? \nFor example: 192.168.1.0\n")
print "#"*20,"\nSESSION KEY EXCHANGE\n","#"*20

print "\nTo avoid errors, start the following routine then immediatly start the client routine\n"
raw_input("Press ENTER to start the key exchange routine...\n")
session_key = sk_exchange_robot(ip)

print "#"*20,"\nTCP ROBOT CONTROL SERVER","#"*20
raw_input("Press ENTER to HOST the ROBOT CONTROL server...")
tcp_server.run_server(session_key)
