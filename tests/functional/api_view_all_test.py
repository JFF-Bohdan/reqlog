import ksuid
from reqlog.support.db_init.initialization_consts import DEMO_DEVICE_READ_TOKEN, DEMO_DEVICE_WRITE_TOKEN
from tests.functional.func_shared import setup_application


def test_returns_401_on_no_access_token_sent():
    app = setup_application(force_recreate_database=True, force_initialize_database=False)

    resp = app.get("/view_all", expect_errors=True)

    assert resp.status_code == 401


def test_returns_403_when_wrong_token_sent_in_request_parameters():
    app = setup_application(force_recreate_database=True, force_initialize_database=False)

    params = {
        "t": "bad"
    }
    resp = app.get("/view_all", params=params, expect_errors=True)

    assert resp.status_code == 403


def test_returns_403_when_wrong_token_sent_in_request_header():
    app = setup_application(force_recreate_database=True, force_initialize_database=False)

    headers = {
        "access_token": "bad"
    }
    resp = app.get("/view_all", headers=headers, expect_errors=True)

    assert resp.status_code == 403


def test_adds_and_returns_valid_events():
    app = setup_application(force_recreate_database=True, force_initialize_database=True)

    headers = {
        "access_token": DEMO_DEVICE_WRITE_TOKEN
    }

    expected_uid = ksuid.ksuid().toBase62()
    params = {
        "id": expected_uid,
        "foo": "bar",
        "bizz": "bazz",
        "boo": "poo",
        "t": "special"
    }
    resp = app.post("/collect", params=params, headers=headers)

    assert resp.status_code == 200

    assert resp.json is not None
    json_resp = resp.json

    requies_uid = json_resp["request"]["uid"]
    assert requies_uid is not None

    headers = {
        "access_token": DEMO_DEVICE_READ_TOKEN
    }
    resp = app.get("/view_all", headers=headers)
    assert resp.status_code == 200

    assert resp.json is not None
    json_resp = resp.json

    assert "data" in json_resp
    json_data = json_resp["data"]
    assert type(json_data) == list

    found = False
    for item in json_data:
        assert "request_uid" in item
        assert "request_id" in item
        assert "request_uid" in item
        assert "adding_dts" in item
        assert "method" in item
        assert "parameters" in item

        if item["request_uid"] == requies_uid:
            v = {item["name"]: item["value"] for item in item["parameters"]}

            assert v == params
            found = True
            break

    assert found
