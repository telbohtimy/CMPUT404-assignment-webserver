import SocketServer
# coding: utf-8

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
import os

version="HTTP/1.1"
endLine="\r\n"
class MyWebServer(SocketServer.BaseRequestHandler):
    def error404(self):
        error=version+" 404 Not Found"+endLine
        error=error+"Content-Type:text/html"+endLine+endLine
        error=error+"<html><body>\n"
        error=error+"<h1>Error 404</h1>\n"
        error=error+"File does not exist\n</body></html>"
        return error
    def requestOK(self,fileType,contents):
        if fileType=="html" or fileType=="css":
            codeOK=version+" 200 OK"+endLine
            codeOK=codeOK+"Content-Type: text/"+fileType+endLine+endLine
            codeOK=codeOK+contents
        else:
            codeOK= version+" 200 OK"+endLine+endLine
            codeOK=codeOK+contents
            #codeOK=self.error404()
        return codeOK
    def redirect(self,URL):
        redirect=version+" 301 Moved Permanently"+endLine
        redirect=redirect+"Content-Type: text/html"+endLine+endLine
        redirect=redirect+"<html><body>\n"
        redirect=redirect+"<h1>Moved</h1>\n"
        redirect=redirect+"<p>This page has been moved: <a href="+URL+"> Redirect me</a></p>"
        return redirect
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        
        self.lineSplit=self.data.split("\n")
        self.wordSplit=self.lineSplit[0].split(" ")
        if self.wordSplit[1][-1]=="/":
           self.wordSplit[1]=self.wordSplit[1]+"index.html"
        findType=self.wordSplit[1].split(".")
        fileType=findType[-1]
        try:
            openFile=open(os.getcwd()+"/www"+self.wordSplit[1],"r")
            contents=openFile.read() 
            openFile.close()
            if "/../" in self.wordSplit[1]:
                response=self.error404()
            else:
                response= self.requestOK(fileType,contents)
        except:
                try:
                    openFile1=open(os.getcwd()+"/www/deep/"+self.wordSplit[1],"r")
                    contents=openFile1.read() 
                    openFile1.close()
                    if "/../" in self.wordSplit[1]:
                        response=self.error404()
                    else:
                        response= self.requestOK(fileType,contents)
                except:
                    if self.wordSplit[1]=="/deep":
                        response=self.redirect("deep/index.html")
                    else:
                        response=self.error404()
        self.request.sendall(response)

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
