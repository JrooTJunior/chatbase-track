import datetime
from typing import Optional

from chatbase_track.backend.base import AbstractBackend
from chatbase_track.backend.requests import RequestsBackend
from chatbase_track.types.message import Message
from chatbase_track.types.message_type import MessageType


class ChatBase:
    def __init__(
        self,
        api_key: str,
        platform: str,
        backend: AbstractBackend = None,
        version: Optional[str] = None,
    ):
        if backend is None:
            backend = RequestsBackend()

        self.api_key = api_key

        self.platform = platform
        self.version = version
        self.backend = backend

    def message(
        self,
        user_id: str,
        message: Optional[str] = None,
        intent: Optional[str] = None,
        not_handled: Optional[bool] = None,
        version: Optional[str] = None,
        session_id: Optional[str] = None,
        message_type: MessageType = MessageType.USER,
        time_stamp: Optional[datetime.datetime] = None,
    ):
        message = Message(
            api_key=self.api_key,
            type=message_type,
            user_id=user_id,
            time_stamp=time_stamp or datetime.datetime.now(),
            platform=self.platform,
            message=message,
            intent=intent,
            not_handled=not_handled,
            version=version or self.version,
            session_id=session_id,
        )
        return message

    def close(self):
        return self.backend.close()

    def track(self, *messages: Message):
        return self.backend.process_messages(*messages)

    def __call__(self, *messages: Message):
        return self.track(*messages)
