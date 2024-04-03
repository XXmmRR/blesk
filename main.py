import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from keyboard.keyboards import main_keyboard, main_keyboard_list
from texts import text_dict
from config import TOKEN
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from texts import anon_risk, not_anon_risk

dp = Dispatcher()

class MainState(StatesGroup):
    description = State()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer('Добрый день! Вас приветствует блеск-бот. Здесь вы можете поделиться информацией, которую считаете важной. Мы благодарим вас за участие в жизни "блеска')
    await message.answer('Вы можете оставить свои контактные данные или остаться анонимным')

@dp.message(F.text=='Анонимно')
async def anon_handler(message: Message) -> None:
    await message.answer('Вы хотели бы', reply_markup=main_keyboard)

@dp.message(F.text in main_keyboard_list)   
async def risk_handler(message: Message, state: FSMContext):
    await message.answer('Опишите свой запрос')
    await state.set_data({'first_message': message.text})
    await state.set_state(MainState.description)
    
@dp.message(MainState.description)
async def input_handler(message: Message, state: FSMContext):
    first_msg = await state.get_data()['first_message']
    is_anon = True
    await message.answer(text_dict[first_msg][is_anon])
    
    

async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main()) 