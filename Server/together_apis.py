import flask
import flask_login
import json

from user import User

apis_blueprint = flask.Blueprint('together_apis', __name__, url_prefix='/api/')
login_manager = flask_login.LoginManager()


@apis_blueprint.route('/')
def test_api():
    return json.dumps({'hello': 'world', 'from': 'TogetherAPI'})


@login_manager.user_loader
def load_user(user_id):
    return User.load_from_db(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    return json.dumps({
        'status': 'error',
        'message': 'unauthorized'
    })


@apis_blueprint.route('/login/', methods=['POST'])
def login():
    """
    {"username": str, "password": str}
    """
    try:
        username = flask.request.form['username']
        password = flask.request.form['password']
        user = User.load_from_db(username, password)
        if user:
            flask_login.login_user(user)
            return json.dumps({
                'status': 'ok'
            })
        else:
            return json.dumps({
                'status': 'error',
                'message': 'Wrong username or password'
            })
    except Exception as e:
        return json.dumps({
            'status': 'error',
            'message': str(e)
        })


@apis_blueprint.route('/logout/')
@flask_login.login_required
def logout():
    try:
        flask_login.logout_user()
        return json.dumps({
            'status': 'ok'
        })
    except Exception as e:
        return json.dumps({
            'status': 'error',
            'message': str(e)
        })


@apis_blueprint.route('/user/getinfo/')
@flask_login.login_required
def user_getinfo():
    try:
        user = flask_login.current_user
        print(user)
        return json.dumps({
            'status': 'ok',
            'username': user.get_id()
        })
    except Exception as e:
        return json.dumps({
            'status': 'error',
            'message': str(e)
        })


if __name__ == '__main__':
    print(load_user('test'))
