from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_pagedown import PageDown
from flask_misaka import Misaka


from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
pagedown = PageDown(app)
Misaka(app)

from app import routes, models
