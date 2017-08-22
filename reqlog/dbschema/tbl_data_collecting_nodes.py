import datetime

from reqlog.app import Base
import sqlalchemy
from sqlalchemy import BigInteger, Boolean, Column, DateTime, Integer, Sequence, String, Text

from .shared import get_string_ksuid


class DataCollectingNode(Base):
    __tablename__ = "data_collecting_nodes"

    # TODO: uid must be uniq
    # TODO: add index for uid

    dcn_id = Column(BigInteger().with_variant(Integer, "sqlite"), Sequence("gen_data_collecting_nodes"), primary_key=True)

    dcn_name = Column(String(255), nullable=False)

    dcn_uid = Column(String(255), nullable=False, default=get_string_ksuid)

    adding_dts = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    update_dts = Column(DateTime, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    last_activity_dts = Column(DateTime, nullable=True)

    owner_id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        sqlalchemy.ForeignKey("sys_users.user_id"),
        nullable=False
    )

    description = Column(Text, nullable=True, default="")
    is_in_use = Column(Boolean, nullable=False, default=True)

    def __init__(self):
        pass
