from flask import (
    Blueprint,
    render_template,
)

bp = Blueprint("dashboard", __name__)


@bp.route("/dashboard", methods=["GET", "POST"])
def home():
    return render_template("dashboard/home.html", title="Home")
