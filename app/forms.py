from flask_pagedown.fields import PageDownField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Optional, Length

from utils import TODO_STATUS


class AddOrEditPost(FlaskForm):

    title = StringField("Title", validators=[Length(min=0, max=100), DataRequired()])
    body = PageDownField("Body")

    submit = SubmitField("Send")


class AddOrEditLink(FlaskForm):

    category = SelectField("Category")
    add_category = StringField("Category", validators=[Length(min=0, max=50)])
    url = StringField("URL", validators=[Length(min=0, max=255)])
    description = TextAreaField("Description")
    artist = StringField("Artist", validators=[Length(min=0, max=50)])
    author = StringField("Author", validators=[Length(min=0, max=50)])
    title = StringField("Title", validators=[Length(min=0, max=100), DataRequired()])
    year = IntegerField("Year", validators=[Optional()])
    website = StringField("Website", validators=[Length(min=0, max=100)])
    isbn = IntegerField("ISBN", validators=[Optional()])

    submit = SubmitField("Send")


class PickCategory(FlaskForm):

    category = SelectField("Category")

    submit = SubmitField("Send")


class AddOrEditTask(FlaskForm):

    status = SelectField("Status", choices=TODO_STATUS, validators=[DataRequired()])
    title = StringField("Title", validators=[Length(min=0, max=100), DataRequired()])
    category = SelectField("Category", validators=[DataRequired()])
    add_category = StringField("Category", validators=[Length(min=0, max=50), Optional()])
    description = PageDownField("Description")

    submit = SubmitField("Send")


class DeleteItem(FlaskForm):

    submit = SubmitField("Delete permanently")