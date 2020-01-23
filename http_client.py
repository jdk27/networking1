import socket
import sys
import re


def is_good_url(url_components):
    if not url_components:
        return False
     # can't be https
    if url_components.group(1) != 'http':
        print('ERROR: https protocol', file=sys.stderr)
        return False
     # must have a host domain
    if not url_components.group(4):
        return False
    return True


def send_request(url_components, client):
    host, path = get_host_and_path(url_components)
    remote_ip = socket.gethostbyname(host)
    request = format_request(host, path)
    if url_components.group(6):
        client.connect((remote_ip, int(url_components.group(6))))
    else:
        client.connect((remote_ip, 80))

    client.send(bytes(request, 'utf-8'))


def get_host_and_path(url_components):
    host = url_components.group(4)
    path = url_components.group(8)
    if not path:
        return host, ''
    else:
        return host, path


def format_request(host, path):
    return "GET /" + path + " HTTP/1.0\r\nHost: " + host + "\r\n\r\n"


def redirect_url(response):
    url_start = response.find('\r\nLocation: ')+12
    url_end = response.find('\r\n', url_start)
    return response[url_start:url_end]


def has_valid_content_type(response):
    start = response.find('Content-Type: ')
    if start == -1:
        return False
    start += len('Content-Type: ')
    end = start+len('text/html')
    content_type = response[start:end]
    return content_type == 'text/html'


def print_body(response, client):
    length_start = response.find('Content-Length: ')
    html = response[response.find('\r\n\r\n')+len('\r\n\r\n'):]
    if -1 != length_start:
        length_start += len('Content-Length: ')
        length_end = response.find('\r\n', length_start)
        total_length = int(response[length_start:length_end])
        while len(html) < total_length:
            response = str(client.recv(1024), 'utf-8')
            html += response
    else:
        while response:
            response = str(client.recv(1024), 'utf-8')
            html += response
    print(html)

# http://airbedandbreakfast.com/
# https://www.airbnb.com/belong-anywhere
# http://insecure.stevetarzia.com/basic.html
# http://portquiz.net:8080/
# https://www.google.com:443/maps
# http://insecure.stevetarzia.com/redirect-hell
# http://cs.northwestern.edu/340


url = str(sys.argv[1])

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
redirects = 0
response_code = 0

while redirects != 10:
    # modified regex expression to handle port numbers
    # original expression:
    # ^((http[s]?|ftp):\/)?\/?([^:\/\s]+)((\/\w+)*\/)([\w\-\.]+[^#?\s]+)(.*)?(#[\w\-]+)?$
    # comes from https://stackoverflow.com/questions/27745/getting-parts-of-a-url-regex
    url_components = re.search(
        r'^(https|http)?(:\/\/)?(w{3}\.)?([\w\-\.]+)(:)?(\d+)?(\/)?([\w\-\.]+)?(\/)?', url)
    valid_url = is_good_url(url_components)
    if not valid_url:
        break

    # get the response
    send_request(url_components, client)
    response = str(client.recv(1024), 'utf-8')
    response_code = int(response[9:12])

    # make another request to fetch the corrected url and print a message to stderr explaining what happened
    if response_code == 301 or response_code == 302:
        url = redirect_url(response)
        print('Redirected to ' + url, file=sys.stderr)
        client.close()
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        redirects += 1

    # return a non-zero exit code, but also print the response body
    elif response_code >= 400:
        if has_valid_content_type(response):
            print_body(response, client)
        break

    # 200 OK response
    else:
        if has_valid_content_type(response):
            print_body(response, client)
        else:
            response_code = -1
        break

client.close()

if 200 == response_code:
    sys.exit(0)
else:
    sys.exit(1)
