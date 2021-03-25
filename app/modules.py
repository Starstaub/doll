from app import db
from app.models import Link, Task


def pick_category(model, category):

    if category == "All":
        if model == "link":
            return Link.query
        elif model == "task":
            return Task.query

    if model == "link":
        return Link.query.filter_by(category=category).order_by(Link.timestamp)
    elif model == "task":
        return Task.query.filter_by(category=category).order_by(Task.created)


def get_unique_categories(model_name, all=False):

    category_list = []

    if model_name == 'link':
        category_list = db.session.query(Link.category).distinct().all()
    elif model_name == 'task':
        category_list = db.session.query(Task.category).distinct().all()

    new_list = [i[0] for i in category_list]

    if all:
        new_list.insert(0, "All")
    elif "Uncategorized" not in new_list:
        new_list.insert(0, "Uncategorized")

    return tuple((cat, cat) for cat in new_list)
