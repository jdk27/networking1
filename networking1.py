import socket

address = "insecure.stevetarzia.com"
remote_ip = socket.gethostbyname(address)
# bad request
request = "GET / HTTP/1.0\nHost: " + address + "\n\n"

# set up a client socket and send an HTTP GET request
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((remote_ip, 80))
client.send(bytes(request, 'utf-8'))

# when recv returns 0 bytes, the server has closed the connection
result = client.recv(1000)
while(len(result) > 0):
    result = client.recv(1000)
    print(result)
client.close()
