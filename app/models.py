from app import db
from utils import NOW_TIME


class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    nb_char = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime, index=True, default=NOW_TIME)
    edit_time = db.Column(db.DateTime, index=True)
    title = db.Column(db.String(100))

    def __repr__(self):
        return f"<Post {self.body}>"


class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    status = db.Column(db.String(50))
    created = db.Column(db.DateTime, index=True)
    modified = db.Column(db.DateTime, index=True)
    category = db.Column(db.String(15))
    description = db.Column(db.Text)

    def __repr__(self):
        return f"<Task {self.title}>"


class Wish(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(15))
    url = db.Column(db.Text)
    description = db.Column(db.Text)
    artist = db.Column(db.String(50))
    author = db.Column(db.String(50))
    size = db.Column(db.String(10))
    color = db.Column(db.String(20))
    title = db.Column(db.String(100))
    year = db.Column(db.Integer)
    website = db.Column(db.String(50))
    isbn = db.Column(db.Integer)
    picture = db.Column(db.Text)
    price = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, index=True)

    def __repr__(self):
        return f"<Wish {self.title}>"
