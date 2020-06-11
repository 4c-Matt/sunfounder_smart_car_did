version = 0.6
print "#"*20,"\nROBOT ROUTINE\nVersion:",version,"\n","#"*20

import shared_modules.socket_scripts as socket_scripts
import shared_modules.crypto as crypto
import shared_modules.auth as auth
import shared_modules.RSA_key_exchange as RSA_key_exchange
import server.tcp_server as tcp_server

print "IP SETUP:"
port = 21550
ip = raw_input("What is the ip address of the CLIENT? \nFor example: 192.168.1.0\n")

print "#"*20,"\nAUTHENTICATION ROUTINE\n","#"*20
raw_input("Press ENTER to start the authentication routine...\n")
device_type = "server"
auth_status = auth.authentication_routine(ip, port, device_type)

print "#"*20,"\nSESSION KEY EXCHANGE\n","#"*20
print "\nTo avoid errors, press enter to start this server session key routine first and then the client routine after\n"
raw_input("Press ENTER to start the key exchange routine...\n")
session_key = RSA_key_exchange.RSA_routine(ip, port, device_type)

print "#"*20,"\nTCP ROBOT CONTROL SERVER\n","#"*20
raw_input("Press ENTER to HOST the ROBOT CONTROL server...\n")
tcp_server.run_server(session_key)
