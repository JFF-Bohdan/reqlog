from reqlog.app import application
from reqlog.version import __app_name__, __version__


@application.route("/version")
def api_version():
    return {
        "app_name": __app_name__,
        "version": __version__
    }
