import bottle
from bottle import template
from reqlog.app import application
from reqlog.dbschema import DataCollectingDevice, DataCollectingNode
from reqlog.pages.pages_shared import get_page_template_values
from reqlog.support.jwt_plugin import jwt_auth_required


@application.route("/brief")
@jwt_auth_required
def page_brief_root(db):
    user = bottle.request.get_user()

    nodes = db.query(
        DataCollectingNode
    ).filter(
        DataCollectingNode.owner_id == user.user_id,
        DataCollectingNode.is_in_use == True
    ).order_by(
        DataCollectingNode.dcn_name
    ).all()

    breadcrumbs = {
        "path": [
        ],
        "current": "Brief"
    }

    avail_nodes = []
    for node in nodes:
        node.devices = db.query(
            DataCollectingDevice
        ).filter(
            DataCollectingDevice.dcn_id == node.dcn_id,
            DataCollectingDevice.is_in_use == True
        ).order_by(
            DataCollectingDevice.dcd_name
        ).all()
        avail_nodes.append(node)

    params = get_page_template_values(
        {
            "user": bottle.request.get_user(),
            "nodes": avail_nodes,
            "breadcrumbs": breadcrumbs,
        },
        page_title="Brief",
        page_header="Data collecting nodes",
        page_description="list of avail node"
    )

    return template("brief/root.tpl", **params)


@application.route("/brief/node/<node_uid>")
@jwt_auth_required
def page_node_information(db, node_uid):
    user = bottle.request.get_user()

    node = db.query(
        DataCollectingNode
    ).filter(
        DataCollectingNode.owner_id == user.user_id,
        DataCollectingNode.dcn_uid == node_uid,
        DataCollectingNode.is_in_use == True
    ).scalar()

    if node is None:
        bottle.abort(404)

    node.devices = db.query(
        DataCollectingDevice
    ).filter(
        DataCollectingDevice.dcn_id == node.dcn_id,
        DataCollectingDevice.is_in_use == True
    ).order_by(
        DataCollectingDevice.dcd_name
    ).all()

    breadcrumbs = {
        "path": [
            (
                "/brief",
                "Brief"
            )
        ],
        "current": node.dcn_name
    }

    params = get_page_template_values(
        {
            "user": bottle.request.get_user(),
            "node": node,
            "breadcrumbs": breadcrumbs,
        },
        page_title="Node [{}]".format(node.dcn_name),
        page_header=node.dcn_name,
        page_description="node information"
    )

    return template("brief/node.tpl", **params)
