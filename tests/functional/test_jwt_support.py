from reqlog.support.db_init.initialization_consts import DEMO_USER_LOGIN, DEMO_USER_PASSWORD, DEMO_USER_UID
from tests.functional.func_shared import setup_application


def test_returns_403_when_checking_token_without_authentication():
    headers = {
        "client_type": "json_api"
    }

    app = setup_application(force_recreate_database=False, force_initialize_database=False)
    resp = app.get("/auth/check", headers=headers, expect_errors=True)

    assert resp.status_code == 403


def test_returns_302_when_checking_token_without_authentication():
    app = setup_application(force_recreate_database=False, force_initialize_database=False)
    resp = app.get("/auth/check", expect_errors=True)

    assert resp.status_code == 302


def test_authenticates_jwt_to_demo_user():
    auth_params = {
        "login": DEMO_USER_LOGIN,
        "password": DEMO_USER_PASSWORD
    }

    app = setup_application(force_recreate_database=True, force_initialize_database=True)
    resp = app.post("/auth/token", params=auth_params, expect_errors=False)

    assert resp.status_code == 200
    assert resp.json is not None

    json_response = resp.json
    assert "access_token" in json_response
    assert "scope" in json_response
    assert "token_type" in json_response
    assert "expires_in" in json_response

    assert json_response["access_token"] is not None
    # TODO: validate token

    assert "Authorization" in resp.headers
    assert "Authorization-Scope" in resp.headers
    assert "Authorization-Token-Type" in resp.headers
    assert "Authorization-Expires-In" in resp.headers

    assert resp.headers["Authorization"] == "Bearer " + json_response["access_token"]
    assert resp.headers["Authorization-Scope"] == json_response["scope"]
    assert resp.headers["Authorization-Token-Type"] == json_response["token_type"]
    assert str(resp.headers["Authorization-Expires-In"]) == str(json_response["expires_in"])

    cookie_found = False
    for k, v in resp.headers.items():
        v = str(v)
        if k == "Set-Cookie":
            if v.startswith("Authorization"):
                auth_cookie_value = v[v.index("=") + 2: v.index(";") - 1]
                assert auth_cookie_value is not None

                assert auth_cookie_value == "Bearer " + json_response["access_token"]
                cookie_found = True

    assert cookie_found


def test_returns_200_when_checking_valid_jwt():
    auth_params = {
        "login": DEMO_USER_LOGIN,
        "password": DEMO_USER_PASSWORD
    }

    app = setup_application(force_recreate_database=False, force_initialize_database=False)
    resp = app.post("/auth/token", params=auth_params, expect_errors=False)

    assert resp.status_code == 200
    assert resp.json is not None

    json_response = resp.json
    token = json_response["access_token"]

    headers = {
        "Authorization": "Bearer " + token
    }

    resp = app.get("/auth/check", headers=headers, expect_errors=False)
    assert resp.status_code == 200
    assert resp.json is not None

    json_resp = resp.json
    assert "ok" in json_resp
    assert "user_uid" in json_resp

    assert json_resp["ok"] == True
    assert json_resp["user_uid"] == DEMO_USER_UID


def test_soft_auth_check_returns_false_when_not_authenticated():
    app = setup_application(force_recreate_database=False, force_initialize_database=False)
    resp = app.get("/auth/soft_check")

    assert resp.status_code == 200
    assert resp.json is not None

    json_response = resp.json
    assert "authenticated" in json_response

    assert not json_response["authenticated"]


def test_soft_auth_check_returns_true_when_not_authenticated():
    auth_params = {
        "login": DEMO_USER_LOGIN,
        "password": DEMO_USER_PASSWORD
    }

    app = setup_application(force_recreate_database=True, force_initialize_database=True)
    resp = app.post("/auth/token", params=auth_params, expect_errors=False)

    assert resp.status_code == 200
    assert resp.json is not None

    json_response = resp.json
    assert "access_token" in json_response
    assert "scope" in json_response
    assert "token_type" in json_response
    assert "expires_in" in json_response

    assert json_response["access_token"] is not None

    resp = app.get("/auth/soft_check")

    assert resp.status_code == 200
    assert resp.json is not None

    json_response = resp.json
    assert "authenticated" in json_response

    assert json_response["authenticated"]
