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


# Readings the request from the client socket
while True:
    conn, addr = accept_s.accept()
    request = conn.recv(2048).decode()
    line = request.strip()
    end_line = line.find('\r\n')
    line = line[:end_line]


    # Parse the request to get the operation

    operation_location = line.find('/')+1
    operation_right = line.find('?')
    # operation = line[operation_location: operation_location + 7]
    operation = line[operation_location: operation_right]
    status_code = ''
    if operation != 'product':
        status_code = '404 Not Found'

    # Parse the rest of the request to get the operands
    rest = line[operation_location + 8:-9]
    values = rest.split('&')
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

