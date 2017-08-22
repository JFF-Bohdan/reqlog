import bottle
from bottle import template
from reqlog.app import application
from reqlog.dbschema import DataCollectingDevice, DataCollectingNode, LoggedRequest, RequestParameters
from reqlog.pages.pages_shared import get_page_template_values, MAX_PARAMS_COUNT, MAX_REQUESTS_COUNT
from reqlog.support.jwt_plugin import jwt_auth_required
import sqlalchemy


@application.route("/brief/device/<device_uid>")
@jwt_auth_required
def page_device_information(db, device_uid):
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

    dcd, dcn = data

    requests = db.query(
        LoggedRequest
    ).filter(
        LoggedRequest.dcd_id == dcd.dcd_id,
        LoggedRequest.is_in_use == True
    ).order_by(
        sqlalchemy.desc(LoggedRequest.adding_dts),
        sqlalchemy.desc(LoggedRequest.request_uid)
    ).limit(MAX_REQUESTS_COUNT)

    res_requests = []
    for request in requests:
        parameters = db.query(
            RequestParameters
        ).filter(
            RequestParameters.request_id == request.request_id,
            RequestParameters.is_in_use == True
        ).order_by(
            RequestParameters.parameter_name,
            RequestParameters.adding_dts
        ).limit(MAX_PARAMS_COUNT)

        request.parameters = parameters
        res_requests.append(request)

    dcd.requests = res_requests

    breadcrumbs = {
        "path": [
            (
                "/brief",
                "Brief"
            ),
            (
                "/brief/node/{}".format(dcn.dcn_uid),
                dcn.dcn_name
            )
        ],
        "current": dcd.dcd_name
    }

    params = get_page_template_values(
        {
            "user": bottle.request.get_user(),
            "device": dcd,
            "breadcrumbs": breadcrumbs,
            "max_params_count": MAX_PARAMS_COUNT,
            "max_requests_count": MAX_REQUESTS_COUNT
        },
        page_title="Device [{}]".format(dcd.dcd_name),
        page_header=dcd.dcd_name,
        page_description="device information [{}]".format(dcd.dcd_uid)
    )

    return template("brief/device.tpl", **params)
