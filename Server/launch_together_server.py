import flask

from together_apis import apis_blueprint, login_manager

HOST = 'localhost'
PORT = 8001

app = flask.Flask(__name__)
login_manager.init_app(app)

app.secret_key = 'mdzz'
app.register_blueprint(apis_blueprint)

if __name__ == '__main__':
    app.run(HOST, PORT)
