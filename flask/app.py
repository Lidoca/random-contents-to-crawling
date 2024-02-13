import sqlite3
from datetime import datetime

from flask import Flask, render_template, request, url_for

PER_PAGE = 12

app = Flask(__name__)

con = sqlite3.connect("example.db")
con.row_factory = sqlite3.Row
cur = con.cursor()

cur.execute("SELECT * FROM companies")
companies = [dict(row) for row in cur.fetchall()]

con.close()


@app.route("/")
def index():
    page = request.args.get("page", 1, type=int)
    total_pages = len(companies) // PER_PAGE
    if len(companies) % PER_PAGE > 0:
        total_pages += 1
    offset = (page - 1) * PER_PAGE

    paginated_companies = companies[offset : offset + PER_PAGE]

    current_year = datetime.now().year
    next_url = url_for("index", page=page + 1) if page < total_pages else None
    prev_url = url_for("index", page=page - 1) if page > 1 else None

    return render_template(
        "index.html.jinja",
        companies=paginated_companies,
        current_year=current_year,
        next_url=next_url,
        prev_url=prev_url,
        page=page,
        total_pages=total_pages,
    )


@app.route("/about")
def about():
    return render_template("about.html.jinja")


@app.route("/flask-health-check")
def flask_health_check():
    return "success"
