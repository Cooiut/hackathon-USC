import flask
import flask_login
import json

apis_blueprint = flask.Blueprint('together_apis', __name__, url_prefix='/api/')
login_manager = flask_login.LoginManager()


@apis_blueprint.record_once
def reg_login_mgr(state):
    login_manager.init_app(state.app)


@apis_blueprint.route('/')
def test_api():
    return json.dumps({'hello': 'world', 'from': 'test'})


if __name__ == '__main__':
    pass
