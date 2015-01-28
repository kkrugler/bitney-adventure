import SocketServer
import BaseHTTPServer
import SimpleHTTPServer
import cgi
import string
import bag_engine

class MyHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    global g_players

    # This contains the template HTML content for the initial login page.
    login = open("bag_login.html").read()

    # This contains the HTML content for the actual interactive game.
    template = open("bag.html").read()

    def get_username(self):
        global g_players

        # Strip off leading '/' in path
        username = self.path[1:]
        self.add_player(username)
        return username

    # Add player <username> if they're not already playing the game.
    def add_player(self, username):
        if not username in g_players:
            g_players.add(username)
            bag_engine.player_start(username)

    # Whenever we get a "get" request, we take the path as the player name. If there's no player name,
    # we return a generic msg.
    def do_GET(self):
        username = self.get_username()
        if username == "":
            self.send_login()
        else:
            self.send_page(username)

        return

    def send_login(self, msg=""):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        html_content = self.login.replace("bag_msg", msg)

        self.wfile.write(html_content)
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

    def get_form_input(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                    'CONTENT_TYPE':self.headers['Content-Type'],
                     })

        return form.list[0].value

    def is_valid_username(self, username):
        length = len(username)
        if (length < 3) or (length > 16):
            return False

        for char in username:
            if not char in string.ascii_letters:
                return False

        return True

    def do_POST(self):
        if self.path == "/bag_login":
            username = self.get_form_input()
            if not self.is_valid_username(username):
                self.send_login("I'm sorry, but \"%s\" is not a valid username" % username)
                return
            else:
                self.add_player(username)
                self.send_page(username)
        else:
            username = self.get_username()
            command = self.get_form_input()
            bag_engine.player_add_msg(username, "> " + command)
            bag_engine.player_command(username, command)
            self.send_page(username)

g_players = set()

PORT = 8000

handler = MyHTTPRequestHandler
httpd = SocketServer.TCPServer(("", PORT), handler)

print "serving at port", PORT
httpd.serve_forever()
