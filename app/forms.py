from flask_pagedown.fields import PageDownField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Optional


class AddOrEditPost(FlaskForm):

    title = StringField("Title", validators=[DataRequired()])
    body = PageDownField("Body")

    submit = SubmitField("to infinity and beyond!")


class DeletePost(FlaskForm):

    submit = SubmitField("to the trash!")


class AddOrEditLink(FlaskForm):

    category = SelectField("Choose category")
    add_category = StringField("Category")
    url = StringField("URL")
    description = TextAreaField("Description")
    artist = StringField("Artist")
    author = StringField("Author")
    title = StringField("Title", validators=[DataRequired()])
    year = IntegerField("Year", validators=[Optional()])
    website = StringField("Website")
    isbn = IntegerField("ISBN", validators=[Optional()])

    submit = SubmitField("put that thing back where it came from or so help me")


class DeleteLink(FlaskForm):

    submit = SubmitField("be gone with it!")


class PickCategory(FlaskForm):

    category = SelectField("Choose category")

    submit = SubmitField("ay, show me the results")
