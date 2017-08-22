import reqlog

from reqlog.support.config_support import get_dbmgt_commandline
from reqlog.support.db_init.db_init import gen_fake_requests_for_demo_user, init_database
from reqlog.support.db_shared import get_plugin


config, args = get_dbmgt_commandline()
reqlog.setup_app(config)


if args.drop_database:
    reqlog.logger.info("dropping all information")
    plugin = get_plugin(reqlog.application)
    assert plugin is not None
    plugin.drop_database()


if args.create_database:
    reqlog.logger.info("recreating tables in database")
    plugin = get_plugin(reqlog.application)
    assert plugin is not None
    plugin.create_all()


if args.init_database:
    reqlog.logger.info("initializing database with initial data")
    plugin = get_plugin(reqlog.application)
    assert plugin is not None
    session = plugin.get_session()
    init_database(reqlog.logger, session)

    session.commit()

if args.gen_test_requests:
    reqlog.logger.info("adding test (fake) requests for Demo user")
    plugin = get_plugin(reqlog.application)
    assert plugin is not None
    session = plugin.get_session()
    gen_fake_requests_for_demo_user(reqlog.logger, session)

    session.commit()


reqlog.logger.info("all operations complete")
