import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from keyboard.keyboards import generate_keyboard, main_keyboard_list, start_keyboard, admin_keyboard
from texts import text_dict
from config import TOKEN, GROUP
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from texts import anon_risk, not_anon_risk
from filters import MyFilter
from database import User

dp = Dispatcher()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

class MainState(StatesGroup):
    description = State()
    
@dp.message(F.text == '/admin')
async def admin_panel(message: Message):
    await message.answer('Админ панель', reply_markup=admin_keyboard)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    
    user = await User.objects.get_or_create(tg_id=message.from_user.id, username=message.from_user.username, name=message.from_user.username)
    user = user[0]
    if user:
        if user.is_anon:
            if user.is_anon == True:
                await anon_handler(message)
            else:
                await not_anon_handler(message)
            return 

    await message.answer('Добрый день! Вас приветствует блеск-бот. Здесь вы можете поделиться информацией, которую считаете важной. Мы благодарим вас за участие в жизни "блеска')
    await message.answer('Вы можете оставить свои контактные данные или остаться анонимным', reply_markup=start_keyboard)

@dp.message(F.text=='Анонимно')
async def anon_handler(message: Message) -> None:
    user = await User.objects.get(tg_id=message.from_user.id)
    user.is_anon = True
    await message.answer('Вы хотели бы', reply_markup=generate_keyboard(user.is_anon))
    await user.update()

@dp.message(F.contact)
async def not_anon_handler(message: Message):
    user = await User.objects.get(tg_id=message.from_user.id)
    user.is_anon = False
    user.number = message.contact.phone_number
    await message.answer('Вы хотели бы', reply_markup=generate_keyboard(user.is_anon))
    await user.update()


@dp.message(MyFilter(keyboard_list=main_keyboard_list))   
async def risk_handler(message: Message, state: FSMContext):
    await message.answer('Опишите свой запрос', reply_markup=types.ReplyKeyboardRemove())
    await state.set_data({'first_message': message.text})
    await state.set_state(MainState.description)
    
@dp.message(MainState.description)
async def input_handler(message: Message, state: FSMContext):
    first_msg = await state.get_data()
    first_msg = first_msg['first_message']
    user = await User.objects.get(tg_id=message.from_user.id)
    
    number = user.number
    is_anon = user.is_anon
    if number:
        request_text = f'Запрос от пользователя: @{message.from_user.username}\nномер: {number},\nЗапрос: "{message.text}"\n\nid#{message.from_user.id}'
    else:
        request_text = f'Запрос от пользователя: @{message.from_user.username}\nЗапрос: "{message.text}"\n\nid#{message.from_user.id}'

    await bot.send_message(GROUP, text=request_text)
    await message.answer(text_dict[first_msg][is_anon], reply_markup=generate_keyboard(is_anon=is_anon))
    
    

async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main()) 