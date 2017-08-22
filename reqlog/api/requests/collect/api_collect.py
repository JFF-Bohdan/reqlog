import datetime

import bottle

from reqlog.app import application
from reqlog.dbschema import DataCollectingDevice, DataCollectingNode, LoggedRequest, RequestParameters


@application.route("/collect", method="ANY")
def api_collect(db):
    r = bottle.request

    is_token_loaded_from_params = False
    access_token = r.headers.get("access_token", None)
    if access_token is None:
        is_token_loaded_from_params = True
        access_token = r.params.get("t", None)

    if access_token is None:
        bottle.abort(401)  # Unauthorized

    dcd = db.query(
        DataCollectingDevice
    ).filter(
        DataCollectingDevice.write_token == access_token,
        DataCollectingDevice.is_in_use == True
    ).scalar()

    if dcd is None:
        bottle.abort(403)  # Forbidden

    logged_request = LoggedRequest()

    logged_request.method = r.method
    logged_request.dcd_id = dcd.dcd_id
    dcd.last_activity = datetime.datetime.utcnow()
    db.add(logged_request)
    db.flush()

    db.query(
        DataCollectingNode
    ).filter(
        DataCollectingNode.dcn_id == dcd.dcn_id
    ).update(
        {
            DataCollectingNode.last_activity_dts : datetime.datetime.utcnow()
        },
        synchronize_session=False
    )

    tracked_params = []
    for k, v in r.params.items():
        if is_token_loaded_from_params and (k == "t"):
            continue

        request_parameter = RequestParameters()
        request_parameter.request_id = logged_request.request_id
        request_parameter.parameter_name = k
        request_parameter.parameter_value = v

        db.add(request_parameter)
        tracked_params.append(request_parameter)

    db.commit()

    return {
        "method": r.method,
        "dcd_id": dcd.dcd_id,
        "request" : {
            "id": logged_request.request_id,
            "uid": logged_request.request_uid,
            "params": {item.parameter_name: item.parameter_value for item in tracked_params}
        }
    }
