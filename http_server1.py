import socket
import os
import sys

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

    # Parse the response to see what file they want
    line = request.strip()
    left = line.find('/') + 1
    right = line.find(' ', left)
    requested_file = line[left:right]
    extension = requested_file[requested_file.find('.'):]
    good_extension = extension == '.htm' or extension == '.html'

    # get the path to the current working directory and the files in it
    cwd = os.getcwd()
    cwd_files = os.listdir(cwd)

    # if there's a matching htm or html file that's in the current working directory
    if requested_file and requested_file in cwd_files and good_extension:
        path = cwd+'/'+requested_file
        file_size = str(os.path.getsize(path))
        header = 'HTTP/1.0 200 OK\r\n' + 'Content-Length: ' + file_size + \
            '\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n'
        conn.send(header.encode())
        response = open(requested_file, 'r')
        body = response.read()
        conn.send(body.encode())

    # if there's a matching file in the current working directory but isn't .htm or .html
    elif requested_file and requested_file in cwd_files and not good_extension:
        forbidden = 'HTTP/1.0 403 FORBIDDEN\n\n'
        conn.send(forbidden.encode())

    # else there is not a matching file in the current working directory
    else:
        not_found = 'HTTP/1.0 404 Not Found\n\n'
        conn.send(not_found.encode())

    conn.close()
