import socket

address = "insecure.stevetarzia.com"
path = "/basic.html"
remote_ip = socket.gethostbyname(address)
request = "GET " + path + " HTTP/1.0\nHost: " + address + "\n\n"

# set up a client socket and send an HTTP GET request
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((remote_ip, 80))
client.send(bytes(request, 'utf-8'))

# when recv returns 0 bytes, the server has closed the connection
result = client.recv(1000)
print('first result:')
print(result)
print(result[9:12])
response_code = result[9:12]
if response_code == b'301':
    print('301 Response detected')
elif response_code == b'302':
    print('302 response detected')
else:
    print('not a 301 or 302 response')
while(len(result) > 0):
    result = client.recv(1000)
    print(result)
client.close()
