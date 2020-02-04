import asyncio
import logging
from typing import Dict, Any, Tuple

try:
    import httpx
except ImportError:
    raise ImportError(
        "`httpx` is not installer. You can install it by `pip install chatbase_track[httpx]"
    )

from chatbase_track.backend.base import AbstractBackend
from chatbase_track.types.message import Message

log = logging.getLogger(__name__)


class HttpxBackend(AbstractBackend):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.session = httpx.AsyncClient()

    def make_request(
        self, endpoint: str, payload: Dict[str, Any], messages: Tuple[Message]
    ):
        loop = asyncio.get_running_loop()
        return loop.create_task(
            self._make_request(endpoint=endpoint, payload=payload, messages=messages)
        )

    async def _make_request(
        self, endpoint: str, payload: Dict[str, Any], messages: Tuple[Message]
    ):
        response = await self.session.post(endpoint, json=payload)
        return self.build_response(response.json(), messages=messages)

    async def close(self):
        await self.session.aclose()

    def __enter__(self):
        raise RuntimeError("HttpxBackend can not be used as async context manager")

    def __exit__(self, exc_type, exc_val, exc_tb):
        raise RuntimeError("HttpxBackend can not be used as async context manager")

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
