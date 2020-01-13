import socket

port = 1002 #input from command line

#Creating the socket
accept_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Binding the port to the socket
accept_s.bind(('',port))
accept_s.listen(1)
print('we are listening')

# Readings the request from the client socket
while True:
    print('here here here')
    conn, addr = accept_s.accept()
    print('waiting to accept', conn)
    cfile = conn.makefile('rw', 0) 

    line = cfile.readline().strip() 
    print('here')

    # Lets see if this works
    cfile.write('HTTP/1.0 200 OK\n\n') 
    cfile.write('<html><head><title>Welcome %s!</title></head>' %(str(caddr))) 
    cfile.write('<body><h1>Follow the link...</h1>') 
    cfile.write('All the server needs to do is ') 
    cfile.write('to deliver the text to the socket. ') 
    cfile.write('It delivers the HTML code for a link, ') 
    cfile.write('and the web browser converts it. <br><br><br><br>') 
    cfile.write('<font size="7"><center> <a href="http://python.about.com/index.html">Click me!</a> </center></font>') 
    cfile.write('<br><br>The wording of your request was: "%s"' %(line)) 
    cfile.write('</body></html>') 

    cfile.close() 
    conn.close() 
