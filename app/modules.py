from flask import request, url_for
from sqlalchemy import desc

from app import db
from app.models import Link, Task
from utils import TODO_STATUS


def pick_category(model, category):

    if category == "All":
        if model == "link":
            return Link.query
        elif model == "task":
            return Task.query

    if model == "link":
        return Link.query.filter_by(category=category).order_by("timestamp")
    elif model == "task":
        return Task.query.filter_by(category=category).order_by("created")


def pick_category_and_status(status, category, order):

    if status == "All" and category == "All":
        if order == "Newest first":
            return Task.query.order_by(desc("created"))
        return Task.query.order_by("created")

    elif status == "All":
        if order == "Newest first":
            return Task.query.filter_by(category=category).order_by(desc("created"))
        return Task.query.filter_by(category=category).order_by("created")

    elif category == "All":
        if order == "Newest first":
            return Task.query.filter_by(status=status).order_by(desc("created"))
        return Task.query.filter_by(status=status).order_by("created")

    else:
        if order == "Newest first":
            return Task.query.filter_by(category=category, status=status).order_by(desc("created"))
        return Task.query.filter_by(category=category, status=status).order_by("created")


def get_unique_categories(model_name, all=False):

    category_list = []

    if model_name == "link":
        category_list = db.session.query(Link.category).distinct().all()
    elif model_name == "task":
        category_list = db.session.query(Task.category).distinct().all()

    new_list = [i[0] for i in category_list]

    if all:
        new_list.insert(0, "All")
    elif "Uncategorized" not in new_list:
        new_list.insert(0, "Uncategorized")

    return tuple((cat, cat) for cat in new_list)


def add_all_status():

    status_list = list(TODO_STATUS)
    status_list.insert(0, ("All", "All"))

    new_status_list = []

    for ele in status_list:
        temp = list(ele)
        if temp[0] == "All":
            temp_count = db.session.query(Task.category).count()
        else:
            temp_count = Task.query.filter_by(status=temp[0]).count()
        temp[1] += " (" + str(temp_count) + ")"
        new_status_list.append(tuple(temp))

    return tuple(new_status_list)


def pages_pagination(results, number_per_page, url):

    page = request.args.get('page', 1, type=int)
    pagination = results.paginate(page,
                                  per_page=number_per_page,
                                  error_out=False)
    count = results.count()

    next_url = (
        url_for(
            url,
            page=pagination.next_num,
        )
        if pagination.has_next
        else None
    )

    prev_url = (
        url_for(
            url,
            page=pagination.prev_num,
        )
        if pagination.has_prev
        else None
    )

    return pagination, count, prev_url, next_url
