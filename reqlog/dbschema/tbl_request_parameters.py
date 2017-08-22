import datetime

from reqlog.app import Base
import sqlalchemy
from sqlalchemy import BigInteger, Boolean, Column, DateTime, Integer, Sequence, Text


class RequestParameters(Base):
    __tablename__ = "request_parameters"

    # TODO: add index for request id

    parameter_id = Column(BigInteger().with_variant(Integer, "sqlite"), Sequence("gen_request_parameters"), primary_key=True)

    request_id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        sqlalchemy.ForeignKey("logged_requests.request_id"),
        nullable=False
    )

    parameter_name = Column(Text, nullable=False)
    parameter_value = Column(Text, nullable=True)
    adding_dts = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    is_in_use = Column(Boolean, nullable=False, default=True)

    def __init__(self):
        pass
