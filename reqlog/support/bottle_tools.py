def inspect_routes(app):
    for route in app.routes:
        if "mountpoint" in route.config:
            prefix = route.config["mountpoint"]["prefix"]
            subapp = route.config["mountpoint"]["target"]

            for prefixes, route in inspect_routes(subapp):
                yield [prefix] + prefixes, route
        else:
            yield [], route


def log_all_routes(logger, app):
    routes = []
    for prefixes, route in inspect_routes(app):
        abs_prefix = "/".join(part for p in prefixes for part in p.split("/"))
        routes.append("{} {} {} {}".format(abs_prefix, route.rule, route.method, route.callback))

    logger.info("all available routes:\n{}".format("\n".join(routes)))
