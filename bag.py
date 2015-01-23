import SocketServer
import BaseHTTPServer
import SimpleHTTPServer

class MyHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    # Whenever we get a "get" request, we take the path as the player name. If there's no player name,
    # we return a generic msg.
    def do_GET(self):

        f = open("bag.html")
        self.template = f.read()
        f.close()

        # Strip off leading '/'
        username = self.path[1:]

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        html_content = self.template.replace("bag_lines", username)
        self.wfile.write(html_content)



PORT = 8000

handler = MyHTTPRequestHandler

httpd = SocketServer.TCPServer(("", PORT), handler)

print "serving at port", PORT
httpd.serve_forever()
