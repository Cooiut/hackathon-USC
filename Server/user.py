import flask_login
import json
import os.path


class User(flask_login.UserMixin):
    INIT_BALANCE = 100

    def __init__(self, username, pswd, balance, activities, avatar):
        self.username = username
        self.pswd = pswd
        self.balance = balance
        self.activities = activities  # [(name, freq, total people)]
        # 现在不考虑人数变动
        self.avatar = avatar

    def __save(self):
        json.dump(self.__dict__,
                  open(f'data/users/{self.username}.json', 'w', encoding='utf-8')
                  )
        return self

    @staticmethod
    def __parse_pswd(pswd):
        return pswd

    @classmethod
    def load_from_db(cls, username, pswd=None):
        try:
            d = json.load(open(f'data/users/{username}.json', 'r', encoding='utf-8'))
            if pswd is None or cls.__parse_pswd(pswd) == d['pswd']:
                return cls(**d)
        except IOError:
            pass
        return None

    @classmethod
    def new_user(cls, username, pswd):
        if not os.path.exists(f'data/users/{username}.json'):
            return cls(username, cls.__parse_pswd(pswd), cls.INIT_BALANCE, [], 'default_avatar ').__save()
        return None

    def get_id(self):
        return self.username

    def get_balance(self):
        return self.balance

    def get_avatar(self):
        return self.avatar

    def get_activities(self):
        return self.activities

    def join_activity(self, act_id):
        self.activities.append(act_id)
        return self.__save()


if __name__ == '__main__':
    print(User.load_from_db('abc', '1123').__dict__)
