import socket
import select
import os
import sys


# Creating the socket
accept_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Binding socket to the port
port = int(sys.argv[1]) #input from command line
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
                request = s.recv(2048).decode()

                line = request.strip()
                right = line.find('.') + 5
                left = line.find('/') + 1
                requested_file = line[left:right]
                file_name = requested_file.split('.')[0]
                
                pages_dict = {}
                for page in os.listdir("pages"):
                    page = page.split('.')
                    pages_dict[page[0]] = page[1]

                if requested_file and requested_file in os.listdir('pages'):
                    okay = 'HTTP/1.0 200 OK\n\n'
                    s.send(okay.encode())
                    response = open('pages/' + requested_file, 'r')
                    contents = response.read()
                    s.send(contents.encode())
                elif file_name in pages_dict:
                    forbidden = 'HTTP/1.0 403 FORBIDDEN\n\n'
                    print('here is the file name: ', file_name)
                    print('forbidden')
                    conn.send(forbidden.encode()) 
                else:
                    not_found = 'HTTP/1.0 404 Not Found\n\n'
                    s.send(not_found.encode()) 
                    print('not find hehe')

                s.close()
                read_list.remove(s)
