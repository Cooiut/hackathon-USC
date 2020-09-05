import json
import os
import time


class Post:
    def __init__(self, post_id, t, user, mood, text, pic, like, comments):
        self.post_id = post_id
        self.time = t
        self.user = user
        self.mood = mood
        self.text = text
        self.pic = pic
        self.like = like
        self.comments = comments

    @classmethod
    def new_post(cls, user, mood, text, pic):
        return cls("ID", time.time(), user, mood, text, pic, 0, [])


class Comment:
    def __init__(self, com_id, post_id, t, user, text):
        self.com_id = com_id
        self.post_id = post_id
        self.time = t
        self.user = user
        self.text = text

    @classmethod
    def new_comment(cls, post_id, user, text):
        return cls("ID", post_id, time.time(), user, text)


class Forum:

    def __init__(self, forum_id, contents):
        self.id = forum_id
        self.contents = contents  # [id, time, user, mood, text, pic, like, comments]
        # 写评论时需要id来区分评论哪个帖子

    def __save(self):
        json.dump(self.__dict__,
                  open(f'data/forums/{self.id}.json', 'w', encoding='utf-8')
                  )
        return self

    @classmethod
    def load_from_db(cls, forum_id):
        try:
            d = json.load(open(f'data/forums/{forum_id}.json', 'r', encoding='utf-8'))
            return cls(**d)
        except IOError:
            pass
        return None

    @classmethod
    def new_forum(cls, forum_id):
        if not os.path.exists(f'data/forums/{forum_id}.json'):
            return cls(forum_id, []).__save()
        return None

    def add_post(self, user, content, mood, pic):
        self.contents.append(Post.new_post(user, mood, content, pic))
        return self.__save()

    def add_comment(self, post_id, user, content):
        for x in self.contents:
            if x[0] == post_id:
                x[-1].append(Comment.new_comment(post_id, user, content))
        return self.__save()

    def get_forum(self):
        return  # todo
