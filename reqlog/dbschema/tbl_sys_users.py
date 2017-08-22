import datetime


from reqlog.app import Base
from sqlalchemy import BigInteger, Boolean, Column, DateTime, Integer, Sequence, String


from .shared import get_string_ksuid


class User(Base):
    __tablename__ = "sys_users"

    # TODO: add uniq for email
    # TODO: add uniq for uid
    # TODO: add index for login

    # TODO: add index for uid
    # TODO: add index for email
    # TODO: add index for login

    user_id = Column(BigInteger().with_variant(Integer, "sqlite"), Sequence("gen_sys_users"), primary_key=True)

    user_uid = Column(String(255), nullable=False, default=get_string_ksuid)

    password_salt = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)

    user_name = Column(String(255), nullable=False, default=get_string_ksuid)
    user_email = Column(String(255), nullable=False, default=get_string_ksuid)
    user_login = Column(String(255), nullable=False, default=get_string_ksuid)

    adding_dts = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    update_dts = Column(DateTime, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    is_in_use = Column(Boolean, nullable=False, default=True)

    def __init__(self):
        pass
