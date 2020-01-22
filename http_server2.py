import socket
import select
import os
import sys


# Creating the socket
accept_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Binding socket to the port
port = int(sys.argv[1])  # input from command line
accept_s.bind(('', port))
accept_s.listen(1)

# list of request sockets
open_connections = {}

# Readings the request from the client socket
while True:
    # Having a new connection arrive on these sockets makes them available for reading
    read_list = []
    read_list.append(accept_s)
    while read_list:
        readable, writable, exceptional = select.select(
            read_list, [], read_list)
        for s in readable:
            if s is accept_s:
                conn, addr = accept_s.accept()
                conn.setblocking(0)
                read_list.append(conn)
                open_connections[conn] = []
            else:
                request = s.recv(2048).decode()

                line = request.strip()
                left = line.find('/') + 1
                right = line.find(' ', left)
                requested_file = line[left:right]
                extension = requested_file[requested_file.find('.'):]
                file_name = requested_file.split('.')[0]
                good_extension = extension == '.htm' or extension == '.html'

                cwd = os.getcwd()
                cwd_files = os.listdir(cwd)

                if requested_file and requested_file in cwd_files and good_extension:
                    path = cwd+'/'+requested_file
                    file_size = str(os.path.getsize(path))
                    header = 'HTTP/1.0 200 OK\r\n' + 'Content-Length: ' + file_size + \
                        '\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n'
                    s.send(header.encode())
                    response = open(requested_file, 'r')
                    body = response.read()
                    s.send(body.encode())
                elif requested_file and requested_file in cwd_files and not good_extension:
                    forbidden = 'HTTP/1.0 403 FORBIDDEN\n\n'
                    conn.send(forbidden.encode())
                else:
                    not_found = 'HTTP/1.0 404 Not Found\n\n'
                    s.send(not_found.encode())

                s.close()
                read_list.remove(s)
