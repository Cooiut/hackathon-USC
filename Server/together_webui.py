import flask

webui_blueprint = flask.Blueprint('together_webui', __name__, url_prefix='/', static_folder='WebUI/assets',
                                  static_url_path='/assets/')


@webui_blueprint.route('/activity_list/')
def activity_page():
    return flask.send_from_directory('WebUI', 'activity_list.html')


@webui_blueprint.route('/schedule/')
def schedule_page():
    return flask.send_from_directory('WebUI', 'schedule.html')


@webui_blueprint.route('/login/')
def login_page():
    return flask.send_from_directory('WebUI', 'login.html')
