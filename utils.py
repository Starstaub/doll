from datetime import datetime, timedelta

NOW_TIME = datetime.utcnow() + timedelta(hours=1)

TODO_STATUS = (
    ('To do', 'To do'),
    ('In progress', 'In progress'),
    ('On hold', 'On hold'),
    ('Done', 'Done')
)

ORDER_BY = (
    ("Newest first", "Newest first"),
    ("Oldest first", "Oldest first")
)