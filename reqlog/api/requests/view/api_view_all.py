import bottle
from reqlog.app import application
from reqlog.dbschema import DataCollectingDevice, LoggedRequest, RequestParameters


@application.get("/view_all")
def api_get_all_requests(db):
    r = bottle.request

    access_token = r.headers.get("access_token", None)
    if access_token is None:
        access_token = r.params.get("t", None)

    if access_token is None:
        bottle.abort(401)  # Unauthorized

    dcd_id = db.query(
        DataCollectingDevice.dcd_id
    ).filter(
        DataCollectingDevice.read_token == access_token
    ).scalar()
    if dcd_id is None:
        bottle.abort(403)  # Forbidden

    db_data = db.query(
        LoggedRequest
    ).filter(
        LoggedRequest.dcd_id == dcd_id,
        LoggedRequest.is_in_use == True
    ).order_by(
        LoggedRequest.adding_dts
    ).all()

    json_items = []
    for item in db_data:
        json_item = {
            "request_id": item.request_id,
            "request_uid": item.request_uid,
            "adding_dts": str(item.adding_dts),
            "method": item.method
        }

        params = db.query(
            RequestParameters
        ).filter(
            RequestParameters.request_id == item.request_id
        ).all()

        json_parameters = []
        for parameter in params:
            json_parameters.append(
                {
                    "name": parameter.parameter_name,
                    "value": parameter.parameter_value
                }
            )

        json_item["parameters"] = json_parameters
        json_items.append(json_item)

    data = {
        "data": json_items
    }
    return data
