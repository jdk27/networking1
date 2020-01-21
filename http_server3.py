import socket
import os
import sys
import json

port = int(sys.argv[1])  # input from command line

# Creating the socket
accept_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Binding the port to the socket
accept_s.bind(('', port))
accept_s.listen(1)
print('we are listening')

# Readings the request from the client socket
while True:
    conn, addr = accept_s.accept()
    request = conn.recv(2048).decode()
    line = request.strip()
    end_line = line.find('\r\n')
    print('end line: ', end_line)
    line = line[:end_line]
    print('here is the line: ', line)
    print('we done with the line')

    # Parse the request to get the operation

    operation_location = line.find('/')+1
    operation_right = line.find('?')
    # operation = line[operation_location: operation_location + 7]
    operation = line[operation_location: operation_right]
    status_code = ''
    if operation != 'product':
        status_code = '404 Not Found'

    # Parse the rest of the request to get the operands
    print('the line before rest: ',line)
    rest = line[operation_location + 8:-9]
    print('rest: ',rest)
    values = rest.split('&')
    print('values: ', values)
    print('operation: ', operation)
    operands = []
    for variable in values:
        left = variable.find('=') + 1
        x = variable[left:]
        try:
            x = float(x)
        except:
            print('')

        if (not isinstance(x,float)) and not status_code:
            status_code = '400 Bad Request'
        operands.append(x)
    print('operands: ', operands)

    if not status_code:
        status_code = '200 OK'
        # Do the math
        product = 1
        for operand in operands:
            product = operand * product

        # Format into JSON
        response_body = json.dumps(
            {'operation': 'product', 'operands': operands, 'result': product})
        okay = 'HTTP/1.0 200 OK\r\n'
        content_type = 'Content-Type: application/json\r\n\r\n'
    
        conn.send(okay.encode())
        conn.send(content_type.encode())
        conn.send(response_body.encode())
    else:
        err = 'HTTP/1.0 ' + status_code + '\r\n'
        conn.send(err.encode())

    conn.close()

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
