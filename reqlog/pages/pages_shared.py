import datetime

from reqlog.app import application
from reqlog.version import __human_readable_app_name__


MAX_REQUESTS_COUNT = 10
MAX_PARAMS_COUNT = 4


def get_page_template_values(params, page_title=None, page_header=None, page_description=None):
    res = {
        "app_name": __human_readable_app_name__,
        "owned_by_company_name": application.config.get("branding", "instance_owner_name"),
        "current_year": datetime.datetime.utcnow().year,
        "page_title": page_title,
        "page_header": page_header,
        "page_description": page_description
    }

    for key in params.keys():
        res[key] = params[key]

    return res


def current_year():
    from datetime import datetime
    return datetime.utcnow().year
