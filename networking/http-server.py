#!/usr/bin/python3

import argparse
from termcolor import colored
from http.server import BaseHTTPRequestHandler, HTTPServer


y = lambda s: colored(s, 'yellow')
b = lambda s: colored(s, 'blue')


def print_headers(headers: list[str]) -> None:
    '''
    Takes a list of HTTP header lines and prints them in a formatted way.

    Parameters:
        headers         List of HTTP header lines

    Returns:
        None
    '''
    for header in headers:

        try:
            split = header.split(':')

            if len(split) < 2:
                raise ValueError(f'Invalid HTTP header: {header}')

            header_name = split[0]
            header_content = ':'.join(split[1:])
            print(f"[+]     {b(header_name)}: {y(header_content)}")

        except ValueError:
            print(f"[+]     {header}")


class Server(BaseHTTPRequestHandler):

    def _set_response(self) -> None:
        '''
        Server always returns 200 OK status code and a HTML based response.

        Parameters:
            None

        Returns:
            None
        '''
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Thanks for your message :)\n')

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

        headers = str(self.headers).splitlines()
        print_headers(headers)

        self._set_response()

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

        headers = str(self.headers).splitlines()
        print_headers(headers)

        try:
            print(f"[+]     {y(post_data.decode())}", end="\n")
        except UnicodeDecodeError:
            print(f"[+]     {post_data}", end="\n")

        self._set_response()
        print("[+]")

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
