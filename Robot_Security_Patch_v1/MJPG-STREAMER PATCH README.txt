Installation Instructions

NOTE!
Lighttpd and MJPG-Streamer must already be compiled and installed on the host system for this
patch to operate

Merge all files in the directory: ./MJPG-Streamer_Patch/lighttpd into /etc/lighttpd on the robot host machine
then restart the lighttpd process via sudo "/etc/init.d/lighttpd restart"

Tested with Lighttpd version
1.4.55


"How to use" instructions

- Run MJPG-Streamer through navigating to its directory and the command "sudo sh start.sh"
- In a seperate terminal navigate to the lighttpd directory with command "cd /etc/lighttpd"
- Start lighttpd with patches configuration file "sudo lighttpd -f lighttpd.conf"
- Block network access to MJPG-Streamer's default HTTP port (8080) by running the commands:
      - "iptables -A INPUT -p tcp -s localhost --dport 8080 -j ACCEPT"
      - "iptables -A INPUT -p tcp --dport 8080 -j DROP"
- Navigate the client to the video stream via Microsoft Edge pointed at the url:
      - "https//(IP ADDRESS OF SERVER):4433"
- Accept the certificate warning if prompted