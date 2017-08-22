import datetime
import random

import ksuid
from reqlog.dbschema import DataCollectingDevice, DataCollectingNode, DcAvailableScope, LinkUserToScope, LoggedRequest, RequestParameters, User
from reqlog.support.shared import create_hash

from .initialization_consts import ADMIN_USER_EMAIL, ADMIN_USER_LOGIN, ADMIN_USER_PASSWORD, \
    DEMO_CONFIGURATION, DEMO_USER_EMAIL, DEMO_USER_LOGIN, DEMO_USER_NAME, DEMO_USER_PASSWORD, \
    DEMO_USER_UID, POSSIBLE_PARAMS_VALUE, POSSIBLE_TEST_PARAMS_NAME


def init_database(logger, session):
    add_initial_users(session)
    session.flush()

    add_dictionaries_data(session)
    session.flush()

    give_all_scopes_to_admin(session)
    session.flush()

    dcns_qty, dcds_qty = add_demo_nodes_and_devices(session)
    logger.info("added DCNs count - {}".format(dcns_qty))
    logger.info("added DCDs count - {}".format(dcds_qty))

    session.flush()

    session.commit()


def add_initial_users(session):
    user = User()

    user.password_hash, user.password_salt = create_hash(ADMIN_USER_PASSWORD)
    user.user_name = ADMIN_USER_LOGIN
    user.user_email = ADMIN_USER_EMAIL
    user.user_login = ADMIN_USER_LOGIN

    session.add(user)

    user = User()

    user.password_hash, user.password_salt = create_hash(DEMO_USER_PASSWORD)
    user.user_name = DEMO_USER_NAME
    user.user_email = DEMO_USER_EMAIL
    user.user_login = DEMO_USER_LOGIN
    user.user_uid = DEMO_USER_UID

    session.add(user)


def add_demo_nodes_and_devices(session):
    user = session.query(
        User
    ).filter(
        User.user_login == DEMO_USER_LOGIN
    ).scalar()

    assert user is not None

    dcns_qty = 0
    dcds_qty = 0
    for dcn_item in DEMO_CONFIGURATION:
        node = DataCollectingNode()

        node.dcn_name = dcn_item["dcn_name"]
        node.dcn_uid = str(ksuid.ksuid())
        node.owner_id = user.user_id
        node.description = dcn_item["dcn_description"]

        session.add(node)
        session.flush()

        dcns_qty += 1

        for dcd_item in dcn_item["devices"]:
            dcd = DataCollectingDevice()

            dcd.dcn_id = node.dcn_id
            dcd.dcd_uid = str(ksuid.ksuid())

            dcd.write_token = dcd_item["write_token"]
            dcd.read_token = dcd_item["read_token"]

            dcd.dcd_name = dcd_item["dcd_name"]
            dcd.description = dcd_item["dcd_description"]

            session.add(dcd)
            session.flush()

            dcds_qty += 1

    return dcns_qty, dcds_qty


def add_dictionaries_data(session):
    for (scope_code, scope_name) in DcAvailableScope.get_all_possible_scopes():
        item = DcAvailableScope()

        item.scope_code = scope_code
        item.scope_name = scope_name
        item.scope_description = scope_name

        session.add(item)


def give_all_scopes_to_admin(session):
    user_id = session.query(
        User.user_id
    ).filter(
        User.user_login == ADMIN_USER_LOGIN
    ).scalar()

    assert user_id is not None

    data = session.query(
        DcAvailableScope.scope_id
    ).filter(
        DcAvailableScope.is_in_use == True
    ).all()

    for (scope_id, ) in data:
        link = LinkUserToScope()

        link.user_id = user_id
        link.scope_id = scope_id

        session.add(link)


def gen_fake_requests_for_demo_user(logger, session):
    random.seed()

    user = session.query(
        User
    ).filter(
        User.user_login == DEMO_USER_LOGIN
    ).scalar()

    assert user is not None

    dcns = session.query(
        DataCollectingNode.dcn_id
    ).filter(
        DataCollectingNode.owner_id == user.user_id
    ).subquery()

    avail_dcd_list = session.query(
        DataCollectingDevice.dcd_id,
        DataCollectingDevice.dcn_id
    ).filter(
        DataCollectingDevice.dcn_id.in_(dcns)
    ).all()

    max_requests_count = random.randint(100, 1000)

    logger.info("devices count in Demo organization - {}".format(len(avail_dcd_list)))

    params_to_add = []
    dcn_last_activity_dts = {}
    dcd_last_activity_dts = {}
    for _ in range(max_requests_count):
        req = LoggedRequest()

        req.method = random.choice(["get", "post"])

        dcd_info = random.choice(avail_dcd_list)

        req.dcd_id = dcd_info[0]
        dcn_last_activity_dts[dcd_info[1]] = datetime.datetime.utcnow()
        dcd_last_activity_dts[dcd_info[0]] = datetime.datetime.utcnow()

        session.add(req)
        session.flush()

        for _ in range(random.randint(3, 10)):
            param = RequestParameters()
            param.request_id = req.request_id

            param.parameter_name = random.choice(POSSIBLE_TEST_PARAMS_NAME)
            v = random.choice(POSSIBLE_PARAMS_VALUE)
            if callable(v):
                v = v()
            param.parameter_value = v

            params_to_add.append(param)

    session.bulk_save_objects(params_to_add)
    session.flush()

    for dcn_id in dcn_last_activity_dts.keys():
        session.query(
            DataCollectingNode
        ).filter(
            DataCollectingNode.dcn_id == dcn_id
        ).update(
            {
                DataCollectingNode.last_activity_dts: dcn_last_activity_dts[dcn_id]
            },
            synchronize_session=False
        )

    for dcd_id in dcd_last_activity_dts.keys():
        session.query(
            DataCollectingDevice
        ).filter(
            DataCollectingDevice.dcd_id == dcd_id
        ).update(
            {
                DataCollectingDevice.last_activity: dcd_last_activity_dts[dcn_id]
            },
            synchronize_session=False
        )

    logger.info("added requests count - {}".format(max_requests_count))
    logger.info("added params count   - {}".format(len(params_to_add)))
