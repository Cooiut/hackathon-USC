import datetime
import time
import random
import string

import flask_login
import json
import os.path


def rand_id():
    while res := ''.join(random.sample(string.ascii_lowercase + string.digits, 6)):
        if not os.path.exists(f'data/activities/{res}.json'):
            break
    return res


class Activity:
    def __init__(self, act_id, name, info, duration, curr_users, auth_users, frequency):
        self.act_id = act_id
        self.name = name
        self.info = info
        self.curr_users = curr_users  # {username: last checkin, # of checkin}
        self.left_users = left_users  # {username: leave time}
        self.duration = duration
        self.frequency = frequency  # per day or week

    def __save(self):
        json.dump(self.__dict__,
                  open(f'data/activities/{self.act_id}.json', 'w', encoding='utf-8')
                  )
        return self

    @classmethod
    def new_activity(cls, name, info, durations, frequency):
        return cls(rand_id(), name, info, durations, {}, {}, frequency).__save()

    def user_join(self, user):
        self.curr_users[user] = [time.time(), 0]
        return self.__save()

    def user_leave(self, user):
        self.curr_users.pop(user)
        self.left_users[user] = time.time()
        return self.__save()

    def user_checkin(self):
        pass
        # TODO

    # TODO: check expiration


if __name__ == '__main__':
    print(rand_id())
