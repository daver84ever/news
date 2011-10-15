from google.appengine.ext import db
import datetime

class News(db.Model):
    newsId = db.IntegerProperty(default=0)
    headline = db.StringProperty(default="Germans Invade!")
    content = db.StringProperty(default="Again...")
    createdAt = db.DateTimeProperty(auto_now_add=True)
