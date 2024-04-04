from aiogram import types

start_buttons = [ 
  [types.KeyboardButton(text='Поделиться контактом', request_contact=True)],
  [types.KeyboardButton(text='Анонимно')]
]
start_keyboard = types.ReplyKeyboardMarkup(keyboard=start_buttons, resize_keyboard=True)



main_keyboard_list = ['Предупредить о риске', 'Рассказать о проблеме', 'Предложить идею', 'Попросить о помощи', 'Поблагодарить кого-то']

main_buttons = [[types.KeyboardButton(text=x) for x in main_keyboard_list]]
main_keyboard = types.ReplyKeyboardMarkup(keyboard=main_buttons)

