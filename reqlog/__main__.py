import os
import sys

import bottle

base_module_dir = os.path.dirname(sys.modules[__name__].__file__)

try:
    import reqlog  # noqa: F401 # need to check import possibility
except ImportError:
    path = base_module_dir
    path = os.path.join(path, "..")
    sys.path.insert(0, path)

    import reqlog  # noqa # testing that we able to import package

from reqlog.support.bottle_tools import log_all_routes  # noqa

config = reqlog.get_config()
reqlog.setup_app(config)

log_all_routes(reqlog.logger, reqlog.application)

bottle.run(
    app=reqlog.application,
    host=config.get("main", "host"),
    port=config.getint("main", "port"),
    debug=config.getboolean("main", "debug"),
    reloader=config.getboolean("main", "reloader"),
    interval=config.getint("main", "reloader_interval")
)
