import flask_login
import json
import os.path


class User(flask_login.UserMixin):
    INIT_BALANCE = 100

    def __init__(self, username, pswd, balance, activities):
        self.username = username
        self.pswd = pswd
        self.balance = balance
        self.activities = activities

    def __save(self):
        json.dump(self.__dict__,
                  open(f'data/users/{self.username}.json', 'w', encoding='utf-8')
                  )
        return self

    @staticmethod
    def __parse_pswd(pswd):
        return pswd

    @classmethod
    def load_from_db(cls, username, pswd):
        try:
            d = json.load(open(f'data/users/{username}.json', 'r', encoding='utf-8'))
            if cls.__parse_pswd(pswd) == d['pswd']:
                return cls(**d)
        except IOError:
            pass
        return None

    @classmethod
    def new_user(cls, username, pswd):
        if not os.path.exists(f'data/users/{username}.json'):
            return cls(username, cls.__parse_pswd(pswd), cls.INIT_BALANCE, []).__save()
        return None


if __name__ == '__main__':
    print(User.load_from_db('abc', '1123').__dict__)
