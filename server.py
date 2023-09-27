#  coding: utf-8 
import socketserver
import os
# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#   
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):

        self.data = self.request.recv(1024).strip()

        # get the data parts
        data_parts = self.data.decode().split(" ")
        command = data_parts[0]
        path = data_parts[1]
        print("Got a request of: %s\n" % self.data)

        # check what command was sent
        if command == "GET":
            self.handle_command(path)
        else:
            self.handle_405()

    def handle_command(self, path):

        version = "HTTP/1.1"
        content_type = ""

        if path.endswith(".html"):
            file_path = "./www" + path
            try:
                file = open(file_path, "r")
                file_contents = file.read()
                file.close()
            except:
                self.handle_404()
                return

            content_type = "text/html"
            self.handle_200(content_type, file_contents)

        elif path.endswith(".css"):
            file_path = "./www" + path
            try:
                file = open(file_path, "r")
                file_contents = file.read()
                file.close()
            except:
                self.handle_404()
                return

            content_type = "text/css"
            self.handle_200(content_type, file_contents)

        elif path.endswith("/"):
            file_path = "./www" + path + "index.html"
            try:
                file = open(file_path, "r")
                file_contents = file.read()
                file.close()
            except:
                self.handle_404()
                return

            content_type = "text/html"
            self.handle_200(content_type, file_contents)

        elif not path.endswith("/"):
            redirected_path = path + "/"
            deep_path = "./www" + path + "/"
            if os.path.isdir(redirected_path):
                self.handle_301(redirected_path)
            elif os.path.isdir(deep_path):
                self.handle_301(redirected_path)
            else:
                self.handle_404()
                return

        else:
            self.handle_404()

    def handle_301(self, redirected_path):

        print("handle301\n")

        response = "HTTP/1.1 301 Moved Permanently\r\nLocation: " + redirected_path + "\r\n"
        self.request.sendall(bytearray(response, 'utf-8'))

    def handle_200(self, content_type, content):
        
        print("handle200\n")

        response = "HTTP/1.1 200 OK\nContent-Type: " + content_type + "\r\n" + content
        self.request.sendall(bytearray(response, 'utf-8'))

    def handle_404(self):

        print("handle404\n")

        self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n",'utf-8'))

    def handle_405(self):

        print("handle405\n")

        self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\r\n",'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
