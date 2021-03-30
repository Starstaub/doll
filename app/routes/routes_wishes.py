from flask import render_template, url_for, flash, request
from werkzeug.utils import redirect

from app import db, app
from app.forms import DeleteItem, PickCategory, AddOrEditWish
from app.models import Wish
from app.modules import get_unique_categories, pick_category


@app.route("/wishes", methods=["GET", "POST"])
def wishes():

    pick = PickCategory()
    pick.category.choices = get_unique_categories("wish", all=True)

    results = pick_category("wish", "All categories")

    if pick.validate_on_submit():

        chosen_pick = pick.category.data
        if chosen_pick == "All categories":
            results = pick_category("wish", "All categories")
        else:
            results = pick_category("wish", chosen_pick)

        if results.first() is None:
            flash("Nothing to show yet.")

    return render_template("wishes.html", title="Wishlist", pick=pick, results=results)


@app.route("/wish/add", methods=["GET", "POST"])
@app.route("/wish/edit/<string:id>", methods=["GET", "POST"])
def wish_add_edit(id=None):

    form = AddOrEditWish()
    form.category.choices = get_unique_categories("wish")

    if id:
        wish = Wish.query.filter_by(id=int(id)).first()
        title = "Edit wish"
        edit = True
    else:
        wish = Wish()
        title = "Add wish"
        edit = False

    if request.method == 'POST' and form.validate_on_submit():

        wish.category = form.category.data
        if wish.category and form.add_category.data:
            wish.category = form.add_category.data

        wish.web_url = form.web_url.data
        wish.description = form.description.data
        wish.title = form.title.data
        wish.website = form.website.data
        wish.picture_url = "![picture](" + form.picture_url.data + ")"

        if id:
            db.session.commit()
            flash(f"Your changes on '{wish.title}' have been saved.")
        else:
            db.session.add(wish)
            db.session.commit()
            flash(f"The wish '{form.title.data}' was successfully added.")

        return redirect(url_for("wishes"))

    elif id and request.method == "GET":

        form.category.data = wish.category
        form.web_url.data = wish.web_url
        form.description.data = wish.description
        form.title.data = wish.title
        form.year.data = wish.year
        form.website.data = wish.website

    return render_template("wish.html", title=title, form=form, edit=edit)


@app.route("/wish/delete/<string:id>", methods=["GET", "POST"])
def wish_delete(id):

    form = DeleteItem()
    wish = Wish.query.filter_by(id=int(id)).first()

    if form.validate_on_submit():

        title = wish.title

        db.session.delete(wish)
        db.session.commit()
        flash(f"The wish '{title}' was successfully deleted.")

        return redirect(url_for("wishes"))

    return render_template(
        "wish_delete.html", title="Confirm delete wish", form=form, result=wish
    )
