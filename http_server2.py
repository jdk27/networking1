import socket
import select
import os


# Creating the socket
accept_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Binding socket to the port
port = 1002  # input from command line
accept_s.bind(('', port))
accept_s.listen(1)
print('we are listening')

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
                cfile = s.makefile('rw', 248)
                line = cfile.readline().strip()
                right = line.find('.htm')+5
                left = line.find('/')+1
                requested_file = line[left:right]

                if requested_file and requested_file in os.listdir('pages'):
                    cfile.write('HTTP/1.0 200 OK\n\n')
                    response = open('pages/' + requested_file, 'r')
                    contents = response.read()
                    cfile.write(contents)
                else:
                    cfile.write('HTTP/1.0 404 Not Found\n\n')

                cfile.close()
                s.close()
                read_list.remove(s)
