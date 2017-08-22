import datetime

from reqlog.support.jwt_plugin.backends import BaseAuthBackend


class JwtAuthBackend(BaseAuthBackend):
    """Implementing an auth backend class with at least two methods.
    """
    def __init__(self):
        super().__init__()

    def authenticate_user(self, login, password):
        from reqlog.app import application
        from reqlog.dbschema import User
        from reqlog.support.db_shared import get_plugin
        from reqlog.support.shared import create_hash

        plugin = get_plugin(application)
        session = plugin.get_session()

        user = session.query(
            User
        ).filter(
            User.user_login == login
        ).scalar()

        if user is None:
            return None

        calculated_hash, _ = create_hash(password, user.password_salt)
        if user.password_hash != calculated_hash:
            return None

        return {
            "user_uid": user.user_uid,
            "scope": "foo bar bizz bazz",
            "genat": str(datetime.datetime.utcnow().isoformat())
        }

    def get_user(self, user_id):
        """Retrieve User By ID.

        Returns:
            A dict representing User Record or None.
        """

        from reqlog.app import application
        from reqlog.dbschema import User
        from reqlog.support.db_shared import get_plugin

        plugin = get_plugin(application)
        session = plugin.get_session()

        user = session.query(
            User
        ).filter(
            User.user_uid == user_id
        ).scalar()

        if user is None:
            return None

        return user
