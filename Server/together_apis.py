import os

import flask
import flask_login
import json

from activity import Activity
from chatroom import Chatroom
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
    # todo
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


@apis_blueprint.route('/user/getnum/')
def user_getnum():
    try:
        return json.dumps({
            'status': 'ok',
            'total': len(os.listdir('data/users'))
        })
    except Exception as e:
        return json.dumps({
            'status': 'error',
            'message': str(e)
        })


@apis_blueprint.route('/activity/new/')
@flask_login.login_required
def new_activity():
    # 客户端提供name, info, durations，frequency
    # TODO  Activity.new_activity(.....)
    try:
        name = flask.request.form['name']
        info = flask.request.form['info']
        duration = flask.request.form['duration']
        frequency = flask.request.form['frequency']
        act = Activity.new_activity(name, info, duration, frequency)
        Chatroom.new_chat(act.get_id())
        return json.dumps({
            'status': 'ok',
        })
    except Exception as e:
        return json.dumps({
            'status': 'error',
            'message': str(e)
        })


@apis_blueprint.route('/user/enrolled_detail/')
@flask_login.login_required
def get_user_enrolled_detail():
    # 客户端不提供信息，username通过login manager调取，
    # 回报所有当前参加的活动
    # id, name, freq, total_people
    try:
        user = flask_login.current_user
        return json.dumps({
            'status': 'ok',
            'message': user.get_activities()
        })
    except Exception as e:
        return json.dumps({
            'status': 'error',
            'message': str(e)
        })


@apis_blueprint.route('/activity/detail/')
@flask_login.login_required
def get_activity_detail():
    # 客户端提供id
    # 服务端回报所有信息
    try:
        id = flask.request.args['id']
        user = flask_login.current_user
        act = Activity.load_from_db(id)
        return json.dumps({
            'status': 'ok',
            'message': act.get_detail(user.get_id())
        })
    except Exception as e:
        return json.dumps({
            'status': 'error',
            'message': str(e)
        })


@apis_blueprint.route('/activity/checkin/')
@flask_login.login_required
def checkin():
    # 客户端提供activity名，心情，文字，图片
    # 服务器端根据时间戳更新具体activity class
    # 回报成功与否
    try:
        id = flask.request.form['id']
        emo = flask.request.form['emo']
        text = flask.request.form['text']
        pic = flask.request.form['pic']
        user = flask_login.current_user.get_id()
        act = Activity.load_from_db(id)
        act.checkin(user, emo, text, pic)
        return json.dumps({
            'status': 'ok'
        })
    except Exception as e:
        return json.dumps({
            'status': 'error',
            'message': str(e)
        })

@apis_blueprint.route('/activity/like/')
@flask_login.login_required
def like():
    try:
        id = flask.request.form['id']
        n = flask.request.form['n']
        act = Activity.load_from_db(id)
        act.like(n)
        return json.dumps({
            'status': 'ok'
        })
    except Exception as e:
        return json.dumps({
            'status': 'error',
            'message': str(e)
        })


@apis_blueprint.route('/activity/recommend/')
@flask_login.login_required
def get_recommend():
    # 从所有的activity中随机挑三个，
    # 返回3个id, 客户端再请求detail
    try:
        recom = []
        for root, dirs, files in os.walk('data/activities'):
            for name in files:
                recom.append(name)
        a = range(3) if len(recom) >= 3 else range(len(recom))
        res = [recom[i] for i in a]
        return json.dumps({
            'status': 'ok',
            'ls': str(res)
        })
    except Exception as e:
        return json.dumps({
            'status': 'error',
            'message': str(e)
        })

@apis_blueprint.route('/chat/get/')
@flask_login.login_required
def get_chat():
    try:
        act_id = flask.request.form['id']
        starttime = flask.request.form['starttime']
        return json.dumps({
            'status': 'ok',
            'message': str(Chatroom.load_from_db(act_id).get_chat(starttime))
        })
    except Exception as e:
        return json.dumps({
            'status': 'error',
            'message': str(e)
        })


@apis_blueprint.route('/chat/post/')
@flask_login.login_required
def post_chat():
    try:
        user = flask_login.current_user.get_id()
        content = flask.request.form['content']
        act_id = flask.request.form['id']
        chat = Chatroom.load_from_db(act_id)
        chat.add_chat(user, content)
        return json.dumps({
            'status': 'ok'
        })
    except Exception as e:
        return json.dumps({
            'status': 'error',
            'message': str(e)
        })


if __name__ == '__main__':
    print(load_user('test'))
