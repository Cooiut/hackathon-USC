import datetime
import time
import random
import string

import flask_login
import json
import os.path


def rand_id():
    while True:
        res = ''.join(random.sample(string.ascii_lowercase + string.digits, 6))
        if not os.path.exists(f'data/activities/{res}.json'):
            break
    return res


class Activity:
    def __init__(self, act_id, name, info, duration, users, frequency, forum):
        self.act_id = act_id
        self.name = name
        self.info = info
        self.users = users  # {username: (当前参与状态 0/1, [总次数的0])}
        self.duration = duration  # 总天数
        self.frequency = frequency  # 每 ? 天
        self.start_time = datetime.datetime.now()  # 创建时间戳
        self.forum = forum  # [(user, time, emotion, text, image, likes)]

    def __save(self):
        json.dump(self.__dict__,
                  open(f'data/activities/{self.act_id}.json', 'w', encoding='utf-8')
                  )
        return self

    @classmethod
    def new_activity(cls, name, info, durations, frequency):
        return cls(rand_id(), name, info, durations, {}, frequency, []).__save()

    @classmethod
    def load_from_db(cls, id):
        try:
            d = json.load(open(f'data/activities/{id}.json', 'r', encoding='utf-8'))
            return cls(**d)
        except IOError:
            pass
        return None

    def user_join(self, user):
        self.users[user] = (1, [0 for i in range(self.duration / self.frequency)])
        return self.__save()

    # TODO 这东西先不做没时间
    # def user_leave(self, user):
    #     self.users.pop(user)
    #     self.left_users[user] = time.time()
    #     return self.__save()

    def checkin(self, user, emotion, text, image):
        # 生成时间戳更新self.users
        # 相关数据插入
        if (datetime.datetime.today() - self.start_time).days % self.frequency != 0:
            return "Error!"
        today = (datetime.datetime.today() - self.start_time).days % self.frequency
        self.users[user][1][today] = 1
        self.forum.insert(0, (user, datetime.datetime.today(), emotion, text, image, 0))
        return self.__save()

    def report(self, user):
        return self.start_time, self.users[user][1]


    def like(self, num_of_forum):
        # 第n个forum点赞 +1
        self.forum[num_of_forum][-1] += 1
        return self.__save()

    # 废弃: check expiration

    def get_detail(self, user):
        return [self.act_id, self.name, user in self.users, self.info, self.frequency, len(self.users), self.forum]

    def get_id(self):
        return self.act_id

if __name__ == '__main__':
    print(rand_id())
