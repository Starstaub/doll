from flask_pagedown.fields import PageDownField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class CreatePost(FlaskForm):

    title = StringField("Title", validators=[DataRequired()])
    body = PageDownField("Body")
    submit = SubmitField("Submit")


class EditPost(FlaskForm):

    title = StringField("Title", validators=[DataRequired()])
    body = PageDownField("Body")
    submit = SubmitField("Submit edited post")


class DeletePost(FlaskForm):

    submit = SubmitField("to the trash!")