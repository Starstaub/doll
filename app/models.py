from datetime import datetime

from app import db


class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    title = db.Column(db.Text)

    def __repr__(self):
        return f"<Post {self.body}>"
