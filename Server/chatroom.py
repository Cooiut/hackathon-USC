import json
import os.path
import bisect
import time


class Chatroom:
    def __init__(self, chatid, contents):
        self.chatid = chatid
        self.contents = contents  # [time, user, content]

    def __save(self):
        json.dump(self.__dict__,
                  open(f'data/chatrooms/{self.chatid}.json', 'w', encoding='utf-8')
                  )
        return self

    @classmethod
    def load_from_db(cls, chatid):
        try:
            d = json.load(open(f'data/chatrooms/{chatid}.json', 'r', encoding='utf-8'))
            return cls(**d)
        except IOError:
            pass
        return None

    @classmethod
    def new_chat(cls, chatid):
        if not os.path.exists(f'data/chatrooms/{chatid}.json'):
            return cls(chatid, []).__save()
        return None

    def add_chat(self, user, content):
        self.contents.append([time.time(), user, content])
        return self.__save()

    def get_chat(self, starttime=None):
        if starttime is None:
            return self.contents
        else:
            return self.contents[
                   bisect.bisect_right(self.contents, [starttime, '', '']):
                   ]

