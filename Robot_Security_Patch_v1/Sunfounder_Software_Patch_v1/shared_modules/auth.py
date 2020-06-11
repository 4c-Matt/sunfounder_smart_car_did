###################################################################
# Authentication Scripts

# AUTHENTICATES THE CLIENT TO THE SERVER SESSION

###################################################################

#Import all necessary modules
import shared_modules.socket_scripts as socket_scripts
import random
import string

# Generates the five character authentication code which the client enters
# later to authenticate the client/server session 
def generate_authentication_string():
    letters = string.ascii_uppercase
    authentication_string = "".join(random.choice(letters) for i in range (5))
    return authentication_string


# The authentication process ran by the server
def authentication_server(ip, port):

    print "An authentication code will be displayed on this terminal."
    print "Within 30 seconds enter the same code on the client terminal to authenticate the client" 
    raw_input("\nPress enter to display the authentication code...\n")

    # Calls the function dedicated to generating the authentication code,
    # saves the code to a variable and displays it on the terminal window
    # for the client to copy and input
    authentication_string = generate_authentication_string()
    print "The authentication string is:\n\n", authentication_string
    print "\n\nPlease enter this string on the client terminal within 30 seconds"

    # Defines the number of permitted login attempts allowed
    login_attempts = 3
    attempt_status = ""

    # Starts a while loop which terminates when the client runs out of
    # login attempts and the recieved client authentication code does
    # not match the one stored by the server
    while (login_attempts > 0) and (not (attempt_status == "success")):
        
        # Sets up the socket ready to recieve the code from the client
        attempt_data = socket_scripts.socket_host(port)

        # Checks to see whether the client code inputted matches the
        # correct serverside value and stores this status in a variable.
        # If the attempt fails the login attempt value reduces by one.
        # If the inputted code is incorrect and the the amount of remaining
        # attempts are zero then the status fails whereas if there are
        # attempts remaining the status is set to retry
        if attempt_data == authentication_string:

            attempt_status = "success"            
            print "Authentication Succeeded"

            # Sends the attempt status to the client via socket            
            socket_scripts.socket_client(ip, port, attempt_status)
        else:           
            login_attempts = login_attempts - 1
            if login_attempts == 0:
                attempt_status = "failed"
                print "Authentication Failed!!!\nPlease restart the program and try again"
            else:
                attempt_status = "retry"
                print "Login Code Incorrect!\nAttempts Remaining = ",login_attempts

            # Sends the attempt status to the client via socket
            socket_scripts.socket_client(ip, port, attempt_status)
            
        print "\n"
         
    
    return attempt_status
            

# The authentication process ran by the client
def authentication_client(ip, port):
    attempt_status = ""

    # Starts a while loop that terminates once the authentication server has failed
    # or succeded.
    while not(attempt_status == "success" or attempt_status == "failed"):

        # The user enters the string shown by the server and sends the value
        # via socket. The client then waits for a response as to whether the
        # entered code was correct
        user_attempt = raw_input("Please enter the 5 digit authentication string displayed on the server terminal\n")
        socket_scripts.socket_client(ip, port, user_attempt)
        attempt_status = socket_scripts.socket_host(port)

        # Displays a message to the user informing them whether the authentication
        # was sucessful, failed or was wrong and needs to be attempted again
        if attempt_status == "success":
            print "Authentication Succeeded"
        elif attempt_status == "retry":
            print "Login Code Incorrect. Please try again"
        elif attempt_status == "failed":
            print "Authentication Failed!!!\nPlease restart the program and try again"
        print "\n"
        
    return attempt_status

# Decides whether to run the authentication client or server scripts based on the
# parsed device type value
def authentication_routine(ip, port, device_type):
    if device_type == "server":
        auth_status = authentication_server(ip, port)
    elif device_type == "client":
        auth_status = authentication_client(ip, port)

    # Runs after the authentication routine has finished. If the routine failed
    # the program exits. If it succeeded then the function returns the
    # success status
    if auth_status == "failed":
        raw_input("Shutting down program")
        quit()
    elif auth_status == "success":
        return auth_status
    
