from flask import Blueprint, render_template

schedule_bp = Blueprint("schedule_bp", __name__, template_folder="templates")


# Home page
@schedule_bp.route("/")
def schedule():
    return render_template("schedule.html")
