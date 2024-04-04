from aiogram.types import Message
from aiogram.filters import Filter
from keyboard.keyboards import main_keyboard_list
from typing import List

class MyFilter(Filter):
    def __init__(self, keyboard_list: List) -> None:
        self.keyboard_list = keyboard_list

    async def __call__(self, message: Message) -> bool:
        return message.text in self.keyboard_list

class FeedBackFilter(Filter):
    def __init__(self) -> None:
        pass
    
    async def __call__(self, message: Message) -> bool:
        return '#' in message.reply_to_message.text
