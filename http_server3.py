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
    operation_start = line.find('/')+1
    operation_end = line.find('?')

    # operation = line[operation_location: operation_location + 7]
    operation = line[operation_start: operation_end]
    status_code = ''
    if operation != 'product':
        status_code = '404 Not Found'

    # Parse the rest of the request to get the operands
    operand_string = line[operation_end+1:line.find(' ', operation_end)]
    values = operand_string.split('&')
    operands = {}
    product = 1
    for variable in values:
        left = variable.find('=') + 1
        x = variable[left:].upper()
        try:
            number = float(x)
            if x == 'INF' or x == '+INF' or x == 'INFINITY' or x == '+INFINITY':
                operands[number] = '+Infinity'
            elif x == "-INF" or x == "-INFINITY":
                operands[number] = '-Infinity'
            else:
                operands[number] = number
        except ValueError:
            status_code = '400 Bad Request'

    if not status_code:
        status_code = '200 OK'
        # Do the math
        product = 1
        for operand in operands.keys():
            try:
                product *= operand
            except OverflowError:
                if product > 0 and number > 0 or product < 0 and number < 0:
                    product = float('+inf')
                else:
                    product = float('-inf')
        if product == float('+inf'):
            product = '+Infinity'
        elif product == float('-inf'):
            product = '-Infinity'

        response_body = json.dumps(
            {'operation': 'product', 'operands': list(operands.values()), 'result': product})
        header = 'HTTP/1.0 200 OK\r\nContent-Type: application/json\r\n\r\n'

        conn.send(header.encode())
        conn.send(response_body.encode())
    else:
        err = 'HTTP/1.0 ' + status_code + '\r\n'
        conn.send(err.encode())

    conn.close()
