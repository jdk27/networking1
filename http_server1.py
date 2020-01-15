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
    cfile = conn.makefile('rw', 248) 

    # Parse the response to see what file they want
    line = cfile.readline().strip() 
    right = line.find('.htm') + 5
    left = line.find('/') + 1
    print('left', left)
    print('right', right)
    print('Requested File: ', line[left:right])
    requested_file = line[left:right]
    print('Full request: ', line)
    print('no ending: ', requested_file.split('.')[0])

    if requested_file and requested_file in os.listdir("pages"):
        cfile.write('HTTP/1.0 200 OK\n\n')
        print('HTTP/1.0 200 OK\n\n')
        response = open('pages/' + requested_file, 'r') 
        contents = response.read()
        cfile.write(contents)
    # Need better way to check if name but not .html exists than just making a new split list and checking through
    # elif request_file.split('.')[0] in :
        # cfile.write('HTTP/1.0 403 Forbidden\n\n')
        # print('HTTP/1.0 403 Forbidden\n\n')
    else:
        cfile.write('HTTP/1.0 404 Not Found\n\n') 
        print('HTTP/1.0 404 Not Found\n\n') 

    # If the file exists
    # cfile.write('HTTP/1.0 200 OK\n\n') 
    # # print('files available: ', os.listdir("pages"))
    # response = open('pages/rfc2616.html', 'r')
    # contents = response.read()
    # # print('hope this works: ', contents) 
    # cfile.write(contents)


    # # If the file does not exists
    # cfile.write('HTTP/1.0 404 Not Found\n\n') 
    # # If the file exists but doesn't end in htm/l
    # cfile.write('HTTP/1.0 403 Forbidden\n\n') 


    cfile.close() 
    conn.close() 