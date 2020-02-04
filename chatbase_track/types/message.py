import datetime
from typing import Any, Dict, Optional, Union

from chatbase_track.types.base import Base
from chatbase_track.types.message_type import MessageType


class Message(Base):
    api_key: str
    type: MessageType
    user_id: str
    time_stamp: Union[int, datetime.datetime]
    platform: str
    message: Optional[str] = None
    intent: Optional[str] = None
    not_handled: Optional[bool] = None
    version: Optional[str] = None
    session_id: Optional[str] = None

    def render_message(self) -> Dict[str, Any]:
        payload = self.dict(exclude_none=True)
        if isinstance(payload["time_stamp"], datetime.datetime):
            payload["time_stamp"] = int(payload["time_stamp"].timestamp() * 1e3)
        return payload
