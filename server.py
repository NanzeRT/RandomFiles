from http.server import BaseHTTPRequestHandler, HTTPServer
import os


class S(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            with open('.' + self.path, 'rb') as file:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(file.read())
        except:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        with open('.' + self.path, 'wb') as file:
            file.write(post_data)
        self.send_response(202)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(f'{self.path[1:]} => {post_data.decode("utf-8")}'.encode('utf-8'))
    
    def do_DELETE(self):
        try:
            with open('.' + self.path, 'r') as file:
                self.send_response(204)
                self.send_header('Content-type', 'text/html')
                self.send_header('X-Value', file.read())
            os.remove('.' + self.path)
        except:
            self.send_response(404)
        self.end_headers()
        
    def do_GIVE(self):
        self.send_response(255, 'Gift Accepted')
        self.send_header('Content-type', 'text/html')
        print(self.headers.get("Gift"))
        self.end_headers()
        self.wfile.write(f'Thanks for your {self.headers.get("Gift")}'.encode('UTF-8'))


def run(server_class=HTTPServer, handler_class=S, port=2020):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == '__main__':
    run()
