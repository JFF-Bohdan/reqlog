import bottle
from bottle import template
from reqlog.app import application
from reqlog.dbschema import DataCollectingDevice, DataCollectingNode, LoggedRequest, RequestParameters
from reqlog.pages.pages_shared import get_page_template_values
from reqlog.support.jwt_plugin import jwt_auth_required


@application.route("/brief/device/<device_uid>/request/<request_uid>")
@jwt_auth_required
def page_request_for_device_information(db, device_uid, request_uid):
    user = bottle.request.get_user()

    data = db.query(
        DataCollectingDevice,
        DataCollectingNode
    ).filter(
        DataCollectingDevice.dcd_uid == device_uid,
        DataCollectingDevice.is_in_use == True
    ).join(
        DataCollectingNode,
        DataCollectingDevice.dcn_id == DataCollectingNode.dcn_id
    ).filter(
        DataCollectingNode.owner_id == user.user_id,
        DataCollectingNode.is_in_use == True
    ).first()

    if data is None:
        bottle.abort(404)

    request = db.query(
        LoggedRequest
    ).filter(
        LoggedRequest.request_uid == request_uid,
        LoggedRequest.is_in_use == True
    ).scalar()

    if request is None:
        bottle.abort(404)

    dcd, dcn = data

    parameters = db.query(
        RequestParameters
    ).filter(
        RequestParameters.request_id == request.request_id,
        RequestParameters.is_in_use == True
    ).order_by(
        RequestParameters.parameter_name
    ).all()

    breadcrumbs = {
        "path": [
            (
                "/brief",
                "Brief"
            ),
            (
                "/brief/node/{}".format(dcn.dcn_uid),
                dcn.dcn_name
            ),

            (
                "/brief/device/{}".format(dcd.dcd_uid),
                dcd.dcd_name
            )

        ],
        "current": "Request details"
    }

    params = get_page_template_values(
        {
            "user": bottle.request.get_user(),
            "device": dcd,
            "node": dcn,
            "parameters": parameters,
            "request": request,
            "breadcrumbs": breadcrumbs
        },
        page_title="Request details".format(request_uid),
        page_header="Request details",
        page_description="uid = {}".format(request_uid)
    )

    return template("brief/request.tpl", **params)
