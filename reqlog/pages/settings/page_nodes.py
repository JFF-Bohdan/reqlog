import datetime

import bottle
from bottle import template
from reqlog.app import application
from reqlog.dbschema import DataCollectingDevice, DataCollectingNode
from reqlog.pages.pages_shared import get_page_template_values
from reqlog.support.jwt_plugin import jwt_auth_required


@application.route("/settings/nodes")
@jwt_auth_required
def page_settings_nodes(db):
    user = bottle.request.get_user()

    nodes = db.query(
        DataCollectingNode
    ).filter(
        DataCollectingNode.owner_id == user.user_id,
        DataCollectingNode.is_in_use == True
    ).order_by(
        DataCollectingNode.dcn_name
    ).all()

    res_nodes = []
    for node in nodes:
        node.devices_count = db.query(
            DataCollectingDevice
        ).filter(
            DataCollectingDevice.dcn_id == node.dcn_id,
            DataCollectingDevice.is_in_use == True
        ).count()

        res_nodes.append(node)

    breadcrumbs = {
        "path": [

        ],
        "current": "Settings nodes"
    }

    params = get_page_template_values(
        {
            "user": bottle.request.get_user(),
            "nodes": res_nodes,
            "breadcrumbs": breadcrumbs
        },
        page_title="Settings nodes",
        page_header="Settings/Nodes",
        page_description="nodes list"
    )

    return template("settings/settings_nodes_list.tpl", **params)


@application.route("/settings/node/<node_uid>", method=["get", "post"])
@jwt_auth_required
def page_settings_for_node(db, node_uid):
    user = bottle.request.get_user()

    node = db.query(
        DataCollectingNode
    ).filter(
        DataCollectingNode.dcn_uid == node_uid,
        DataCollectingNode.owner_id == user.user_id,
        DataCollectingNode.is_in_use == True
    ).scalar()

    if node is None:
        bottle.abort(404)

    if bottle.request.method == "POST":
        node_name = bottle.request.forms.node_name
        # node_uid = bottle.request.params.get("node_uid")
        node_description = bottle.request.forms.node_description

        node.dcn_name = node_name
        node.description = str(node_description).strip()
        node.update_dts = datetime.datetime.utcnow()

        db.flush()
        db.commit()

        bottle.redirect("/settings/nodes")

    breadcrumbs = {
        "path": [
            (
                "/settings/nodes",
                "Settings-Nodes"
            )
        ],
        "current": node.dcn_name
    }

    params = get_page_template_values(
        {
            "user": bottle.request.get_user(),
            "node": node,
            "breadcrumbs": breadcrumbs
        },
        page_title="Settings/{}".format(node.dcn_name),
        page_header="{}".format(node.dcn_name),
        page_description="Settings for node ({})".format(node.dcn_uid)
    )

    return template("settings/settings_node.tpl", **params)
