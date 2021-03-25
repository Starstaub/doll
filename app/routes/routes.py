from flask import render_template

from app import app


@app.route("/markdown_guide")
def markdown_guide():

    return render_template("markdown_guide.html", title="Markdown guide")
