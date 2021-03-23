from flask_pagedown.fields import PageDownField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Optional, Length

from utils import TODO_STATUS


class AddOrEditPost(FlaskForm):

    title = StringField("Title", validators=[DataRequired(Length(min=0, max=100))])
    body = PageDownField("Body")

    submit = SubmitField("to infinity and beyond!")


class DeletePost(FlaskForm):

    submit = SubmitField("to the trash!")


class AddOrEditLink(FlaskForm):

    category = SelectField("Choose category")
    add_category = StringField("Category", Length(min=0, max=50))
    url = StringField("URL", Length(min=0, max=255))
    description = TextAreaField("Description")
    artist = StringField("Artist", Length(min=0, max=50))
    author = StringField("Author", Length(min=0, max=50))
    title = StringField("Title", validators=[DataRequired(Length(min=0, max=100))])
    year = IntegerField("Year", validators=[Optional()])
    website = StringField("Website", Length(min=0, max=100))
    isbn = IntegerField("ISBN", validators=[Optional()])

    submit = SubmitField("put that thing back where it came from or so help me")


class DeleteLink(FlaskForm):

    submit = SubmitField("be gone with it!")


class PickCategory(FlaskForm):

    category = SelectField("Choose category")

    submit = SubmitField("ay, show me the results")


class AddOrEditTask(FlaskForm):

    status = SelectField("Status", choices=TODO_STATUS)
    title = StringField("Title", Length(min=0, max=100))
    category = SelectField("Category")
    description = TextAreaField("Description")

    submit = SubmitField("add task")


class DeleteTask(FlaskForm):

    submit = SubmitField("bye bye")
