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

    # Parse the request to get the operands
    line = cfile.readline().strip() 
    operation_location = line.find('/')+1
    operation = line[operation_location: operation_location + 7]
    rest = line[operation_location +8:-9]
    print(rest)
    values = rest.split('&')
    print(values)
    print(operation)
    operands = []
    for variable in values:
        left = variable.find('=') + 1
        operands.append(variable[left:])
    print(operands)

    # Do the math
    product = 1
    for operand in operands:
        product = operands * product

    # Format into JSON

    # Write the response back to the file?


    # if requested_file and requested_file in os.listdir("pages"):
    #     cfile.write('HTTP/1.0 200 OK\n\n')
    #     print('HTTP/1.0 200 OK\n\n')
    #     response = open('pages/' + requested_file, 'r') 
    #     contents = response.read()
    #     cfile.write(contents)
    # # Need better way to check if name but not .html exists than just making a new split list and checking through
    # # elif request_file.split('.')[0] in :
    #     # cfile.write('HTTP/1.0 403 Forbidden\n\n')
    #     # print('HTTP/1.0 403 Forbidden\n\n')
    # else:
    #     cfile.write('HTTP/1.0 404 Not Found\n\n') 
    #     print('HTTP/1.0 404 Not Found\n\n') 

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


    # cfile.close() 
    # conn.close() 