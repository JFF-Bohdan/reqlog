from reqlog.support.db_init.initialization_consts import DEMO_DEVICE_WRITE_TOKEN
from tests.functional.func_shared import setup_application


def test_returns_401_on_no_access_token_sent():
    app = setup_application(force_recreate_database=False, force_initialize_database=False)

    params = {
        "foo": "bar",
        "bizz": "bazz",
        "boo": "poo"
    }
    resp = app.post("/collect", params=params, expect_errors=True)

    assert resp.status_code == 401


def test_returns_403_when_wrong_token_sent_in_request_parameters():
    app = setup_application(force_recreate_database=False, force_initialize_database=False)

    params = {
        "foo": "bar",
        "bizz": "bazz",
        "boo": "poo",
        "t": "bad"
    }
    resp = app.post("/collect", params=params, expect_errors=True)

    assert resp.status_code == 403


def test_returns_403_when_wrong_token_sent_in_request_header():
    app = setup_application(force_recreate_database=False, force_initialize_database=False)

    params = {
        "foo": "bar",
        "bizz": "bazz",
        "boo": "poo",
    }

    headers = {
        "access_token": "bad"
    }
    resp = app.post("/collect", params=params, headers=headers, expect_errors=True)

    assert resp.status_code == 403


def test_successfully_adds_values():
    app = setup_application()

    params = {
        "foo": "bar",
        "bizz": "bazz",
        "boo": "poo",
        "t": DEMO_DEVICE_WRITE_TOKEN
    }
    resp = app.post("/collect", params=params)

    assert resp.status_code == 200

    assert resp.json is not None
    json_resp = resp.json

    assert "method" in json_resp
    assert "dcd_id" in json_resp
    assert "request" in json_resp

    request_info = json_resp["request"]
    assert type(request_info) == dict

    assert "id" in request_info
    assert "uid" in request_info
    assert "params" in request_info

    request_id = request_info["id"]

    assert request_id is not None
    assert str(request_id).isnumeric()

    assert request_id == 1

    response_params = request_info["params"]
    for item in params:
        if item == "t":
            continue

        assert item in response_params


def test_successfully_adds_values_again():
    app = setup_application(force_recreate_database=True, force_initialize_database=True)

    params = {
        "foo": "bar",
        "bizz": "bazz",
        "boo": "poo",
        "t": DEMO_DEVICE_WRITE_TOKEN
    }
    resp = app.post("/collect", params=params)

    assert resp.status_code == 200

    assert resp.json is not None
    json_resp = resp.json

    request_id = json_resp["request"]["id"]
    assert str(request_id).isnumeric()

    assert request_id == 1


def test_successfully_adds_values_with_access_token_in_header():
    app = setup_application(force_recreate_database=False, force_initialize_database=False)

    headers = {
        "access_token": DEMO_DEVICE_WRITE_TOKEN
    }

    expected_t_value = "foo_bar"

    params = {
        "foo": "bar",
        "bizz": "bazz",
        "boo": "poo",
        "t": expected_t_value
    }
    resp = app.post("/collect", params=params, headers=headers)

    assert resp.status_code == 200

    assert resp.json is not None
    json_resp = resp.json

    assert "method" in json_resp
    assert "dcd_id" in json_resp
    assert "request" in json_resp

    request_info = json_resp["request"]
    assert type(request_info) == dict

    assert "id" in request_info
    assert "uid" in request_info
    assert "params" in request_info

    request_id = request_info["id"]

    assert request_id is not None
    assert str(request_id).isnumeric()

    assert request_id > 0

    added_params = request_info["params"]
    assert "t" in added_params
    assert added_params["t"] == expected_t_value

    response_params = request_info["params"]
    for item in params:
        assert item in response_params
