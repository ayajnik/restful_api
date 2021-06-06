## importing modules
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "hello world", 200

@app.route("/new_page")
def not_found():
    return "Page not found", 404


if __name__ == "__main__":
    app.run()