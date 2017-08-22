import datetime

from reqlog.app import Base
import sqlalchemy
from sqlalchemy import BigInteger, Boolean, Column, DateTime, Integer, Sequence, String, Text

from .shared import get_base62_ksuid, get_string_ksuid


class DataCollectingDevice(Base):
    __tablename__ = "data_collecting_device"

    # TODO: add than token must be uniq
    # TODO: add that uid must be uniq

    dcd_id = Column(BigInteger().with_variant(Integer, "sqlite"), Sequence("gen_data_collecting_device"), primary_key=True)

    dcn_id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        sqlalchemy.ForeignKey("data_collecting_nodes.dcn_id"),
        nullable=False
    )

    dcd_uid = Column(String(255), nullable=False, default=get_string_ksuid)

    write_token = Column(String(255), nullable=True, default=get_base62_ksuid)
    read_token = Column(String(255), nullable=True)

    dcd_name = Column(String(255), nullable=False)

    adding_dts = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    update_dts = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    last_activity = Column(DateTime, nullable=True)

    description = Column(Text, nullable=True, default="")
    is_in_use = Column(Boolean, nullable=False, default=True)

    def __init__(self):
        pass
