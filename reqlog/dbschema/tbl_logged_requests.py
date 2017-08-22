import datetime

from reqlog.app import Base
import sqlalchemy
from sqlalchemy import BigInteger, Boolean, Column, DateTime, Integer, Sequence, String

from .shared import get_string_ksuid


class LoggedRequest(Base):
    __tablename__ = "logged_requests"

    # TODO: add index for uid
    # TODO: add uniq for uid
    # TODO: add index for dcd_id

    request_id = Column(BigInteger().with_variant(Integer, "sqlite"), Sequence("request_id"), primary_key=True)

    request_uid = Column(String(255), nullable=False, default=get_string_ksuid)
    adding_dts = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    method = Column(String(128), nullable=False)

    dcd_id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        sqlalchemy.ForeignKey("data_collecting_device.dcd_id"),
        nullable=False
    )

    is_in_use = Column(Boolean, nullable=False, default=True)

    def __init__(self):
        pass
