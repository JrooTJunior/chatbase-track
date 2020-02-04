import asyncio
import logging
from typing import Dict, Any, Tuple

try:
    import aiohttp
except ImportError:
    raise ImportError(
        "`aiohttp` is not installer. You can install it by `pip install chatbase_track[aiohttp]"
    )

from chatbase_track.backend.base import AbstractBackend
from chatbase_track.types.message import Message
from chatbase_track.types.response import MessagesResponse

log = logging.getLogger(__name__)


class AiohttpBackend(AbstractBackend):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.session = aiohttp.ClientSession()

    def make_request(
        self, endpoint: str, payload: Dict[str, Any], messages: Tuple[Message]
    ):
        loop = asyncio.get_running_loop()
        return loop.create_task(
            self._make_request(endpoint=endpoint, payload=payload, messages=messages)
        )

    async def _make_request(
        self, endpoint: str, payload: Dict[str, Any], messages: Tuple[Message]
    ) -> MessagesResponse:
        async with self.session.post(
            endpoint, json=payload, timeout=aiohttp.ClientTimeout(total=5)
        ) as response:
            return self.build_response(await response.json(), messages=messages)

    async def close(self):
        await self.session.close()

    def __enter__(self):
        raise RuntimeError("AiohttpBackend can not be used as async context manager")

    def __exit__(self, exc_type, exc_val, exc_tb):
        raise RuntimeError("AiohttpBackend can not be used as async context manager")

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
