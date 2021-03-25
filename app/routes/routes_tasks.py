from datetime import datetime, timedelta

from flask import flash, render_template, url_for
from werkzeug.utils import redirect

from app import app, db
from app.forms import PickCategory, AddOrEditTask
from app.models import Task
from app.modules import get_unique_categories, pick_category


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
