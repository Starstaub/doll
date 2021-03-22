from datetime import datetime

from app import db


class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    nb_char = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    edit_time = db.Column(db.DateTime, index=True)
    title = db.Column(db.Text)

    def __repr__(self):
        return f"<Post {self.body}>"
