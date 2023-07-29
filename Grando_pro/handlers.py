from aiogram import types
from buttons import *
from guide_message import guide
from guide_message import msg


async def start_command(message: types.Message):
    markup = start_command_button()
    spaces = ' ' * ((len(msg)) // 2 + 10)
    text = msg + '\n' + '\n' + spaces + '👇'
    markup_guide = guide_button()
    await message.answer(text, reply_markup=markup)
    await message.answer('To get instructions press button below 🗺', reply_markup=markup_guide)


async def button_pressed_handler(callback_query: types.CallbackQuery):
    if callback_query.data == 'button_pressed':
        await callback_query.answer()
        await callback_query.message.answer('Use /info command')
    elif callback_query.data == 'guide_button_pressed':
        await callback_query.answer()
        await callback_query.message.answer(guide)
        

