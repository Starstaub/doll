from flask import render_template, url_for, flash, request
from werkzeug.utils import redirect

from app import db, app
from app.forms import DeleteItem, AddOrEditLink, PickCategory
from app.models import Link
from app.modules import get_unique_categories, pick_category


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
            flash("Nothing to show yet.")

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
        if not link.description:
                link.description = "_[ No description ]_"

        link.artist = form.artist.data
        link.author = form.author.data
        link.title = form.title.data
        link.year = form.year.data
        link.website = form.website.data
        link.isbn = form.isbn.data

        db.session.add(link)
        db.session.commit()

        flash(f"The link '{form.title.data}' was successfully added.")

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
        flash(f"Your changes on '{link.title}' have been saved.")

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
        flash(f"The link '{title}' was successfully deleted.")

        return redirect(url_for("links"))

    return render_template(
        "link_delete.html", title="Confirm delete link", form=form, result=link
    )
