import crypto
import tcp_server


def sk_exchange_robot(ip):

    print "Generating and exchanging session key..."

    #SK1
    private_key, public_key = crypto.keypair()

    #SK2#
    port = 21567
    client_public_key = crypto.socket_host(port)
    #print "TEST = ", client_public_key

    #SK3#
    session_key = crypto.generate_session_key()

    #SK4#
    encrypted_session_key = crypto.session_key_encrypt(client_public_key, session_key)

    #SK5#
    #ip = "192.168.1.2"
    port = 21568
    crypto.socket_client(ip, port, encrypted_session_key)

    print "Login Session key = ", session_key

    return session_key



ip = raw_input("What is the ip address of the CLIENT? \nFor example: 192.168.1.0\n")

raw_input("Press enter to start the ROBOT routine...")
session_key = sk_exchange_robot(ip)

raw_input("Press enter to HOST the ROBOT CONTROL server...")
tcp_server.run_server(session_key)
