import os

import bottle
from bottle import JSONPlugin
import bottle_sqlalchemy

from reqlog.support.config_support import get_config
from reqlog.support.jwt_plugin import JWTProviderPlugin
from reqlog.support.log_tools import init_logger
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from ujson import dumps as json_dumps


logger = init_logger()

Base = declarative_base()
db_plugin = None

application = bottle.Bottle(autojson=False)
application.logger = logger
application.install(JSONPlugin(json_dumps=lambda s: json_dumps(s, sort_keys=True, indent=4)))


def init_base_and_engine(logger, config):
    from reqlog.support.consts import SQLITE_IN_MEMORY_DB_PATH

    db_path = config.get("sqlitedb", "path")
    logger.info("db_path = '{}'".format(db_path))

    if db_path != SQLITE_IN_MEMORY_DB_PATH:
        db_path = os.path.abspath(db_path)
        recreate_db = not os.path.exists(db_path)
    else:
        recreate_db = True

    engine = sqlalchemy.create_engine("sqlite:///" + db_path, echo=False)

    return engine, recreate_db


class ImprovedSqlAlchemyPlugin(bottle_sqlalchemy.SQLAlchemyPlugin):
    def __init__(self, engine, metadata=None,
                 keyword="db", commit=True, create=False, use_kwargs=False, create_session=None):
        super().__init__(engine, metadata, keyword, commit, create, use_kwargs, create_session)

    def recreate_database(self):
        self.drop_database()
        self.create_all()

    def drop_database(self):
        self.metadata.drop_all(self.engine)

    def create_all(self):
        self.metadata.create_all(self.engine)

    def get_session(self):
        return self.create_session(bind=self.engine)


def recreate_database(plugin):
    logger.warning("force database recreation called")
    plugin.recreate_database()


def init_db_with_initial_data(plugin):
    from reqlog.support.db_init.db_init import init_database
    session = plugin.get_session()
    init_database(logger, session)
    session.commit()


def init_tempaltes_file_path(config, section, key_name):
    templates_root = config.get(section, key_name)
    res = os.path.normpath(os.path.abspath(templates_root))

    if not os.path.exists(res):
        msg = "root for template files does not exists. path = '{}'".format(templates_root)
        logger.error(msg)
        raise Exception(msg)

    if not os.path.isdir(res):
        msg = "root for template files is not a directory. path = '{}'".format(templates_root)
        logger.error(msg)
        raise Exception(msg)

    return res


def init_static_file_path(config, section, key_name):
    static_root = config.get(section, key_name)
    res = os.path.normpath(os.path.abspath(static_root))
    if not os.path.exists(res):
        msg = "root for static files does not exists. path = '{}'".format(static_root)
        logger.error(msg)
        raise Exception(msg)

    if not os.path.isdir(res):
        msg = "root for static files is not a directory. path = '{}'".format(static_root)
        logger.error(msg)
        raise Exception(msg)

    return res


def on_jwt_auth_failed():
    if bottle.request.get_header("client_type", "") != "json_api":
        return application.jwt_plugin.get_redirect_response_object("/login")

    return None


def on_auth_redirect(response):
    response.set_cookie(
        "client_type",
        "browser",
        path="/",
        secret=application.cookie_secret
    )

    return response


def setup_app(config=None, force_recreate_database=False, force_initialize_database=False):
    for plugin in application.plugins:
        if isinstance(plugin, ImprovedSqlAlchemyPlugin):
            logger.info("SQLAlchemy plugin already installed")

            if force_recreate_database:
                recreate_database(plugin)

            if force_initialize_database:
                init_db_with_initial_data(plugin)

            return

    for plugin in application.plugins:
        if ("keyword" in plugin.__dict__) and (plugin.keyword == "db"):
            return

    if config is None:
        config = get_config()

    application.config = config

    engine, recreate_db = init_base_and_engine(logger, config)

    db_plugin = ImprovedSqlAlchemyPlugin(
        engine,  # SQLAlchemy engine created with create_engine function.
        Base.metadata,  # SQLAlchemy metadata, required only if create=True.
        keyword="db",  # Keyword used to inject session database in a route (default "db").
        create=recreate_db,  # If it is true, execute `metadata.create_all(engine)` when plugin is applied (default False).
        commit=False,  # If it is true, plugin commit changes after route is executed (default True).
        use_kwargs=False  # If it is true and keyword is not defined, plugin uses **kwargs argument to inject session database (default False).
    )

    if force_recreate_database:
        recreate_database(db_plugin)

    if force_initialize_database:
        init_db_with_initial_data(db_plugin)

    application.install(db_plugin)

    application.static_files_path = init_static_file_path(config, "static", "root")
    bottle.TEMPLATE_PATH.insert(0, init_tempaltes_file_path(config, "templates", "root"))

    cookie_sign_secret = str(config.get("security", "cookie_sign_secret")).strip()
    cookie_sign_secret = cookie_sign_secret if len(cookie_sign_secret) > 0 else None

    from reqlog.support.jwt_backend.jwt_backend import JwtAuthBackend

    provider_plugin = JWTProviderPlugin(
        keyword="jwt",
        auth_endpoint="/auth/token",
        backend=JwtAuthBackend(),
        fields=("login", "password"),
        secret=config.get("security", "server_secret"),

        ttl=config.getint("security", "token_ttl_secs"),
        token_recreate_before=config.getint("security", "token_recreate_before_secs"),
        id_field="user_uid",

        add_cookie=True,
        cookie_secret=cookie_sign_secret,

        auth_redirect_rule=(lambda: True if bottle.request.params.get("client_type") == "browser" else False),
        auth_redirect_to="/cabinet",

        soft_authentication_keyword="is_authenticated",
        on_jwt_exception=on_jwt_auth_failed,
        on_auth_redirect=on_auth_redirect
    )

    application.install(provider_plugin)
    application.jwt_plugin = provider_plugin
    application.cookie_secret = cookie_sign_secret


from reqlog.dbschema import *  # noqa
from reqlog.api import *  # noqa
from reqlog.pages import *  # noqa

try:
    import uwsgidecorators

    uwsgidecorators.postfork(setup_app)
except ImportError:
    logger.info("NOT RUNNING ON UWSGI")
