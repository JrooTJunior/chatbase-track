from typing import Optional

from aiogram import types

from chatbase_track import ChatBase
from chatbase_track.backend.aiohttp import AiohttpBackend
from chatbase_track.backend.base import AbstractBackend
from chatbase_track.types.message_type import MessageType


class AiogramChatBase(ChatBase):
    def __init__(
        self,
        api_key: str,
        backend: AbstractBackend = None,
        version: Optional[str] = None,
    ):
        if backend is None:
            backend = AiohttpBackend()

        super().__init__(
            api_key=api_key, platform="Telegram", backend=backend, version=version
        )

    def from_message(
        self,
        message: types.Message,
        intent: Optional[str] = None,
        not_handled: Optional[bool] = None,
        version: Optional[str] = None,
        session_id: Optional[str] = None,
        message_type: MessageType = MessageType.USER,
    ):
        event = self.message(
            user_id=str(message.from_user.id),
            message=message.text or message.caption or f"[{message.content_type}]",
            time_stamp=message.date,
            intent=intent,
            not_handled=not_handled,
            version=version,
            session_id=session_id,
            message_type=message_type,
        )
        return self(event)

    def from_callback_query(
        self,
        query: types.CallbackQuery,
        intent: Optional[str] = None,
        not_handled: Optional[bool] = None,
        version: Optional[str] = None,
        session_id: Optional[str] = None,
        message_type: MessageType = MessageType.USER,
    ):
        event = self.message(
            user_id=query.from_user.id,
            message=query.data,
            intent=intent,
            not_handled=not_handled,
            version=version,
            session_id=session_id,
            message_type=message_type,
        )
        return self(event)
