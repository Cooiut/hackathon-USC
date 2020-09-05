import flask

webui_blueprint = flask.Blueprint('together_webui', __name__, url_prefix='/', static_folder='WebUI/assets',
                                  static_url_path='/assets/')


@webui_blueprint.route('/activity_list/')
def login_page():
    return flask.send_from_directory('WebUI', 'activity_list.css')


@webui_blueprint.route('/login/')
def login_page():
    return flask.send_from_directory('WebUI', 'login.html')
