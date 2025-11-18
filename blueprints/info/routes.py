from flask import Blueprint, render_template

info_bp = Blueprint("info_bp", __name__, template_folder="templates")


# Home page
@info_bp.route("/")
def info():
    return render_template("info.html")
