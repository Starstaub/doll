from datetime import datetime

from flask import render_template, url_for, flash, request
from sqlalchemy import desc
from werkzeug.utils import redirect

from app import db, app
from app.forms import DeleteItem, AddOrEditPost
from app.models import Post


@app.route("/")
@app.route("/index")
def index():

    posts = Post.query.order_by(desc(Post.timestamp)).all()

    return render_template("index.html", title="Home", posts=posts)


@app.route("/post_add", methods=["GET", "POST"])
def post_add():

    form = AddOrEditPost()

    if form.validate_on_submit():

        post_data = Post(
            body=form.body.data, title=form.title.data, nb_char=len(form.body.data)
        )
        db.session.add(post_data)
        db.session.commit()
        flash("post now online.")

        return redirect(url_for("index"))

    return render_template("post_add.html", title="Add Post", form=form)


@app.route("/post_edit/<string:id>", methods=["GET", "POST"])
def post_edit(id):

    form = AddOrEditPost()
    post_data = Post.query.filter_by(id=int(id)).first()

    if request.method == "POST" and form.validate_on_submit():
        post_data.title = form.title.data
        post_data.body = form.body.data
        post_data.nb_char = len(form.body.data)
        post_data.edit_time = datetime.utcnow()
        db.session.commit()
        flash("your changes have been saved.")

        return redirect(url_for("index"))

    elif request.method == "GET":
        form.title.data = post_data.title
        form.body.data = post_data.body

    return render_template("post_edit.html", title="Edit post", form=form)


@app.route("/post_delete/<string:id>", methods=["GET", "POST"])
def post_delete(id):

    form = DeleteItem()
    post_data = Post.query.filter_by(id=int(id)).first()

    if form.validate_on_submit():
        db.session.delete(post_data)
        db.session.commit()
        flash("so long, partner.")

        return redirect(url_for("index"))

    return render_template(
        "post_delete.html", title="Confirm delete post", form=form, post=post_data
    )


@app.route("/post/<string:id>", methods=["GET"])
def post(id):

    post_data = Post.query.filter_by(id=int(id)).first()

    return render_template("post.html", title=post_data.title, post=post_data)
