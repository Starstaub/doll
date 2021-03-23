from app import db
from app.models import Link


def pick_category(category):

    if category is "All":
        return Link.query
    if category == "Uncategorized":
        category = ""

    return Link.query.filter_by(category=category).order_by(Link.timestamp)


def get_unique_categories(all=False):

    category_list = db.session.query(Link.category).distinct().all()
    new_list = [i[0] for i in category_list]

    if all:
        new_list.insert(0, "All")
        new_list = ["Uncategorized" if x == "" else x for x in new_list]
    elif "" not in new_list:
        new_list.insert(0, "")

    return tuple((cat, cat) for cat in new_list)
