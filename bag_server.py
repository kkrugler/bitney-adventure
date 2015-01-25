import SocketServer
import BaseHTTPServer
import SimpleHTTPServer
import cgi
import bag_engine

class MyHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    global g_players

    template = open("bag.html").read()

    def get_username(self):
        global g_players

        # Strip off leading '/'
        username = self.path[1:]

        if not username in g_players:
            g_players.add(username)
            bag_engine.player_start(username)

        return username

    # Whenever we get a "get" request, we take the path as the player name. If there's no player name,
    # we return a generic msg.
    def do_GET(self):
        username = self.get_username()
        self.send_page(username)
        return

    def send_page(self, username):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        msgs = bag_engine.player_get_msgs(username)
        html_msg = ""
        for msg in msgs:
            html_msg += "<br />"
            html_msg += msg

        html_content = self.template.replace("bag_lines", html_msg)
        html_content = html_content.replace("bag_username", username)

        self.wfile.write(html_content)
        return

    def do_POST(self):
        username = self.get_username()

        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })

        #  extract the command from the form, send it to the game,
        # and then get the response.
        command = form.list[0].value
        bag_engine.player_add_msg(username, "> " + command)
        bag_engine.player_command(username, command)

        self.send_page(username)
        return

g_players = set()

PORT = 8000

handler = MyHTTPRequestHandler
httpd = SocketServer.TCPServer(("", PORT), handler)

print "serving at port", PORT
httpd.serve_forever()
