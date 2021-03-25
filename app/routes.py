from datetime import datetime, timedelta

from flask import render_template, flash, url_for, request
from sqlalchemy import desc
from werkzeug.utils import redirect

from app import app, db
from app.forms import DeleteItem, PickCategory, AddOrEditPost, AddOrEditLink, AddOrEditTask
from app.models import Post, Link, Task
from app.modules import pick_category, get_unique_categories


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


@app.route("/links", methods=["GET", "POST"])
def links():

    pick = PickCategory()
    pick.category.choices = get_unique_categories("link", all=True)

    results = pick_category("link", "All")

    if pick.validate_on_submit():

        chosen_pick = pick.category.data
        if chosen_pick == "All":
            results = pick_category("link", "All")
        else:
            results = pick_category("link", chosen_pick)

        if results.first() is None:
            flash("nothing to see here, move on!")

    return render_template("links.html", title="Links", pick=pick, results=results)


@app.route("/link_add", methods=["GET", "POST"])
def link_add():

    form = AddOrEditLink()
    form.category.choices = get_unique_categories("link")

    if form.validate_on_submit():

        link = Link()

        link.category = form.category.data
        if link.category == "" and form.add_category.data:
            link.category = form.add_category.data

        link.url = form.url.data
        link.description = form.description.data
        link.artist = form.artist.data
        link.author = form.author.data
        link.title = form.title.data
        link.year = form.year.data
        link.website = form.website.data
        link.isbn = form.isbn.data

        db.session.add(link)
        db.session.commit()

        flash(f"{form.title.data} added successfully")

        return redirect(url_for("links"))

    return render_template("link_add.html", title="Add link", form=form)


@app.route("/link_edit/<string:id>", methods=["GET", "POST"])
def link_edit(id):

    form = AddOrEditLink()
    form.category.choices = get_unique_categories("link")
    link = Link.query.filter_by(id=int(id)).first()

    if request.method == "POST" and form.validate_on_submit():

        link.category = form.category.data
        if (link.category or link.category == "") and form.add_category.data:
            link.category = form.add_category.data
        link.url = form.url.data
        link.description = form.description.data
        link.artist = form.artist.data
        link.author = form.author.data
        link.title = form.title.data
        link.year = form.year.data
        link.website = form.website.data
        link.isbn = form.isbn.data

        db.session.commit()
        flash(f"your changes on {link.title} have been saved.")

        return redirect(url_for("links"))

    elif request.method == "GET":

        form.category.data = link.category
        form.add_category.data = link.category
        form.url.data = link.url
        form.description.data = link.description
        form.artist.data = link.artist
        form.author.data = link.author
        form.title.data = link.title
        form.year.data = link.year
        form.website.data = link.website
        form.isbn.data = link.isbn

    return render_template("link_edit.html", title="Edit link", form=form)


@app.route("/link_delete/<string:id>", methods=["GET", "POST"])
def link_delete(id):

    form = DeleteItem()
    link = Link.query.filter_by(id=int(id)).first()

    if form.validate_on_submit():

        title = link.title

        db.session.delete(link)
        db.session.commit()
        flash(f"the amigo {title} was successfully deleted")

        return redirect(url_for("links"))

    return render_template(
        "link_delete.html", title="Confirm delete link", form=form, link=link
    )


@app.route("/markdown_guide")
def markdown_guide():

    return render_template("markdown_guide.html", title="Markdown guide")


@app.route("/tasks", methods=['GET', 'POST'])
def tasks():

    pick = PickCategory()
    pick.category.choices = get_unique_categories("task", all=True)

    results = pick_category("task", "All")

    if pick.validate_on_submit():

        chosen_pick = pick.category.data
        if chosen_pick == "All":
            results = pick_category("task", "All")
        else:
            results = pick_category("task", chosen_pick)

        if results.first() is None:
            flash("nothing to see here, move on!")

    return render_template("tasks.html", title="Tasks", pick=pick, results=results)


@app.route("/task_add", methods=["GET", "POST"])
def task_add():

    form = AddOrEditTask()
    form.category.choices = get_unique_categories("task")

    if form.validate_on_submit():

        task = Task()

        task.status = form.status.data
        task.category = form.category.data
        if task.category and form.add_category.data:
            task.category = form.add_category.data
        task.title = form.title.data
        task.description = form.description.data
        task.created = datetime.utcnow() + timedelta(hours=1)

        db.session.add(task)
        db.session.commit()

        flash(f"Task '{form.title.data}' successfully added.")

        return redirect(url_for('tasks'))

    return render_template("task_add.html", title="Add task", form=form)
