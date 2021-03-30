from flask_pagedown.fields import PageDownField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, IntegerField, FloatField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired, Optional, Length, url

from utils import TODO_STATUS, ORDER_BY


class AddOrEditPost(FlaskForm):

    title = StringField("Title", validators=[Length(min=0, max=100), DataRequired()])
    body = PageDownField("Body")

    submit = SubmitField("Send")


class AddOrEditWish(FlaskForm):

    category = SelectField("Category")
    add_category = StringField("Category", validators=[Length(min=0, max=15)])
    web_url = URLField("URL", validators=[url()], render_kw={"placeholder": "http://..."})
    description = TextAreaField("Description")
    title = StringField("Title", validators=[Length(min=0, max=100), DataRequired()])
    year = IntegerField("Year", validators=[Optional()], render_kw={"placeholder": "1970"})
    website = StringField("Website", validators=[Length(min=0, max=50)])
    picture_url = StringField("Picture URL", render_kw={"placeholder": "http://..."})
    price = FloatField("Price", validators=[Optional()], render_kw={"placeholder": "9.99"})

    submit = SubmitField("Send")


class PickCategory(FlaskForm):

    category = SelectField("Category")

    submit = SubmitField("Send")


class PickCategoryAndStatus(FlaskForm):

    status = SelectField("Status", validators=[DataRequired()])
    category = SelectField("Category", validators=[DataRequired()])
    order = SelectField("Order by", choices=ORDER_BY, validators=[DataRequired()])

    submit = SubmitField("Search")


class AddOrEditTask(FlaskForm):

    status = SelectField("Status", choices=TODO_STATUS, validators=[DataRequired()])
    title = StringField("Title", validators=[Length(min=0, max=100), DataRequired()])
    category = SelectField("Category", validators=[DataRequired()])
    add_category = StringField(
        "Category", validators=[Length(min=0, max=15), Optional()]
    )
    description = PageDownField("Description")

    submit = SubmitField("Send")


class DeleteItem(FlaskForm):

    submit = SubmitField("Delete permanently")
