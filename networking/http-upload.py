#!/usr/bin/python3

import random
import string
import argparse
from hashlib import md5
from pathlib import Path
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer


upload_form = '''
              <html>
                  <head>
                      <title>
                          Upload File
                      </title>
                  </head>
                  <body>
                      <div style="width: 26%; margin: auto; margin-top: 20%">
                          <form method='POST' enctype='multipart/form-data'>
                              <h2>Select a file and pump it up! :D</h2>
                              <input name='file' type='file'>
                              <br/>
                              <label for='secret'>Key:</label>
                              <input name='secret' type='password'>
                              <button style="float: right; margin-top: 10px;">Pump it up!</button>
                          </form>
                      </div>
                  </body>
              </html>
              '''.encode('utf-8')

upload_error = '''
               <html>\r
                   <head>\r
                       <title>\r
                           Error :(\r
                       </title>\r
                   </head>\r
                   <body>\r
                       <div style="width: 26%; margin: auto; margin-top: 20%">\r
                           <h2 style="margin: auto;">An error occured during the file upload :(</h2>\r
                       </div>\r
                   </body>\r
               </html>
               '''.encode('utf-8')

upload_success = '''
                 <html>\r
                     <head>\r
                         <title>\r
                             Success :D\r
                         </title>\r
                     </head>\r
                     <body>\r
                         <div style="width: 27%; margin: auto; margin-top: 20%">\r
                             <h2 style="margin: auto;">Your file was sucessfully uploaded :D</h2>\r
                         </div>\r
                     </body>\r
                 </html>
               '''.encode('utf-8')


class UploadError(Exception):
    '''
    Is raised when an error is encountered during the upload.
    '''


class UploadRequestHandler(BaseHTTPRequestHandler):
    '''
    Custom HTTPRequestHandler that allows file uploads.
    '''
    upload_key = ''
    upload_dir = Path('.')

    def _set_response(self) -> None:
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self) -> None:
        '''
        Return the HTML template for uploads
        '''
        self._set_response()
        self.wfile.write(upload_form)

    def do_POST(self) -> None:
        '''
        Process the upload.
        '''
        print("[+] Incoming upload!")

        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            border = post_data.split(b'\r\n')[0]

            if not border.startswith(b'----'):
                raise UploadError("Unexpected input format!")

            content_parts = post_data.split(border)
            content_parts = filter(lambda x: x.startswith(b'\r\nContent-Disposition'), content_parts)
            content = self.get_content(content_parts)

            file = content.get('file')
            secret = content.get('secret')

            if file is None:
                raise UploadError("Missing file parameter!")

            elif secret is None:
                raise UploadError("Missing secret parameter!")

            elif secret != UploadRequestHandler.upload_key:
                raise UploadError("Wrong upload key!")

            timestamp = datetime.now().strftime('%Y.%m.%d-%H%M%S%f')
            filename = UploadRequestHandler.upload_dir.joinpath(timestamp + '.dat')

            with open(filename, 'wb') as handle:
                handle.write(file)

            print("[+] File saved as: " + str(filename.absolute()))
            print("[+] MD5: " + md5(file).hexdigest())
            self.send_success()

        except UploadError as e:
            print('[-] Error: ' + str(e))
            self.send_error()

    def get_content(self, parts: list[bytes]) -> dict:
        '''
        Attempts to parse the file content and the upload key from incoming requests.
        '''
        content = {}

        for part in parts:

            key = None
            split = part.split(b'\r\n')

            for line in list(split):

                if not line:
                    split.remove(line)
                    continue

                elif line.startswith(b'Content-'):

                    if b'name="file"' in line:
                        key = 'file'

                    elif b'name="secret"' in line:
                        key = 'secret'

                    split.remove(line)
                    continue

                else:

                    if key is None:
                        raise UploadError()

                    content[key] = b'\r\n'.join(split[:-1])
                    break

        return content

    def send_error(self):
        '''
        Send a generic error message.
        '''
        self._set_response()
        self.wfile.write(upload_error)

    def send_success(self):
        '''
        Send a generic success message.
        '''
        self._set_response()
        self.wfile.write(upload_success)


def run(addr: str = '', port: int = 8000) -> None:
    '''
    Start the HTTP server.

    Parameters:
        addr        The ip address to start the server on
        port        The port to listen on

    Returns:
        None
    '''
    server_address = (addr, port)
    httpd = HTTPServer(server_address, UploadRequestHandler)

    print(f'[+] Started webserver on {str(addr)}:{str(port)}')
    print('[+]')

    try:
        httpd.serve_forever()

    except KeyboardInterrupt:
        pass

    httpd.server_close()
    print('[+] Webserver stopped')


parser = argparse.ArgumentParser(description='''HTTP Upload Server - Password protected file uploads''')
parser.add_argument('--key', default=None, help='secret key required for the upload')
parser.add_argument('--key-length', default=12, type=int, help='keylength for randomly generated keys (default: 12)')
parser.add_argument('--dir', default='.', help='upload directory where files are saved in')
parser.add_argument('--addr', default='0.0.0.0', help='ip address to start the server on')
parser.add_argument('--port', type=int, default=8000, help='port to start the server on (default: 8000)')
args = parser.parse_args()

if args.key:
    UploadRequestHandler.upload_key = args.key

else:
    pool = string.ascii_lowercase + string.ascii_uppercase + string.digits
    UploadRequestHandler.upload_key = ''.join(random.choices(pool, k=12)).encode()

    UploadRequestHandler.upload_dir = Path(args.dir)
    print('[+] Upload Key: ' + UploadRequestHandler.upload_key.decode())
    print('[+] Upload Dir: ' + str(UploadRequestHandler.upload_dir.absolute()))

    run(addr=args.addr, port=args.port)
