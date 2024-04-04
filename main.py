import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, InputMediaPhoto
from keyboard.keyboards import generate_keyboard, main_keyboard_list, start_keyboard, admin_keyboard
from texts import text_dict
from config import TOKEN, GROUP, ADMIN
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from filters import MyFilter, FeedBackFilter
from database import User
from middlewares import CaptionAlbumMiddleware

dp = Dispatcher()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

class MainState(StatesGroup):
    description = State()
    
class Broadcast(StatesGroup):
    message = State()
    

dp.message.middleware(CaptionAlbumMiddleware())

@dp.message(F.text == '/admin')
async def admin_panel(message: Message, state: FSMContext):
    await state.clear()
    if message.from_user.id == ADMIN:
         await message.answer('Админ панель', reply_markup=admin_keyboard)

@dp.message(F.text == 'Рассылка')
async def broadcast(message: Message, state: FSMContext):
    if message.from_user.id == ADMIN:
        await message.answer('Введите сообщение для рассылки')
        await state.set_state(Broadcast.message)

@dp.message(Broadcast.message)
async def mail_handler(message: types.Message, state: FSMContext, album = None):
    users = await User.objects.all()
    if album:
        success = 0
        fails = 0
        notification = await message.answer(f'Успешных пересылок {success} неудачных {fails}')
        photos = [x[0].file_id for x in album]
        try:
            text = [x[1] for x in album if x[1] != None][0]
            media_group = [InputMediaPhoto(media=x) for x in photos[1:]]
            media_group.append(InputMediaPhoto(media=photos[0], caption=text, parse_mode='HTML'))
        except:
            media_group = [InputMediaPhoto(media=x) for x in photos[1:]]
            media_group.append(InputMediaPhoto(media=photos[0], parse_mode='HTML'))

        for user in users:
            try:
                success += 1
                await notification.edit_text(f'Успешных пересылок {success} неудачных {fails}')

                await bot.send_media_group(user.tg_id,
                                            media_group)
            except Exception as e:
                print(e)
                fails += 1
                await notification.edit_text(f'Успешных пересылок {success} неудачных {fails}')
    else:
        success = 0
        fails = 0
        markup = message.reply_markup
        notification = await message.answer(f'Успешных пересылок {success} неудачных {fails}')
        for user in users:
            try:
                await bot.send_message(
                        chat_id=user.tg_id,
                        text=message.text,
                        reply_markup=markup
                    )
                success += 1
                await notification.edit_text(f'Успешных пересылок {success} неудачных {fails}')
            except Exception as e:
                print(e)
                fails += 1
                await notification.edit_text(f'Успешных пересылок {success} неудачных {fails}')
    await state.clear()


@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    """
    This handler receives messages with `/start` command
    """
    await state.clear()
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
async def input_handler(message: Message, state: FSMContext, album = None):
    first_msg = await state.get_data()
    first_msg = first_msg['first_message']
    user = await User.objects.get(tg_id=message.from_user.id)
    number = user.number
    is_anon = user.is_anon
    if number:
        request_text = f'Запрос от пользователя: @{message.from_user.username}\nномер: {number},\nЗапрос: "{message.text}"\n\nid#{message.from_user.id}'
    else:
        request_text = f'Запрос от пользователя: @{message.from_user.username}\nЗапрос: "{message.text}"\n\nid#{message.from_user.id}'
    if album:
        photos = [x[0].file_id for x in album]
        text = [x[1] for x in album if x[1] != None][0]
        media_group = [InputMediaPhoto(media=x) for x in photos[1:]]
        request_text = f'Запрос от пользователя: @{message.from_user.username}\nЗапрос: "{text}"\n\nid#{message.from_user.id}'
        media_group.append(InputMediaPhoto(media=photos[0], caption=request_text, parse_mode='HTML'))
        await bot.send_media_group(GROUP, media_group)
    else:
        await bot.send_message(GROUP, text=request_text)
    await message.answer(text_dict[first_msg][is_anon], reply_markup=generate_keyboard(is_anon=is_anon))
    await state.clear()

@dp.message(FeedBackFilter())
async def test_filter(message: Message):
    id = message.reply_to_message.text.split('#')[-1]
    await bot.send_message(chat_id=id, text=message.text)


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main()) 