import abc
import logging
from typing import Dict, Any, Tuple

from chatbase_track.types.message import Message
from chatbase_track.types.response import MessagesResponse

log = logging.getLogger(__name__)

API_URL = "https://chatbase.com/api"


class AbstractBackend(abc.ABC):
    def __init__(self, api_url: str = API_URL):
        self.api_url = api_url

    @classmethod
    def _render_message(cls, message: Message) -> Dict[str, Any]:
        log.info(
            "Track event %r from user %r (handled=%s)",
            message.intent or message.message,
            message.user_id,
            not message.not_handled,
        )
        return message.render_message()

    def process_messages(self, *messages: Message):
        log.debug("Track events: %s", messages)
        return self.make_request(
            endpoint=f"{self.api_url}/messages",
            payload={
                "messages": [self._render_message(message) for message in messages]
            },
            messages=messages,
        )

    def build_response(
        self, data: Dict[str, Any], messages: Tuple[Message]
    ) -> MessagesResponse:
        response = MessagesResponse(**data)
        log.debug("Tracked events %s", response)
        if not response.all_succeeded:
            for resp, message in zip(response.responses, messages):
                if resp.is_error:
                    log.error("Failed to track message %r: %s", resp.error, message)
        return response

    @abc.abstractmethod
    def make_request(
        self, endpoint: str, payload: Dict[str, Any], messages: Tuple[Message]
    ):
        pass

    @abc.abstractmethod
    def close(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
