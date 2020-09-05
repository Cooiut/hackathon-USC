import flask

webui_blueprint = flask.Blueprint('together_webui', __name__, url_prefix='/', static_folder='WebUI/assets',
                                  static_url_path='/assets/')


@webui_blueprint.route('/')
def login_page():
    return flask.send_from_directory('WebUI', 'login.html')