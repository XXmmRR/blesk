from aiogram import types

start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
start_keyboard.add(types.KeyboardButton(text='Поделиться контактом', request_contact=True))
start_keyboard.add(types.KeyboardButton(text='Анонимно'))


main_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

main_keyboard_list = ['Предупредить о риске', 'Рассказать о проблеме', 'Предложить идею', 'Попросить о помощи', 'Поблагодарить кого-то']

[main_keyboard.add(types.KeyboardButton(text=x)) for x in main_keyboard_list]

