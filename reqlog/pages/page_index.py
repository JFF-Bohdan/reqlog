from bottle import redirect
from reqlog.app import application
from reqlog.support.jwt_plugin import jwt_auth_required


@application.route("/")
@application.route("/index")
@application.route("/index.htm")
@application.route("/index.html")
@jwt_auth_required
def api_index():
    redirect("/cabinet")
