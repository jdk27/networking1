import socket
import os
import sys

port = int(sys.argv[1]) #input from command line

#Creating the socket
accept_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Binding the port to the socket
accept_s.bind(('',port))
accept_s.listen(1)
print('we are listening')

# Readings the request from the client socket
while True:
    conn, addr = accept_s.accept()
    # cfile = conn.makefile('rw', 248)
    request = conn.recv(2048).decode()
    # capitalizedRequest = request.upper()
    # conn.send(request.encode())

    # Parse the response to see what file they want
    line = request.strip()
    right = line.find('.') + 5
    left = line.find('/') + 1
    requested_file = line[left:right]
    file_name = requested_file.split('.')[0]

    cwd = os.getcwd()

    pages_dict = {}
    for page in os.listdir(cwd):
        print(page)
        if page.find('.') != 0:
            page = page.split('.')
            pages_dict[page[0]] = page[1]
        else:
            pages_dict[page] = ''

    if requested_file and requested_file in os.listdir(cwd):
        okay = 'HTTP/1.0 200 OK\n\n'
        conn.send(okay.encode())
        response = open(requested_file, 'r') 
        contents = response.read()
        conn.send(contents.encode())

    elif file_name in pages_dict:
        forbidden = 'HTTP/1.0 403 FORBIDDEN\n\n'
        conn.send(forbidden.encode()) 

    else:
        not_found = 'HTTP/1.0 404 Not Found\n\n'
        conn.send(not_found.encode()) 

    conn.close() 