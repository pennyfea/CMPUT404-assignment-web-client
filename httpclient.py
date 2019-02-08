#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
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

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

#***************************************************************************************
# Reason: Decoding information read by the socket... Changed it back to 'utf-8'. Worked on lab machine
# Availability: https://stackoverflow.com/questions/19699367/unicodedecodeerror-utf-8-codec-cant-decode-byte
# 
# Reason: Understanding & structuring request bodies
# Availability: https://stackoverflow.com/questions/978061/http-get-with-request-body
#
# Reason: Understanding GET & POST request bodies
# Availability: https://developer.mozilla.org/en-US/
#
# Reason: Sending a request body
# Availability: https://www.programcreek.com/python/example/93088/http.client.HTTPResponse
#***************************************************************************************

import sys
import socket
import re
# you may use urllib to encode data appropriately
from urllib.parse import urlparse, urlencode

def help():
    print("httpclient.py [GET/POST] [URL]\n")

# TODO: Print HTTPResponse object
class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

    # def __str__(self):
    #     return "Code: {}\nBody:\n{} \n\n".format(self.code, self.body)
    
class HTTPClient(object):

    def get_host_port_path(self,url):
    
        # URL: scheme://netloc/path;parameters?query#fragment
        URL = urlparse(url)
        host = URL.hostname
        port = URL.port
        path = URL.path
        # scheme = URL.scheme

        # if port is None  and scheme == 'http':
        #     port = 80
        # if port is None and scheme == 'https':
        #     port = 443

        if port is None:
            port = 80

        if len(path) == 0:
            path = "/"
        
        # Debugging purposes

        # print(host)
        # print(port)
        # print(path)
        # print(scheme)

        return host, port, path


    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        code = int(data.split()[1])
        return code

    def get_headers(self,data):
        headers = data.split('\r\n\r\n]')[0]
        return headers

    def get_body(self, data):
        body = data.split('\r\n\r\n')[1]
        return body
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):

        host, port, path = self.get_host_port_path(url)
        # Connect to the server socket
        self.connect(host, port)

        #Request body
        request =  ('GET %s HTTP/1.1\r\nConnection: close\r\nHost: %s \r\n\r\n'%(path, host))
        
        # Send the request body to the server 
        self.sendall(request)

        # Receive all data from the server socket
        data = self.recvall(self.socket)

        # Call close after you received data from the socket.
        self.close()

        headers = self.get_headers(data)
        code = self.get_code(data)
        body = self.get_body(data)

        print("Code: {}\nBody:\n{} \n\n".format(code, body))
       
        # print(code)
        # print(headers)
        # print(body)

        return HTTPResponse(code, body)

    def POST(self, url, args=None):

        parameter = ""

        if args != None:
            parameter = urlencode(args)
        
        # print("----------------------------------------------parameter", parameter)

        host, port, path = self.get_host_port_path(url)

        # Connect to the server socket
        self.connect(host, port)

        # Request body
        request = ('POST %s HTTP/1.1\r\nHost: %s\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: %s\r\n\r\n%s' % (path, host, str(len(parameter)), parameter))
        

        # Send the request body to the server 
        self.sendall(request)

        # Receive all data from the server socket
        data = self.recvall(self.socket)

        # Call close after you received data from the socket.
        self.close()

        


        headers = self.get_headers(data)
        code = self.get_code(data)
        body = self.get_body(data)
       
        # print(code)
        # print(headers)
        # print(body)
        print("Code: {}\nBody:\n{} \n\n".format(code, body))


        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()

    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
