from flask import Flask
from waitress import serve

app = Flask(__name__)


@app.route('/api/v1/hello-world-30')
def index():
    return "Hello World 30"


if __name__ == '__main__':
    serve(app)
    app.run()
