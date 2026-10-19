from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        # Главная страница открывается по адресу /
        if self.path == "/":
            filename = "home.html"

        elif self.path in ("/home.html", "/home/"):
            filename = "home.html"

        elif self.path in ("/catalog.html", "/catalog/"):
            filename = "catalog.html"

        elif self.path in ("/category.html", "/category/"):
            filename = "category.html"

        elif self.path in ("/contacts.html", "/contacts/"):
            filename = "contacts.html"

        else:
            self.send_custom_error(404, "Страница не найдена")
            return

        try:
            with open(BASE_DIR / filename, "r", encoding="utf-8") as file:
                html = file.read()

        except OSError:
            self.send_custom_error(500, "Не удалось открыть HTML-файл")
            return

        self.send_response(200)
        self.send_header(
            "Content-Type",
            "text/html; charset=utf-8"
        )
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def do_POST(self):
        if self.path not in ("/contacts/", "/contacts.html"):
            self.send_error(404, "Страница не найдена")
            return

        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length).decode("utf-8")
        form_data = parse_qs(post_data)

        name = form_data.get("name", [""])[0]
        email = form_data.get("email", [""])[0]
        message = form_data.get("message", [""])[0]

        print("Получены данные из формы:")
        print(f"Имя: {name}")
        print(f"Почта: {email}")
        print(f"Сообщение: {message}")

        response_html = """
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <title>Сообщение отправлено</title>
        </head>
        <body>
            <h1>Сообщение отправлено!</h1>
            <p>Данные выведены в консоль сервера.</p>
            <a href="/contacts/">Вернуться к контактам</a>
        </body>
        </html>
        """

        self.send_response(200)
        self.send_header(
            "Content-Type",
            "text/html; charset=utf-8"
        )
        self.end_headers()
        self.wfile.write(response_html.encode("utf-8"))


server = HTTPServer(("localhost", 8000), MyHandler)

print("Сервер запущен: http://localhost:8000")
server.serve_forever()