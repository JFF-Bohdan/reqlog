from bottle import static_file
from reqlog.app import application


@application.route("/static/<filepath:path>")
def api_version(filepath):
    return static_file(filepath, root=application.static_files_path)
