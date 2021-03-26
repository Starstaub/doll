from datetime import datetime, timedelta

from flask import flash, render_template, url_for
from werkzeug.utils import redirect

from app import app, db
from app.forms import AddOrEditTask, DeleteItem, PickCategoryAndStatus
from app.models import Task
from app.modules import get_unique_categories, pick_category_and_status, add_all_status


@app.route("/tasks", methods=["GET", "POST"])
def tasks():

    pick = PickCategoryAndStatus()
    pick.category.choices = get_unique_categories("task", all=True)
    pick.status.choices = add_all_status()

    results = pick_category_and_status("All", "All", "Newest first")

    if pick.validate_on_submit():

        chosen_status = pick.status.data
        chosen_category = pick.category.data
        chosen_order = pick.order.data

        results = pick_category_and_status(chosen_status, chosen_category, chosen_order)

        if results.first() is None:
            flash("Nothing to show yet.")

    return render_template(
        "tasks.html", title="Tasks", pick=pick, results=results, delete=False
    )


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
        if not task.description:
            task.description = "_[ No description ]_"
        task.created = datetime.utcnow() + timedelta(hours=1)

        db.session.add(task)
        db.session.commit()

        flash(f"The task '{form.title.data}' was successfully added.")

        return redirect(url_for("tasks"))

    return render_template("task_add.html", title="Add task", form=form)


@app.route("/task_delete/<string:id>", methods=["GET", "POST"])
def task_delete(id):

    form = DeleteItem()
    task = Task.query.filter_by(id=int(id)).first()

    if form.validate_on_submit():

        title = task.title

        db.session.delete(task)
        db.session.commit()

        flash(f"The task '{title}' was successfully deleted.")

        return redirect(url_for("tasks"))

    return render_template(
        "task_delete.html",
        title="Confirm delete task",
        form=form,
        result=task,
        delete=True,
    )
