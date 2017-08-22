import datetime

from reqlog.app import Base
from sqlalchemy import Boolean, Column, DateTime, Integer, Sequence, String, Text


class DcAvailableScope(Base):
    __tablename__ = "dc_available_scopes"

    # TODO: add unic for scope code name
    # TODO: add index for scope code name

    SCOPE_VIEW_ALL_USERS = "view_all_users"
    SCOPE_EDIT_ALL_USERS = "edit_all_users"

    scope_id = Column(Integer, Sequence("gen_dc_available_scopes"), primary_key=True)
    scope_code = Column(String(255), nullable=False)
    scope_name = Column(String(512), nullable=False, default="")
    scope_description = Column(Text, nullable=False, default="")
    adding_dts = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    is_in_use = Column(Boolean, nullable=False, default=True)

    def __init__(self):
        pass

    @staticmethod
    def get_all_possible_scopes():
        return [
            (DcAvailableScope.SCOPE_VIEW_ALL_USERS, "View all users"),
            (DcAvailableScope.SCOPE_EDIT_ALL_USERS, "Edit all users")
        ]
