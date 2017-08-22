import datetime

import bottle
from bottle import template
from reqlog.app import application
from reqlog.dbschema import DataCollectingDevice, DataCollectingNode
from reqlog.dbschema.shared import get_base62_ksuid
from reqlog.pages.pages_shared import get_page_template_values
from reqlog.support.jwt_plugin import jwt_auth_required


@application.route("/settings/devices")
@jwt_auth_required
def page_settings_devices(db):
    user = bottle.request.get_user()

    nodes = db.query(
        DataCollectingNode.dcn_id
    ).filter(
        DataCollectingNode.owner_id == user.user_id,
        DataCollectingNode.is_in_use == True
    ).subquery()

    data = db.query(
        DataCollectingDevice,
        DataCollectingNode
    ).filter(
        DataCollectingDevice.dcn_id.in_(nodes),
        DataCollectingDevice.is_in_use == True
    ).join(
        DataCollectingNode,
        DataCollectingDevice.dcn_id == DataCollectingNode.dcn_id
    ).order_by(
        DataCollectingDevice.dcd_name
    ).all()

    breadcrumbs = {
        "path": [

        ],
        "current": "Settings devices"
    }

    params = get_page_template_values(
        {
            "user": bottle.request.get_user(),
            "data": data,
            "breadcrumbs": breadcrumbs
        },
        page_title="Settings devices",
        page_header="Settings/Devices",
        page_description="devices list"
    )

    return template("settings/settings_devices_list.tpl", **params)


def load_device_by_uid_and_user_id(db, device_uid, user_id):
    return db.query(
        DataCollectingDevice
    ).filter(
        DataCollectingDevice.dcd_uid == device_uid,
        DataCollectingDevice.is_in_use == True
    ).join(
        DataCollectingNode,
        DataCollectingDevice.dcn_id == DataCollectingNode.dcn_id
    ).filter(
        DataCollectingNode.owner_id == user_id,
        DataCollectingNode.is_in_use == True
    ).scalar()


@application.route("/api/settings/device/<device_uid>/tokens/write/generate_new", method=["post"])
@application.route("/api/settings/device/<device_uid>/tokens/write/clear", method=["post"])
@application.route("/api/settings/device/<device_uid>/tokens/read/generate_new", method=["post"])
@application.route("/api/settings/device/<device_uid>/tokens/read/clear", method=["post"])
@jwt_auth_required
def api_settings_for_device_tokens_mgt(db, device_uid):

    need_clear = "/clear" in str(bottle.request.path)
    write_token = "/tokens/write" in str(bottle.request.path)

    user = bottle.request.get_user()

    device = load_device_by_uid_and_user_id(db, device_uid, user.user_id)
    if device is None:
        bottle.abort(404)

    if write_token:
        old_token = device.write_token

        if need_clear:
            device.write_token = None
        else:
            device.write_token = get_base62_ksuid()

        new_token = device.write_token

    else:
        old_token = device.read_token

        if need_clear:
            device.read_token = None
        else:
            device.read_token = get_base62_ksuid()

        new_token = device.read_token

    db.commit()
    return {
        "new_uid": new_token,
        "old_uid": old_token,
    }


@application.route("/settings/device/<device_uid>", method=["get", "post"])
@jwt_auth_required
def page_settings_for_device(db, device_uid):
    user = bottle.request.get_user()

    data = db.query(
        DataCollectingDevice,
        DataCollectingNode
    ).filter(
        DataCollectingDevice.dcd_uid == device_uid,
        DataCollectingDevice.is_in_use == True
    ).join(
        DataCollectingNode,
        DataCollectingDevice.dcn_id == DataCollectingNode.dcn_id,
    ).filter(
        DataCollectingNode.owner_id == user.user_id,
        DataCollectingNode.is_in_use == True
    ).order_by(
        DataCollectingDevice.dcd_name
    ).first()

    if data is None:
        bottle.abort(404)

    device, node = data

    if bottle.request.method == "POST":
        dcd_name = bottle.request.forms.device_name
        dcd_description = bottle.request.forms.device_description

        device.dcd_name = dcd_name
        device.description = dcd_description
        device.update_dts = datetime.datetime.utcnow()

        db.flush()
        db.commit()

        bottle.redirect("/settings/devices")

    breadcrumbs = {
        "path": [
            (
                "/settings/devices",
                "Settings-Devices"
            )
        ],
        "current": device.dcd_name
    }

    params = get_page_template_values(
        {
            "user": bottle.request.get_user(),
            "device": device,
            "node": node,
            "breadcrumbs": breadcrumbs,
            "info_message_title": "Info title",
            "info_message_text": "Info text, line1\nline2"
        },
        page_title="Settings/{}".format(device.dcd_name),
        page_header="{}".format(device.dcd_name),
        page_description="Settings for device ({})".format(device.dcd_name)
    )

    return template("settings/settings_device.tpl", **params)
