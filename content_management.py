from google.appengine.api import users
from google.appengine.ext import ndb
from models import Post, User
from datetime import datetime

logout_url = users.create_logout_url('/')
login_url = users.create_login_url('/')

def format_posts(posts):
    return [(User.query().filter(User.key == post.author).get().username,
            post.content, post.time) for post in posts]

def populate_feed(current_user):
    feed_fields = {
        "sign_out": logout_url,
        "username": current_user.username,
        "user_name": current_user.name,
        "post_count": len(Post.query().filter(Post.author == current_user.key).fetch()),
        "user_count": len(User.query().fetch()),
        "posts": format_posts(Post.query().order(-Post.time).fetch(limit=30)),
        "users": User.query().order(User.username).fetch(),
    }
    return feed_fields
