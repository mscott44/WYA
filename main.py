import webapp2
import os
import jinja2
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

#LOGIN STUFF STARTS HERE
class ReturningUser(ndb.Model):
  first_name = ndb.StringProperty()
  last_name = ndb.StringProperty()

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        # If the user is logged in...
        if user:
            email_address = user.nickname()
            returning_user = ReturningUser.get_by_id(user.user_id())
            signout_link_html = '<a href="%s">sign out</a>' % (
                users.create_logout_url('/'))
            # If the user has previously been to our site, we greet them!
            if returning_user:
                self.response.write('''
                    Welcome %s %s (%s)! <br> %s <br>''' % (
                        returning_user.first_name,
                        returning_user.last_name,
                        email_address,
                        signout_link_html))
        # If the user hasn't been to our site, we ask them to sign up
            else:
                self.response.write('''
                    Welcome to our site, %s!  Please sign up! <br>
                    <form method="post" action="/">
                    <input type="text" name="first_name">
                    <input type="text" name="last_name">
                    <input type="submit">
                    </form><br> %s <br>
                    ''' % (email_address, signout_link_html))
        # Otherwise, the user isn't logged in!
        else:
            self.response.write('''
                Please log in to use our site! <br>
                <a href="%s">Sign in</a>''' % (
                    users.create_login_url('/')))

    def post(self):
        user = users.get_current_user()
        if not user:
            # You shouldn't be able to get here without being logged in
            self.error(500)
            return
        returning_user = ReturningUser(
            first_name=self.request.get('first_name'),
            last_name=self.request.get('last_name'),
            id=user.user_id())
        returning_user.put()
        self.response.write('Thanks for signing up, %s!' %
            returning_user.first_name)
#LOGIN STUFF ENDS HERE

class FeedHandler(webapp2.RequestHandler):
    def get(self):
        feed_template = jinja_env.get_template("templates/feed.html")
        self.response.write(feed_template.render())

class SettingsHandler(webapp2.RequestHandler):
    def get(self):
        settings_template = jinja_env.get_template("templates/settings.html")
        self.response.write(settings_template.render())

class ProfileHandler(webapp2.RequestHandler):
    def get(self):
        profile_template = jinja_env.get_template("templates/profile.html")
        self.response.write(profile_template.render())

class SearchHandler(webapp2.RequestHandler):
    def get(self):
        search_template = jinja_env.get_template("templates/search.html")
        self.response.write(search_template.render())

class NotficationsHandler(webapp2.RequestHandler):
    def get(self):
        notifications_template = jinja_env.get_template("templates/notifications.html")
        self.response.write(notifications_template.render())

app = webapp2.WSGIApplication ([
('/', LoginHandler),
('/feed', FeedHandler),
('/settings', SettingsHandler),
('/profile', ProfileHandler),
('/search', SearchHandler),
('/notifications' , NotficationsHandler)
], debug = True)
