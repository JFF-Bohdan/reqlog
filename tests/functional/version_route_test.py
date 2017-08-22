from reqlog.version import __app_name__, __version__
from tests.functional.func_shared import setup_application


def test_version_route_returns_200():
    app = setup_application(False, False)

    resp = app.get("/version")
    assert resp.status_code == 200


def test_version_route_returns_valid_values():
    app = setup_application(False, False)

    resp = app.get("/version")
    assert resp.status_code == 200

    js_response = resp.json
    assert js_response is not None

    assert "version" in js_response
    assert "app_name" in js_response

    assert js_response["version"] == __version__
    assert js_response["app_name"] == __app_name__
