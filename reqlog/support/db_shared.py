from reqlog.app import ImprovedSqlAlchemyPlugin


def get_plugin(app):
    for plugin in app.plugins:
        if isinstance(plugin, ImprovedSqlAlchemyPlugin):
            return plugin

    return None
