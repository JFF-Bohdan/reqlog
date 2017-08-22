import bottle
from bottle import template
from reqlog.app import application
from reqlog.dbschema import DataCollectingDevice, DataCollectingNode, LoggedRequest, RequestParameters
from reqlog.pages.pages_shared import get_page_template_values, MAX_PARAMS_COUNT
from reqlog.support.datatablessupport import DataTablesBottleRequestAdapter, DataTablesParser, DataTablesResponse
from reqlog.support.jwt_plugin import jwt_auth_required
import sqlalchemy
import sqlalchemy.sql.functions as funcs


@application.route("/reports/all_requests")
@jwt_auth_required
def page_reports_all_requests():
    breadcrumbs = {
        "path": [
        ],
        "current": "Reports - all requests"
    }

    params = get_page_template_values(
        {
            "user": bottle.request.get_user(),
            "breadcrumbs": breadcrumbs
        },
        page_title="Reports all requests",
        page_header="All requests",
        page_description="all requests list"
    )

    return template("reports/all_requests.tpl", **params)


def get_all_devices_for_user_query(db, user_id):
    return db.query(
        DataCollectingDevice.dcd_id
    ).select_from(
        DataCollectingNode
    ).filter(
        DataCollectingNode.owner_id == user_id,
        DataCollectingNode.is_in_use == True
    ).join(
        DataCollectingDevice,
        DataCollectingNode.dcn_id == DataCollectingDevice.dcd_id
    ).filter(
        DataCollectingDevice.is_in_use == True
    )


def map_db_data_to_request(db, data, columns_list):
    res = []

    for request, dcd_uid, dcd_name, dcn_name, params_count in data:
        res_item = {}
        if "added_at" in columns_list:
            res_item["added_at"] = request.adding_dts.isoformat()

        if "uid" in columns_list:
            res_item["uid"] = request.request_uid

        if "method" in columns_list:
            res_item["method"] = request.method

        if "params_brief_4" in columns_list:
            parameters = db.query(
                RequestParameters
            ).filter(
                RequestParameters.request_id == request.request_id,
                RequestParameters.is_in_use == True
            ).order_by(
                RequestParameters.parameter_name,
                RequestParameters.adding_dts
            ).limit(MAX_PARAMS_COUNT)

            res_item["params_brief_4"] = [
                {
                    "name": parameter.parameter_name,
                    "value": parameter.parameter_value
                } for parameter in parameters
            ]

        if "dcd_name" in columns_list:
            res_item["dcd_name"] = dcd_name

        if "dcn_name" in columns_list:
            res_item["dcn_name"] = dcn_name

        if "params_count" in columns_list:
            res_item["params_count"] = params_count

        if "event_details_href_data" in columns_list:
            res_item["event_details_href_data"] = {
                "dcd_uid": dcd_uid,
                "event_uid": request.request_uid
            }

        res.append(res_item)

    return res


@application.route("/api/reports/all_requests/datatable", method=["post"])
@jwt_auth_required
def api_reports_all_requests_datatable(db):
    user = bottle.request.get_user()

    datatables_request = DataTablesParser.parse(bottle.request, DataTablesBottleRequestAdapter, application.logger)
    if datatables_request is None:
        bottle.abort(404)

    user_devices = get_all_devices_for_user_query(db, user.user_id).subquery()

    parameters_count_stmt = db.query(
        funcs.count()
    ).select_from(
        RequestParameters
    ).filter(
        RequestParameters.request_id == LoggedRequest.request_id,
        RequestParameters.is_in_use == True
    )

    query = db.query(
        LoggedRequest,
        DataCollectingDevice.dcd_uid,
        DataCollectingDevice.dcd_name,
        DataCollectingNode.dcn_name,
        parameters_count_stmt.label("cnt")
    ).filter(
        LoggedRequest.dcd_id.in_(user_devices),
        LoggedRequest.is_in_use == True
    ).join(
        DataCollectingDevice,
        LoggedRequest.dcd_id == DataCollectingDevice.dcd_id
    ).join(
        DataCollectingNode,
        DataCollectingDevice.dcn_id == DataCollectingNode.dcn_id
    )

    total_records_count = query.count()

    filter_value = datatables_request.filter_by()
    if filter_value is not None:
        query = query.filter(
            sqlalchemy.or_(
                LoggedRequest.request_uid.ilike(filter_value),
                DataCollectingDevice.dcd_name.ilike(filter_value),
                DataCollectingNode.dcn_name.ilike(filter_value),
            )
        )

    filtered_records_count = query.count()
    query.order_by(LoggedRequest.adding_dts)

    if (datatables_request.length is not None) and (datatables_request.length > 0):
        query = query.limit(datatables_request.length)

    if (datatables_request.start is not None) and (datatables_request.start > 0):
        query = query.offset(datatables_request.start)

    data = query.all()

    all_columns = datatables_request.all_columns_data()
    data = map_db_data_to_request(db, data, all_columns)

    return DataTablesResponse.produce_result(data, datatables_request.draw, filtered_records_count, total_records_count)
