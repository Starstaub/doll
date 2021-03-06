from datetime import datetime, timedelta

from flask import flash, render_template, url_for, request
from werkzeug.utils import redirect

from app import app, db
from app.forms import AddOrEditTask, DeleteItem, PickCategoryAndStatus
from app.models import Task
from app.modules import (
    get_unique_categories,
    pick_category_and_status,
    add_all_status,
    pages_pagination,
)


@app.route("/tasks", methods=["GET", "POST"])
def tasks():

    pick = PickCategoryAndStatus()
    pick.category.choices = get_unique_categories("task", all=True)
    pick.status.choices = add_all_status()

    results = pick_category_and_status("All statuses", "All categories", "Newest first")

    pagination, count, prev_url, next_url = pages_pagination(
        results, app.config["TASKS_PER_PAGE"], "tasks"
    )

    if pick.validate_on_submit():

        chosen_status = pick.status.data
        chosen_category = pick.category.data
        chosen_order = pick.order.data

        results = pick_category_and_status(chosen_status, chosen_category, chosen_order)

        pagination, count, prev_url, next_url = pages_pagination(
            results, app.config["TASKS_PER_PAGE"], "tasks"
        )

        if results.first() is None:
            flash("Nothing to show yet.")

    return render_template(
        "tasks.html",
        title="Tasks",
        pick=pick,
        results=pagination.items,
        delete=False,
        count=count,
        next_url=next_url,
        prev_url=prev_url,
        page=pagination.page,
        pages=pagination.pages,
    )


@app.route("/task/delete/<string:id>", methods=["GET", "POST"])
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


@app.route("/task/add", methods=["GET", "POST"])
@app.route("/task/edit/<string:id>", methods=["GET", "POST"])
def task_add_edit(id=None):

    form = AddOrEditTask()
    form.category.choices = get_unique_categories("task")

    if id:
        task = Task.query.filter_by(id=int(id)).first()
        title = "Edit task"
        edit = True
    else:
        task = Task()
        title = "Add task"
        edit = False

    if request.method == "POST" and form.validate_on_submit():

        task.status = form.status.data
        task.category = form.category.data
        if task.category and form.add_category.data:
            task.category = form.add_category.data
        task.title = form.title.data
        task.description = form.description.data
        if not task.description:
            task.description = "_[ No description ]_"

        if id:
            task.modified = datetime.utcnow() + timedelta(hours=1)
            db.session.commit()
            flash(f"The changes on '{task.title}' have been saved.")

        else:
            task.created = datetime.utcnow() + timedelta(hours=1)
            db.session.add(task)
            db.session.commit()
            flash(f"The task '{form.title.data}' was successfully added.")

        return redirect(url_for("tasks"))

    elif id and request.method == "GET":

        form.status.data = task.status
        form.category.data = task.category
        form.title.data = task.title
        if task.description == "_[ No description ]_":
            form.description.data = ""
        else:
            form.description.data = task.description

    return render_template("task.html", title=title, form=form, edit=edit)
