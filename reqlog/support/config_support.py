import argparse
import configparser
import logging


def get_config():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        metavar="FILE",
        help="use FILE as configuration file")
    args = parser.parse_args()

    config = configparser.RawConfigParser()

    try:
        config.read(args.config)
    except:  # pragma: no coverage
        logging.error("Config was not found")

    return config


def get_dbmgt_commandline():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        metavar="FILE",
        help="use FILE as configuration file"
    )

    parser.add_argument(
        "--drop_database",
        action="store_true",
        help="drop all tables in database"
    )

    parser.add_argument(
        "--create_database",
        action="store_true",
        help="create all tables in database"
    )

    parser.add_argument(
        "--init_database",
        action="store_true",
        help="initialize database with initial data"
    )

    parser.add_argument(
        "--gen_test_requests",
        action="store_true",
        help="generate test requests for Demo user"
    )

    args = parser.parse_args()

    config = configparser.RawConfigParser()

    try:
        config.read(args.config)
    except:  # pragma: no coverage
        logging.error("Config was not found")

    return config, args
