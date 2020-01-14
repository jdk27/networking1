import socket
import sys
from urllib.parse import urlparse


def send_request(url):
    host, path = get_host_and_path(url)
    remote_ip = socket.gethostbyname(host)
    request = format_request(host, path)
    client.connect((remote_ip, 80))
    client.send(bytes(request, 'utf-8'))
    print(request)


def get_host_and_path(url):
    parsed = urlparse(url)
    if parsed.path[0] == '/':
        return parsed.hostname, parsed.path[1:]
    else:
        return parsed.hostname, parsed.path


def format_request(host, path):
    return "GET /" + path + " HTTP/1.0\r\nHost: " + host + "\n\n"


def redirect_url(response):
    url_start = response.find('\r\nLocation: ')+12
    url_end = response.find('\r\n', url_start)
    return response[url_start:url_end]


redirects = 0
url = "https://www.airbnb.com/belong-anywhere"  # url = str(sys.argv)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while redirects != 10:
    send_request(url)
    data = client.recv(1024)
    response = ''
    while data:
        response += data.decode('utf-8')
        data = client.recv(1024)
    response_code = int(response[9:12])
    # make another request to fetch the corrected url and print a message to stderr explaining what happened
    if response_code == 301 or response_code == 302:
        url = redirect_url(response)
        sys.stderr.write('Redirected to ' + url)
        client.close()
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        redirects += 1
    # return a non-zero exit code, but also print the response body
    elif response_code >= 400:
        redirects = 10
        sys.stderr.write('error')
    # 200 OK response
    else:
        break
