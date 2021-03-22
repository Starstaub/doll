from flask import render_template, flash, url_for, request
from sqlalchemy import desc
from werkzeug.utils import redirect

from app import app, db
from app.forms import CreatePost, EditPost, DeletePost
from app.models import Post


@app.route("/")
@app.route("/index")
def index():

    posts = Post.query.order_by(desc(Post.timestamp)).all()
    meh = "# hey"

    return render_template("index.html", title="Home", posts=posts, meh=meh)


@app.route("/add", methods=['GET', 'POST'])
def add():

    form = CreatePost()

    if form.validate_on_submit():
        post = Post(body=form.body.data, title=form.title.data)
        db.session.add(post)
        db.session.commit()
        flash('post now online.')

        return redirect(url_for('index'))

    return render_template("add.html", title='Add Post', form=form)


@app.route("/edit/<string:id>", methods=['GET', 'POST'])
def edit(id):

    form = EditPost()
    post = Post.query.filter_by(id=int(id)).first()

    if request.method == "POST" and form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        db.session.commit()
        flash("your changes have been saved.")

        return redirect(url_for("index"))

    elif request.method == "GET":
        form.title.data = post.title
        form.body.data = post.body

    return render_template("edit.html", title="Edit post", form=form)


@app.route("/delete/<string:id>", methods=['GET', 'POST'])
def delete(id):

    form = DeletePost()
    post = Post.query.filter_by(id=int(id)).first()

    if form.validate_on_submit():
        db.session.delete(post)
        db.session.commit()
        flash("so long, partner.")

        return redirect(url_for("index"))

    return render_template("delete.html", title="Confirm delete post", form=form, post=post)