from flask import Flask
from waitress import serve
from User import user
from Medicine import medicine
from Pharmacy import order

app = Flask(__name__)

app.register_blueprint(user)
app.register_blueprint(medicine)
app.register_blueprint(order)


@app.route('/api/v1/hello-world-30')
def index():
    return "Hello World 30"


if __name__ == '__main__':
    serve(app)
    app.run()
