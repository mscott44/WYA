import datetime
import jinja2
import json
import os
import webapp2
import time

from models import Post, User, Message
from content_management import populate_feed, logout_url, login_url
from google.appengine.api import users
from google.appengine.ext import ndb

jinja_current_directory = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class ReturningUser(ndb.Model):
   first_name = ndb.StringProperty()
   last_name = ndb.StringProperty()

class LoginHandler(webapp2.RequestHandler):
     def get(self):

         new_user_template = jinja_current_directory.get_template("templates/new_user.html")
         google_login_template = jinja_current_directory.get_template("templates/login.html")

       #get Google users
         user = users.get_current_user()

         if user:
            # look for user in datastore
            user_in_database = User.query().filter(User.email == user.email()).get()
            nickname = user.nickname()
            if not user_in_database:
                # prompt new users to sign up
                fields = {
                    "nickname": nickname,
                    "logout_url": logout_url,
                }
                self.response.write(new_user_template.render(fields))
            else:
                # direct existing user to profile_template
               self.redirect('/profile')
         else:
           # ask user to sign in to google
           self.response.write(google_login_template.render({ "login_url": login_url }))

 #LOGIN STUFF ENDS HERE
class CalendarHandler(webapp2.RequestHandler):
    def get(self):
        index_template = jinja_current_directory.get_template("templates/index.html")
        self.response.write(index_template.render())

class ProfileHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        current_user = User.query().filter(User.email == user.email()).get()
        fields = {
            "name": current_user.name,
            "username": current_user.username,
            "sign_out": logout_url,
            "email" : current_user.email,
            "users": User.query().fetch(),
            "user_count": len(User.query().fetch())
        }
        profile_template = jinja_current_directory.get_template("templates/profile.html")
        self.response.write(profile_template.render(fields))
    def post(self):
         user = users.get_current_user()
         if user is None:
             self.redirect('/')
             return # lol idk if this is ok?? it works I guess
         current_user = User.query().filter(User.email == user.email()).get()
         if not current_user:
             # upon new user form submission, create new user and store in datastore
             new_user_entry = User(
                 name = self.request.get("name"),
                 username = self.request.get("username"),
                 email = user.email(),
             )
             new_user_entry.put()
             current_user = new_user_entry
         else:
             # if not a new user, existing user submitted a post from feed
             new_post = Post(author= current_user.key, content= self.request.get("user_post"))
             new_post.put()
         time.sleep(.2)
         self.redirect('/profile')

class ChatroomHandler(webapp2.RequestHandler):
     def get(self):
         user = users.get_current_user()
         current_user = User.query().filter(User.email == user.email()).get()
         all_users = User.query().fetch()
         fields = {
            "username": current_user.username,
            "name": current_user.name,
            "sign_out": logout_url,
            "email" : current_user.email,
            "all_users" : all_users
          }
         template = jinja_current_directory.get_template("templates/chatroom.html")
         self.response.write(template.render(fields))

class FeedHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        current_user = User.query().filter(User.email == user.email()).get()
        fields = {
            "name": current_user.name,
            "username": current_user.username,
            "sign_out": logout_url,
            "email" : current_user.email,
            "users": User.query().fetch(),
            "user_count": len(User.query().fetch())
        }
        feed_template = jinja_current_directory.get_template("templates/feed.html")
        self.response.write(feed_template.render(fields))

class FriendprofileHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        current_user = User.query().filter(User.email == user.email()).get()
        fields = {
            "name": current_user.name,
            "username": current_user.username,
            "sign_out": logout_url,
            "email" : current_user.email,
            "users": User.query().fetch(),
            "user_count": len(User.query().fetch()),
            "friend": User.query().filter(User.username == self.request.get("friend")).get()
        }
        friendprofile_template = jinja_current_directory.get_template("templates/friendprofile.html")
        self.response.write(friendprofile_template.render(fields))

class SearchHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        current_user = User.query().filter(User.email == user.email()).get()
        fields = {
            "name": current_user.name,
            "username": current_user.username,
            "sign_out": logout_url,
            "email" : current_user.email,
            "users": User.query().fetch(),
            "user_count": len(User.query().fetch())
        }
        search_template = jinja_current_directory.get_template("templates/search.html")
        self.response.write(search_template.render(fields))

class ExploreHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        current_user = User.query().filter(User.email == user.email()).get()
        fields = {
            "name": current_user.name,
            "username": current_user.username,
            "sign_out": logout_url,
            "email" : current_user.email,
            "users": User.query().fetch(),
            "user_count": len(User.query().fetch())
        }
        explore_template = jinja_current_directory.get_template("templates/explore.html")
        self.response.write(explore_template.render(fields))

class ChatService(webapp2.RequestHandler):
    def get(self):
        key = self.getKey(self.request);
        me = self.request.get('me')
        other = self.request.get('other');
        ancestor_key = ndb.Key('Messages', key)
        messages = Message.query_conversation().filter(
            Message.sender == me,
            Message.receiver == other).fetch()
        messages += Message.query_conversation().filter(
            Message.sender == other,
            Message.receiver == me).fetch()
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(
            json.dumps([self.to_serializable(m) for m in messages]))

    def post(self):
        key = self.getKey(self.request);
        content = self.request.get('content');
        sender = self.request.get('from')
        receiver = self.request.get('to');
        message = Message(parent=ndb.Key("Messages", key), content=content, receiver=receiver, sender=sender)
        message.put()
        time.sleep(0.3)

    def getKey(self, request):
        from_user = self.request.get('from');
        to_user = self.request.get('to');
        key_values = [from_user, to_user]
        key_values.sort()
        return key_values[0] + '_' + key_values[1];

    def to_serializable(self, data):
        """Build a new dict so that the data can be JSON serializable"""
        result = data.to_dict()
        record = {}

        for key in result.iterkeys():
            if isinstance(result[key], datetime.datetime):
                record[key] = result[key].isoformat()
                continue
            record[key] = result[key]

        record['key'] = data.key.id()
        return record

app = webapp2.WSGIApplication ([
('/chat', ChatService),
('/', LoginHandler),
('/chatroom', ChatroomHandler),
('/feed', FeedHandler),
('/profile', ProfileHandler),
('/friendprofile', FriendprofileHandler),
('/search', SearchHandler),
('/explore' , ExploreHandler),
('/index', CalendarHandler)
], debug = True)
