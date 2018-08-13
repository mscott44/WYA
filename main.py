import webapp2
import os
import jinja2

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("Where You At?")

class SettingsHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("templates/settings-page.html")
        self.response.write("")

class ProfileHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("templates/profile-page.html")
        self.response.write("")

class SearchHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_templates("templates/search-page.html")
        self.response.write("")

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("templates/login-page.html")
        self.response.write("")

class NotficationsHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("templates/notification-page.html")
        self.response.write("")

app = webapp2.WSGIApplication ([
('/', MainHandler),
('/settings', SettingsHandler),
('/profile', ProfileHandler),
('/search', SearchHandler),
('/login', LoginHandler),
('/notifications' , NotficationsHandler)
], debug = True)
