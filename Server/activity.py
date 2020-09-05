import datetime
import random

import flask_login
import json
import os.path


class Activity:
    # 指向聊天和论坛id?
    def __init__(self, act_id, name, info, duration, users, frequency):
        self.act_id = act_id
        self.name = name
        self.info = info
        self.users = users
        self.duration = duration
        self.frequency = frequency  # per day or week

    def __save(self):
        json.dump(self.__dict__,
                  open(f'data/activities/{self.act_id}.json', 'w', encoding='utf-8')
                  )
        return self

    @classmethod
    def new_activity(cls, name, info, durations, frequency):

        return cls(random.randint(0, 1000), name, info, durations, {}, frequency).__save()

    def add_user(self, username):
        if username in self.users.keys():
            print("You have already enrolled in this activity!")
        else:
            self.users[username] = [datetime.datetime.today() + datetime.timedelta(days=self.frequency), self.duration]
        return self.__save()

    def remove_user(self, username):
        self.users.pop(username)
        return self.__save()

    def clock_in(self, username):
        self.users[username][0] = datetime.datetime.today() + datetime.timedelta(days=self.frequency)
        if self.users[username][1] - 1 == 0:
            print("完成所有打卡！")
        else:
            self.users[username][1] -= 1
            print("完成打卡！")
        return self.__save()

    def check(self):
        for x in self.users:
            if datetime.datetime.today() > self.users[x][0]:
                print("错过打卡！")
                self.remove_user(x)
        return self.__save()


