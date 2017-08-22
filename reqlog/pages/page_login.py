from bottle import template
from reqlog.app import application

from .pages_shared import current_year


@application.route("/login")
def api_login():
    params = {
        "web_app_name": str(application.config.get("main", "webappname")),
        "current_year": current_year()
    }
    return template("login.tpl", **params)
