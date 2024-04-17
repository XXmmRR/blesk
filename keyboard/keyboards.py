from aiogram import types

start_buttons = [ 
  [types.KeyboardButton(text='Поделиться контактом', request_contact=True)],
  [types.KeyboardButton(text='Анонимно')]
]
start_keyboard = types.ReplyKeyboardMarkup(keyboard=start_buttons, resize_keyboard=True)

request_buttons = [ 
  [types.KeyboardButton(text='Поделиться контактом', request_contact=True)],
  [types.KeyboardButton(text='🔙Назад')]
]

back_buttons = [
  [types.KeyboardButton(text='🔙Назад')]
  ]

back_keyboard = types.ReplyKeyboardMarkup(keyboard=back_buttons, resize_keyboard=True)

contact_keyboard = types.ReplyKeyboardMarkup(keyboard=request_buttons, resize_keyboard=True)

main_keyboard_list = ['Предупредить о риске❗️', 'Рассказать о проблеме😱', 'Предложить идею💡', 'Попросить о помощи🙏🏻', 'Поблагодарить кого-то❤️']



def generate_keyboard(is_anon: bool):
    main_keyboard_list = ['Предупредить о риске❗️', 'Рассказать о проблеме😱', 'Предложить идею💡', 'Попросить о помощи🙏🏻', 'Поблагодарить кого-то❤️']
    if is_anon:
        main_keyboard_list.remove('Попросить о помощи🙏🏻')
        main_keyboard_list.remove('Поблагодарить кого-то❤️')
    main_buttons = [[types.KeyboardButton(text=x)] for x in main_keyboard_list]
    main_keyboard = types.ReplyKeyboardMarkup(keyboard=main_buttons)
    return main_keyboard

admin_buttons = [[types.KeyboardButton(text='Рассылка')]]
admin_keyboard = types.ReplyKeyboardMarkup(keyboard=admin_buttons, resize_keyboard=True)
