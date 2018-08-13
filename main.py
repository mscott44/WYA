import webapp2
import os
import jinja2

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class FeedHandler(webapp2.RequestHandler):
    def get(self):
        feed_template = jinja_env.get_template("templates/feed-page.html")
        self.response.write(feed_template.render())

class SettingsHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("templates/settings-page.html")
        self.response.write(template.render())

class ProfileHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("templates/profile-page.html")
        self.response.write(template.render())

class SearchHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_templates("templates/search-page.html")
        self.response.write(template.render())

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("templates/login-page.html")
        self.response.write(template.render())

class NotficationsHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("templates/notification-page.html")
        self.response.write (template.render())

class SettingsHandler(webapp2.RequestHandler):
    def get(self):
        settings_template = jinja_env.get_template("templates/settings-page.html")
        self.response.write(settings_template.render())

class ProfileHandler(webapp2.RequestHandler):
    def get(self):
        profile_template = jinja_env.get_template("templates/profile-page.html")
        self.response.write(profile_template.render())

class SearchHandler(webapp2.RequestHandler):
    def get(self):
        search_template = jinja_env.get_templates("templates/search-page.html")
        self.response.write(search_template.render())

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        login_template = jinja_env.get_template("templates/login-page.html")
        self.response.write(login_template.render())

class NotficationsHandler(webapp2.RequestHandler):
    def get(self):
        notifications_template = jinja_env.get_template("templates/notification-page.html")
        self.response.write(notifications_template.render())

app = webapp2.WSGIApplication ([
('/', FeedHandler),
('/settings', SettingsHandler),
('/profile', ProfileHandler),
('/search', SearchHandler),
('/login', LoginHandler),
('/notifications' , NotficationsHandler)
], debug = True)
