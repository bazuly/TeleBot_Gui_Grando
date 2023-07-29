from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def start_command_button():
    button_text = ' Get info 🚚'
    main_button = InlineKeyboardButton(button_text, callback_data='button_pressed')
    markup = InlineKeyboardMarkup().add(main_button)

    return markup


def guide_button():
    button_text = 'guide button'
    main_button = InlineKeyboardButton(button_text, callback_data='guide_button_pressed')
    markup = InlineKeyboardMarkup().add(main_button)

    return markup

