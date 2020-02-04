from typing import Optional, Union, List

from chatbase_track.types.base import Base


class MessageResult(Base):
    message_id: Optional[int] = None
    status: Union[str, int]
    error: Optional[str] = None

    @property
    def is_success(self) -> bool:
        return self.status in {200, "success"}

    @property
    def is_error(self) -> bool:
        return not self.is_success


class MessagesResponse(Base):
    all_succeeded: bool
    responses: List[MessageResult]
    status: int
