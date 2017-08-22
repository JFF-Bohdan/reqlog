import datetime

from reqlog.app import Base
import sqlalchemy
from sqlalchemy import BigInteger, Column, DateTime, Integer, Sequence


class LinkUserToScope(Base):
    __tablename__ = "link_users_to_scopes"

    # TODO: add index for user
    # TODO: add index for user & scope

    row_id = Column(BigInteger().with_variant(Integer, "sqlite"), Sequence("gen_link_users_to_scopes"), primary_key=True)

    user_id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        sqlalchemy.ForeignKey("sys_users.user_id"),
        nullable=False
    )

    scope_id = Column(
        Integer,
        sqlalchemy.ForeignKey("dc_available_scopes.scope_id"),
        nullable=False
    )

    adding_dts = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)

    def __init__(self):
        pass
