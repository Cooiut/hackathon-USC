import flask
from together_apis import apis_blueprint

HOST = 'localhost'
PORT = 8001

app = flask.Flask(__name__)
app.register_blueprint(apis_blueprint)

if __name__ == '__main__':
    app.run(HOST, PORT)
