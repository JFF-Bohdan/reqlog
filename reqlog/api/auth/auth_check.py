import bottle

from reqlog.app import application
from reqlog.support.jwt_plugin.auth import jwt_auth_required, jwt_soft_auth_check_required


@application.route("/auth/check", method="get")
@jwt_auth_required
def api_auth_check():
    r = bottle.request

    return {
        "ok": True,
        "user_uid": r.environ["jwt_user_id"]
    }


@application.route("/auth/soft_check", method="get")
@jwt_soft_auth_check_required
def api_auth_soft_check(is_authenticated):
    return {
        "authenticated": is_authenticated
    }
