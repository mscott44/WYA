from google.appengine.ext import ndb

class User(ndb.Model):
    name = ndb.StringProperty(required=True)
    username = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    time = ndb.DateTimeProperty(auto_now_add=True)

class Post(ndb.Model):
    author = ndb.KeyProperty(User, required=True)
    content = ndb.StringProperty(required=True)
    time = ndb.DateTimeProperty(auto_now_add=True)

class Message(ndb.Model):
    content = ndb.StringProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
    sender = ndb.StringProperty()
    receiver = ndb.StringProperty()

    @classmethod
    def query_conversation(cls):
        return cls.query().order(-cls.timestamp)
