import bottle
from bottle import template
from reqlog.app import application
from reqlog.dbschema import DataCollectingDevice, DataCollectingNode, LoggedRequest
from reqlog.support.jwt_plugin import jwt_auth_required

from .pages_shared import get_page_template_values


@application.route("/cabinet")
@jwt_auth_required
def api_cabinet(db):
    user = bottle.request.get_user()

    nodes_query = db.query(
        DataCollectingNode.dcn_id
    ).filter(
        DataCollectingNode.owner_id == user.user_id,
        DataCollectingNode.is_in_use == True
    )

    devices_query = db.query(
        DataCollectingDevice.dcd_id
    ).filter(
        DataCollectingDevice.dcn_id.in_(nodes_query.subquery()),
        DataCollectingDevice.is_in_use == True
    )

    request_query = db.query(
        LoggedRequest.request_id
    ).filter(
        LoggedRequest.dcd_id.in_(devices_query.subquery()),
        LoggedRequest.is_in_use == True
    )

    total_nodes_count = nodes_query.count()
    total_devices_count = devices_query.count()
    total_requests_count = request_query.count()

    params = get_page_template_values(
        {

            "user": bottle.request.get_user(),
            "total_requests_count": total_requests_count,
            "total_devices_count": total_devices_count,
            "total_nodes_count": total_nodes_count
        },
        page_title="Cabinet"
    )

    return template("cabinet.tpl", **params)
