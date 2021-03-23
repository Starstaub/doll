from app import db
from utils import NOW_TIME


class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    nb_char = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime, index=True, default=NOW_TIME)
    edit_time = db.Column(db.DateTime, index=True)
    title = db.Column(db.Text)

    def __repr__(self):
        return f"<Post {self.body}>"


class Link(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50))
    url = db.Column(db.String(255))
    description = db.Column(db.Text)
    artist = db.Column(db.String(50))
    author = db.Column(db.String(50))
    title = db.Column(db.String(100))
    year = db.Column(db.Integer)
    website = db.Column(db.String(100))
    isbn = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=NOW_TIME)

    def __repr__(self):
        return f"<Link {self.title}>"
