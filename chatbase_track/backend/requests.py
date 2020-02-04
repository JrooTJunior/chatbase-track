import logging
from concurrent.futures.thread import ThreadPoolExecutor
from typing import Dict, Any, Optional, Tuple

try:
    import requests
except ImportError:
    raise ImportError(
        "`requests` is not installer. You can install it by `pip install chatbase_track[requests]"
    )

from chatbase_track.backend.base import AbstractBackend
from chatbase_track.types.message import Message

log = logging.getLogger(__name__)


class RequestsBackend(AbstractBackend):
    def __init__(self, max_workers: Optional[int] = None, **kwargs):
        super().__init__(**kwargs)
        self.session = requests.Session()
        self._pool = ThreadPoolExecutor(
            max_workers=max_workers, thread_name_prefix="ChatBase"
        )

    def make_request(
        self, endpoint: str, payload: Dict[str, Any], messages: Tuple[Message]
    ):
        future = self._pool.submit(
            self._make_request, endpoint=endpoint, payload=payload, messages=messages
        )
        return future

    def _make_request(
        self, endpoint: str, payload: Dict[str, Any], messages: Tuple[Message]
    ):
        response = self.session.post(endpoint, json=payload, timeout=5)
        return self.build_response(response.json(), messages=messages)

    def close(self):
        self._pool.shutdown()
        self.session.close()
