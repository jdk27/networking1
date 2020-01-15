import socket
import sys
import re

def is_good_url(url_components):
    if not url_components:
        return False
     # can't be https
    if url_components.group(1) != 'http':
        sys.stderr.write('ERROR: https protocol')
        return False
     # must have a host domain
    if not url_components.group(4):
        return False
    return True


def send_request(url_components):
    host, path = get_host_and_path(url_components)
    remote_ip = socket.gethostbyname(host)
    request = format_request(host, path)
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


# http://airbedandbreakfast.com/
# https://www.airbnb.com/belong-anywhere
# http://insecure.stevetarzia.com/basic.html
# http://portquiz.net:8080/
# https://www.google.com:443/maps
# http://insecure.stevetarzia.com/redirect-hell
# http://cs.northwestern.edu/340

url = "http://cs.northwestern.edu/340"  # url = str(sys.argv)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
redirects = 0

while redirects != 10:
    # modified regex expression to handle port numbers
    # original expression:
    # ^((http[s]?|ftp):\/)?\/?([^:\/\s]+)((\/\w+)*\/)([\w\-\.]+[^#?\s]+)(.*)?(#[\w\-]+)?$
    # comes from https://stackoverflow.com/questions/27745/getting-parts-of-a-url-regex
    url_components = re.search(
        r'^(http|https)?(:\/\/)?(w{3}\.)?([\w\-\.]+)(:)?(\d+)?(\/)?([\w\-\.]+)?(\/)?', url)
    valid_url = is_good_url(url_components)
    if not valid_url:
        break

    # get the response
    send_request(url_components)
    data = client.recv(1024)
    response = ''
    while data:
        response += data.decode('utf-8')
        data = client.recv(1024)
    print('Here is the response: ', response)
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
        sys.stderr.write('error')
        break

    # 200 OK response
    else:
        break

client.close()

if redirects != 10 and valid_url and 200 == response_code or 400 <= response_code and -1 != response.find('Content-Type: text/html'):
    start = response.find('\r\n\r\n')+4
    print(response[start:-1])
if 200 == response_code:
    sys.exit(0)
else:
    sys.exit(1)
