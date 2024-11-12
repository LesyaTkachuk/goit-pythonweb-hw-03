from http.server import HTTPServer, BaseHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader
import urllib.parse
import mimetypes
import pathlib
import json
from datetime import datetime


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        page_url = urllib.parse.urlparse(self.path)

        match page_url.path:
            case "/":
                self.send_html_file("index.html")
            case "/message":
                self.send_html_file("message.html")
            case "/read":
                self.send_html_file(
                    filename="messages.html", template="messages_tmp.html"
                )
            case _:
                if pathlib.Path().joinpath(page_url.path[1:]).exists():
                    self.send_static()
                else:
                    self.send_html_file("error.html", 404)

    def do_POST(self):
        data = self.rfile.read(int(self.headers["Content-Length"]))
        print(data)
        data_parse = urllib.parse.unquote_plus(data.decode())
        print(data_parse)
        data_dict = {
            key: value for key, value in [el.split("=") for el in data_parse.split("&")]
        }
        print(data_dict)

        with open("./storage/data.json", "r") as fd:
            stored_messages = json.load(fd)
            if not stored_messages or not isinstance(stored_messages, object):
                stored_messages = {}
            time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            stored_messages[time_str] = data_dict
            print("stored_messages", stored_messages)

        with open("./storage/data.json", "w") as fd:
            json.dump(stored_messages, fd)

        self.send_response(302)
        self.send_header("Location", "/read")
        self.end_headers()

    def send_html_file(self, filename, status=200, template=None):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        if template:
            template_env = Environment(loader=FileSystemLoader("."))
            template_html = template_env.get_template(template)
            with open("./storage/data.json", "r") as fd:
                stored_messages = json.load(fd)
            output = template_html.render(messages=stored_messages.values())
            with open(filename, "w", encoding="utf-8") as fd:
                fd.write(output)
        with open(filename, "rb") as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", "text/plain")
        self.end_headers()

        with open(f".{self.path}", "rb") as file:
            self.wfile.write(file.read())


def run(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ("", 3000)
    http = server_class(server_address, handler_class)

    try:
        print("Server started at port 3000")
        http.serve_forever()
    except KeyboardInterrupt:
        print("\n Server stopped")
        http.server_close()
    except:
        print("Some error happened at an attempt to run the server...")


if __name__ == "__main__":
    run()
