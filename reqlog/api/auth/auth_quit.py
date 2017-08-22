from reqlog.app import application


@application.route("/auth/quit", method="get")
def api_auth_quit():
    return application.jwt_plugin.get_resp_for_auth_cookie_erase("/login")
