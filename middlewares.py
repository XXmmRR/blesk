import asyncio
from typing import Callable, Dict, Any, Awaitable, Union

from aiogram import BaseMiddleware
from aiogram.types import Message


class CaptionAlbumMiddleware(BaseMiddleware):
    """
    This middleware is for capturing document, photo and video groups
    """
    album_data: dict = {}

    def __init__(self, latency: Union[int, float] = 2):
        self.latency = latency
        super().__init__()

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        if event.document:
            document = event.document
        elif event.photo:
            document = event.photo[-1]
        elif event.video:
            document = event.video
        else:
            return await handler(event, data)

        try:
            self.album_data[event.chat.id].append((document, event.caption))
        except KeyError:
            self.album_data[event.chat.id] = [(document, event.caption)]
            await asyncio.sleep(self.latency)

            data["album"] = self.album_data[event.chat.id]
            del self.album_data[event.chat.id]

            return await handler(event, data)