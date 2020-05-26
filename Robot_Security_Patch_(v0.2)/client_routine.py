version = 0.2

import shared_modules.socket_scripts as socket_scripts
import shared_modules.crypto as crypto
from socket import *
import time


def sk_exchange_client(ip):

    print "Generating and exchanging session key..."
    
    #SK1#
    private_key, public_key = crypto.keypair()

    #SK2#
    #ip = "192.168.1.2"
    #time.sleep(10)
    port = 21567
    socket_scripts.socket_client(ip, port, public_key)

    #SK5#
    port = 21568
    #time.sleep(2)
    encrypted_session_key = socket_scripts.socket_host(port)

    #SK6#
    session_key = crypto.session_key_decrypt(private_key, encrypted_session_key)

    print "Login Session key = ", session_key

    return session_key

def sunfounder_client(ip, key):
        #!/usr/bin/env python
        # -*- coding: utf-8 -*-
        from Tkinter import Tk, Button, Label, Scale, HORIZONTAL

        print "Connecting to IP", ip

        ctrl_cmd = ['forward', 'backward', 'left', 'right', 'stop', 'read cpu_temp', 'home', 'distance', 'x+', 'x-', 'y+', 'y-', 'xy_home']

        top = Tk()   # Create a top window
        top.title('Sunfounder Raspberry Pi Smart Video Car')

        HOST = ip    # Server(Raspberry Pi) IP address
        PORT = 21567
        BUFSIZ = 1024             # buffer size
        ADDR = (HOST, PORT)

        tcpCliSock = socket(AF_INET, SOCK_STREAM)   # Create a socket
        tcpCliSock.connect(ADDR)                    # Connect with the server
        # =============================================================================
        # The function is to send the command forward to the server, so as to make the 
        # car move forward.
        # ============================================================================= 
        def forward_fun(event):
                print "\nUser command = forward"
                print "Encrypted command = ",crypto.AES_encrypt('forward',key)[2]
                tcpCliSock.send(str(crypto.AES_encrypt('forward',key)))

        def backward_fun(event):
                print '\nUser command = backward'
                print "Encrypted command = ",crypto.AES_encrypt('backward',key)[2]
                tcpCliSock.send(str(crypto.AES_encrypt('backward',key)))

        def left_fun(event):
                print '\nUser command = left'
                print "Encrypted command = ",crypto.AES_encrypt('left',key)[2]
                tcpCliSock.send(str(crypto.AES_encrypt('left',key)))

        def right_fun(event):
                print '\nUser command = right'
                print "Encrypted command = ",crypto.AES_encrypt('right',key)[2]
                tcpCliSock.send(str(crypto.AES_encrypt('right',key)))

        def stop_fun(event):
                print '\nUser command = stop'
                print "Encrypted command = ",crypto.AES_encrypt('stop',key)[2]
                tcpCliSock.send(str(crypto.AES_encrypt('stop',key)))

        def home_fun(event):
                print '\nUser command = home'
                print "Encrypted command = ",crypto.AES_encrypt('home',key)[2]
                tcpCliSock.send(str(crypto.AES_encrypt('home',key)))

        def x_increase(event):
                print '\nUser command = x+'
                print "Encrypted command = ",crypto.AES_encrypt('x+',key)[2]
                tcpCliSock.send(str(crypto.AES_encrypt('x+',key)))

        def x_decrease(event):
                print '\nUser command = x-'
                print "Encrypted command = ",crypto.AES_encrypt('x-',key)[2]
                tcpCliSock.send(str(crypto.AES_encrypt('x-',key)))

        def y_increase(event):
                print '\nUser command = y+'
                print "Encrypted command = ",crypto.AES_encrypt('y+',key)[2]
                tcpCliSock.send(str(crypto.AES_encrypt('y+',key)))

        def y_decrease(event):
                print '\nUser command = y-'
                print "Encrypted command = ",crypto.AES_encrypt('y-',key)[2]
                tcpCliSock.send(str(crypto.AES_encrypt('y-',key)))

        def xy_home(event):
                print '\nUser command = xy_home'
                print "Encrypted command = ",crypto.AES_encrypt('xy_home',key)[2]
                tcpCliSock.send(str(crypto.AES_encrypt('xy_home',key)))

        # =============================================================================
        # Exit the GUI program and close the network connection between the client 
        # and server.
        # =============================================================================
        def quit_fun(event):
                print "\nShutting down program..."
                top.quit()
                tcpCliSock.send(str(crypto.AES_encrypt('stop',key)))
                tcpCliSock.close()

        # =============================================================================
        # Create buttons
        # =============================================================================
        Btn0 = Button(top, width=5, text='Forward')
        Btn1 = Button(top, width=5, text='Backward')
        Btn2 = Button(top, width=5, text='Left')
        Btn3 = Button(top, width=5, text='Right')
        Btn4 = Button(top, width=5, text='Quit')
        Btn5 = Button(top, width=5, height=2, text='Home')

        # =============================================================================
        # Buttons layout
        # =============================================================================
        Btn0.grid(row=0,column=1)
        Btn1.grid(row=2,column=1)
        Btn2.grid(row=1,column=0)
        Btn3.grid(row=1,column=2)
        Btn4.grid(row=3,column=2)
        Btn5.grid(row=1,column=1)

        # =============================================================================
        # Bind the buttons with the corresponding callback function.
        # =============================================================================
        Btn0.bind('<ButtonPress-1>', forward_fun)  # When button0 is pressed down, call the function forward_fun().
        Btn1.bind('<ButtonPress-1>', backward_fun)
        Btn2.bind('<ButtonPress-1>', left_fun)
        Btn3.bind('<ButtonPress-1>', right_fun)
        Btn0.bind('<ButtonRelease-1>', stop_fun)   # When button0 is released, call the function stop_fun().
        Btn1.bind('<ButtonRelease-1>', stop_fun)
        Btn2.bind('<ButtonRelease-1>', stop_fun)
        Btn3.bind('<ButtonRelease-1>', stop_fun)
        Btn4.bind('<ButtonRelease-1>', quit_fun)
        Btn5.bind('<ButtonRelease-1>', home_fun)

        # =============================================================================
        # Create buttons
        # =============================================================================
        Btn07 = Button(top, width=5, text='X+', bg='red')
        Btn08 = Button(top, width=5, text='X-', bg='red')
        Btn09 = Button(top, width=5, text='Y-', bg='red')
        Btn10 = Button(top, width=5, text='Y+', bg='red')
        Btn11 = Button(top, width=5, height=2, text='HOME', bg='red')

        # =============================================================================
        # Buttons layout
        # =============================================================================
        Btn07.grid(row=1,column=5)
        Btn08.grid(row=1,column=3)
        Btn09.grid(row=2,column=4)
        Btn10.grid(row=0,column=4)
        Btn11.grid(row=1,column=4)

        # =============================================================================
        # Bind button events
        # =============================================================================
        Btn07.bind('<ButtonPress-1>', x_increase)
        Btn08.bind('<ButtonPress-1>', x_decrease)
        Btn09.bind('<ButtonPress-1>', y_decrease)
        Btn10.bind('<ButtonPress-1>', y_increase)
        Btn11.bind('<ButtonPress-1>', xy_home)
        #Btn07.bind('<ButtonRelease-1>', home_fun)
        #Btn08.bind('<ButtonRelease-1>', home_fun)
        #Btn09.bind('<ButtonRelease-1>', home_fun)
        #Btn10.bind('<ButtonRelease-1>', home_fun)
        #Btn11.bind('<ButtonRelease-1>', home_fun)

        # =============================================================================
        # Bind buttons on the keyboard with the corresponding callback function to 
        # control the car remotely with the keyboard.
        # =============================================================================
        top.bind('<KeyPress-a>', left_fun)   # Press down key 'A' on the keyboard and the car will turn left.
        top.bind('<KeyPress-d>', right_fun) 
        top.bind('<KeyPress-s>', backward_fun)
        top.bind('<KeyPress-w>', forward_fun)
        top.bind('<KeyPress-h>', home_fun)
        top.bind('<KeyRelease-a>', home_fun) # Release key 'A' and the car will turn back.
        top.bind('<KeyRelease-d>', home_fun)
        top.bind('<KeyRelease-s>', stop_fun)
        top.bind('<KeyRelease-w>', stop_fun)

        spd = 50

        def changeSpeed(ev=None):
                tmp = 'speed'
                global spd
                spd = speed.get()
                data = tmp + str(spd)  # Change the integers into strings and combine them with the string 'speed'.  
                #print 'sendData = %s' % data
                print '\nUser command = ', data
                print "Encrypted command = ",crypto.AES_encrypt(data,key)[2]

                tcpCliSock.send(str(crypto.AES_encrypt(data,key)))  # Send the speed data to the server(Raspberry Pi)

        label = Label(top, text='Speed:', fg='red')  # Create a label
        label.grid(row=6, column=0)                  # Label layout

        speed = Scale(top, from_=0, to=100, orient=HORIZONTAL, command=changeSpeed)  # Create a scale
        speed.set(50)
        speed.grid(row=6, column=1)

        def main():
                top.mainloop()

        if __name__ == '__main__':
                main()



print "#"*20,"\nCLIENT ROUTINE\nVersion:",version,"\n","#"*20
print "IP SETUP:"
ip = raw_input("What is the ip address of the ROBOT? \nFor example: 192.168.1.0\n")
print "#"*20,"\nSESSION KEY EXCHANGE\n","#"*20

print "\nTo avoid errors, start the following routine immediatly after starting the robot routine \n"
raw_input("Press ENTER to start the key exchange routine...\n")
session_key = sk_exchange_client(ip)

print "#"*20
raw_input("Press enter to CONNECT to the ROBOT CONTROL server!")
sunfounder_client(ip,session_key)
