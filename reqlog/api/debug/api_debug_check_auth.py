import bottle

from reqlog.app import application
from reqlog.support.jwt_plugin import jwt_auth_required


@application.route("/api/debug_check_auth", method="get", jwt_scopes=["foo", "bar", "bizz", "bazz"])
@jwt_auth_required
def api_login():
    r = bottle.request

    return {
        "ok": "true",
        "user": str(r.get_user())
    }
