import configparser

import reqlog
from reqlog.support.consts import SQLITE_IN_MEMORY_DB_PATH
import webtest


def setup_test_config():
    config = configparser.RawConfigParser()

    config.add_section("main")
    config.set("main", "host", "0.0.0.0")
    config.set("main", "port", "9000")
    config.set("main", "debug", "true")
    config.set("main", "reloader", "true")
    config.set("main", "reloader_interval", "3")

    config.add_section("db_connection")
    config.set("db_connection", "connection_string", SQLITE_IN_MEMORY_DB_PATH)
    config.set("db_connection", "produce_echo", "false")

    config.add_section("static")
    config.set("static", "root", "./static")

    config.add_section("templates")
    config.set("templates", "root", "./reqlog/templates")

    config.add_section("security")
    config.set("security", "server_secret", "123")
    config.set("security", "cookie_sign_secret", "")
    config.set("security", "token_ttl_secs", "300")
    config.set("security", "token_recreate_before_secs", "100")

    config.add_section("branding")
    config.set("branding", "solution_name", "ReqLog")
    config.set("branding", "instance_owner_name", "ACME corp")
    return config


def setup_application(force_recreate_database=True, force_initialize_database=True):
    config = setup_test_config()
    reqlog.setup_app(config, force_recreate_database=force_recreate_database, force_initialize_database=force_initialize_database)

    return webtest.TestApp(reqlog.application)
