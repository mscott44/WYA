import webapp2
import os
import jinja2
import time
import webapp2
from models import Post, User
from content_management import populate_feed, logout_url, login_url
from google.appengine.api import users
from google.appengine.ext import ndb

jinja_current_directory = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

#LOGIN STUFF STARTS HERE
class ReturningUser(ndb.Model):
  first_name = ndb.StringProperty()
  last_name = ndb.StringProperty()

class LoginHandler(webapp2.RequestHandler):
    def get(self):

        new_user_template = jinja_current_directory.get_template("templates/new_user.html")
        google_login_template = jinja_current_directory.get_template("templates/login.html")

        # get Google users
        user = users.get_current_user()

        if user:
            # look for user in datastore
            existing_user = User.query().filter(User.email == user.email()).get()
            nickname = user.nickname()
            if not existing_user:
                # prompt new users to sign up
                fields = {
                    "nickname": nickname,
                    "logout_url": logout_url,
                }
                self.response.write(new_user_template.render(fields))
            else:
                # direct existing user to feed_template
                self.redirect('/feed')
        else:
            # ask user to sign in to google
            self.response.write(google_login_template.render({ "login_url": login_url }))

#LOGIN STUFF ENDS HERE

class CalendarHandler(webapp2.RequestHandler):
    def get(self):
        index_template = jinja_current_directory.get_template("templates/index.html")
        self.response.write(index_template.render())


class FeedHandler(webapp2.RequestHandler):
    def get(self):
        feed_template = jinja_current_directory.get_template("templates/feed.html")
        self.response.write(feed_template.render({ "sign_out": logout_url }))

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
        self.redirect('/feed')

class SettingsHandler(webapp2.RequestHandler):
    def get(self):
        settings_template = jinja_current_directory.get_template("templates/settings.html")
        self.response.write(settings_template.render({ "sign_out": logout_url }))

class ChatroomHandler(webapp2.RequestHandler):
    def get(self):
        settings_template = jinja_current_directory.get_template("templates/chatroom.html")
        self.response.write(settings_template.render({ "sign_out": logout_url}))

class ProfileHandler(webapp2.RequestHandler):
    def get(self):
        profile_template = jinja_current_directory.get_template("templates/profile.html")
        self.response.write(profile_template.render({ "sign_out": logout_url }))

class SearchHandler(webapp2.RequestHandler):
    def get(self):
        search_template = jinja_current_directory.get_template("templates/search.html")
        self.response.write(search_template.render({ "sign_out": logout_url }))

class NotficationsHandler(webapp2.RequestHandler):
    def get(self):
        notifications_template = jinja_current_directory.get_template("templates/notifications.html")
        self.response.write(notifications_template.render({ "sign_out": logout_url }))

app = webapp2.WSGIApplication ([
('/', LoginHandler),
('/chatroom', ChatroomHandler),
('/feed', FeedHandler),
('/settings', SettingsHandler),
('/profile', ProfileHandler),
('/search', SearchHandler),
('/notifications' , NotficationsHandler),
('/index', CalendarHandler)
], debug = True)
