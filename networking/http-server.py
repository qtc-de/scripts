#!/usr/bin/python3

import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer


y = lambda s: '\033[33m' + s + '\033[0m'
b = lambda s: '\033[34m' + s + '\033[0m'


def parse_headers(headers: list[str]) -> dict[str, str]:
    '''
    Takes a list of HTTP header lines and returns a corresponding
    HTTP header dictionary.

    Parameters:
        headers         List of HTTP header lines

    Returns:
        dictionary containing HTTP headers
    '''
    header_dict = {}

    for header in headers:

        key, value = header.split(':', 1)

        if len(split) == 2:
            header_dict[key] = value


def print_headers(headers: dict[str, str]) -> None:
    '''
    Takes a HTTP header dict and prints it in a formatted way.

    Parameters:
        headers         HTTP header dict

    Returns:
        None
    '''
    for key, value in headers.items():
        print(f'[+]     {b(key)}: {y(value)}')


class Server(BaseHTTPRequestHandler):

    def _set_response(self, headers: dict[str, str]) -> None:
        '''
        Server always returns 200 OK status code and a HTML based response.

        Parameters:
            headers           optional header dict for CORS access

        Returns:
            None
        '''
        self.send_response(200)
        self.send_header('Content-type', 'text/html')

        if headers:
            self.set_cors_headers(headers)

        self.end_headers()
        self.wfile.write(b'Thanks for your message :)\n')

    def set_cors_headers(self, headers: dict[str, str]) -> None:
        '''
        Set Access-Control-Allow headers to allow CORS requests.

        Parameters:
            headers           header dict for CORS access

        Returns:
            None
        '''
        if 'Origin' in headers:
            self.send_header('Access-Control-Allow-Origin', headers['Origin'])

        else:
            self.send_header('Access-Control-Allow-Origin', '*')

        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS')

        if 'Access-Control-Request-Headers' in headers:
            self.send_header('Access-Control-Allow-Headers', headers['Access-Control-Request-Headers'])
        else:
            self.send_header('Access-Control-Allow-Headers', 'content-type,private-token,user-agent')

    def do_GET(self) -> None:
        '''
        For incoming GET requests, the server prints their associated path
        and the contained HTTP headers in a formatted way.

        Parameters:
            None

        Returns:
            None
        '''
        print(f"[+] {b('Obtained')} {y('GET')} {b('Request')}.")
        print(f"[+]     {b('Path')}: {y(str(self.path))}")

        headers = parse_headers(str(self.headers).splitlines())
        print_headers(headers)

        self._set_response(headers)

    def do_POST(self) -> None:
        '''
        For incoming POST requests, the server prints their associated path
        and the contained HTTP headers in a formatted way.

        Parameters:
            None

        Returns:
            None
        '''
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        print(f"[+] {b('Obtained')} {y('POST')} {b('Request')}.")
        print(f"[+]     {b('Path')}: {y(str(self.path))}")

        headers = parse_headers(str(self.headers).splitlines())
        print_headers(headers)

        try:
            print(f"[+]     {y(post_data.decode())}", end="\n")

        except UnicodeDecodeError:
            print(f"[+]     {post_data}", end="\n")

        self._set_response(headers)
        print("[+]")

    def do_OPTIONS(self) -> None:
        '''
        For incoming OPTIONS requests, the server prints their associated path
        and the contained HTTP headers. Afterwards it responds with permissive
        CORS headers.

        Parameters:
            None

        Returns:
            None
        '''
        print(f"[+] {b('Obtained')} {y('OPTIONS')} {b('Request')}.")
        print(f"[+]     {b('Path')}: {y(str(self.path))}")

        headers = parse_headers(str(self.headers).splitlines())
        print_headers(headers)

        self.send_response(200, 'OK')
        self.set_cors_headers(headers)
        self.end_headers()

    def log_message(self, format, *args) -> None:
        '''
        Disable the default logging of the HTTP server.
        '''
        return


def run(port: int = 8000) -> None:
    '''
    Start the HTTP server.

    Parameters:
        port            The port number to listen on

    Returns:
        None
    '''
    server_address = ('', port)
    httpd = HTTPServer(server_address, Server)
    print(f"[+] {b('Started webserver on port')} {y(str(port))}.")
    print(f'[+]')

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    print(f"[+] {b('Webserver stopped')}")


parser = argparse.ArgumentParser(description='''Simple HTTP server for monitoring incoming requests''')
parser.add_argument('port', nargs='?', type=int, default=8000, help='the port to listen on (default: 8000)')
args = parser.parse_args()

run(args.port)
