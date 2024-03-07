#!/usr/bin/python3
import sys
import socket

# Function to print usage instructions
def print_usage():
    print("""
This Python script is designed to check for valid user names on a Simple Mail Transfer Protocol (SMTP) server.
It can be useful for verifying the existence of user accounts before sending emails. The script can be run from
the command line, accepting arguments for the SMTP server IP address, port, user name, and optional file paths
for loading or writing user names.
""")
    print("Usage: ./smtp_check_users_validatin.py <IP> <port> <USER_NAME> [OPTION]\nOptions:\n-h, --help  Show this help message\n-r <text_file_path>  load names from file\n-w <text_file_path>  write valid names in file ")
    exit(0)

# Print banner
print("""
       _   ____            _                
      | | |___ \          | |               
   ___| |   __) | __ _  __| |_      ___   _ 
  / _ \ |  |__ < / _` |/ _` \ \ /\ / / | | |
 |  __/ |  ___) | (_| | (_| |\ V  V /| |_| |
  \___|_| |____/ \__,_|\__,_| \_/\_/  \__, |
                                       __/ |
                                      |___/ 
""")
print("written by @ahmed el3adwy")

# Check if arguments are provided
if len(sys.argv) == 1 or sys.argv[1] == "-h" or sys.argv[1] == "--help":
    print_usage()

# Check if port is an integer
port = sys.argv[2]
if not port.isdigit():
    print("Error: Port must be an integer.")
    exit(0)

# Establish connection to SMTP server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect = s.connect((sys.argv[1], int(port)))
banner = s.recv(1024)
print("step 1")
print(banner)

# Check for '-r' option or direct user name
not_found_user_error = "Recipient address rejected:"
if sys.argv[3] != "-r":
    user = sys.argv[3]
    s.send(('VRFY ' + user + '\r\n').encode())
    result = s.recv(1024)
    print("step 2")
    if not_found_user_error.encode() not in result:
        print("user found: " + user)
    else:
        print("user not found: " + user)
else:
    file_path = sys.argv[4]
    file2 = None

    # Check for '-w' option
    if len(sys.argv) == 7:
        file_path2 = sys.argv[6]
        try:
            file2 = open(file_path2, 'w')
        except IOError:
            print("Error: Unable to create or write to the file.") 


    print("step 3")
    try:
        with open(file_path, "r") as file: 
            for line in file:
                try:
                    s.send(('VRFY ' + line).encode())
                    result = s.recv(1024)
                except IOError:
                    print("Error:Bad recipient address syntax.")
                    exit(0)
                if len(sys.argv) != 7:
                    if not_found_user_error.encode() not in result:
                        print("user found: " + line)
                    else:
                        print("user not found: " + line)
                else:
                    if not_found_user_error.encode() not in result:
                        print("user found: " + line)
                        file2.write(line)
                    else:
                        print("user not found: " + line)
            if len(sys.argv) == 7:
                print("------------------->file load successfully<-------------------")
    except IOError:
        print("Error: Unable to read wordlist.")
    # Close file and socket
    if file2:
        file2.close()
s.close()
