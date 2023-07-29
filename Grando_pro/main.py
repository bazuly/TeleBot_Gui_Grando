import config
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from handlers import start_command, button_pressed_handler
from io import BytesIO
import base64
from PIL import Image
from database import setup_db

logging.basicConfig(level=logging.INFO)


class Grando_bot:
    def __init__(self):
        self.bot = Bot(token=config.BOT_TOKEN)
        self.dp = Dispatcher(self.bot)
        self.value = ''
        self.limit = 5
        self.image_id = ''

        self.setup_handlers()

    def setup_handlers(self):
        self.dp.register_message_handler(set_limit_handler,
                                         commands=['set_limit'])
        self.dp.register_message_handler(start_command,
                                         commands=['start'])
        self.dp.register_callback_query_handler(button_pressed_handler)
        self.dp.register_message_handler(handle_message,
                                         commands=['info'])
        self.dp.register_message_handler(handle_image_command,
                                         commands=['image'])

    async def start(self):
        await self.dp.start_polling()


""" Telegram commands """


async def handle_message(message: types.Message, self):
    try:
        self.value = message.text

        info = self.value.split()
        if len(info) > 1 and info[0] == '/info':
            first_value = info[1]
        else:
            await message.answer('Error: missing value')
            return

        parts = self.value.split(' ', 2)
        if len(parts) >= 3:
            second_value = parts[2].split()[0]
        else:
            await message.answer('Error: missing value')
            return

        data = await self.get_data_from_db(first_value, second_value)
        await self.process_data(message, data)
    except Exception as e:
        await message.answer(e)


"""  Set message limit  """


async def set_limit_handler(message: types.Message, self):
    try:
        arg = message.text.split()[1].lower()
        if arg == 'default':
            self.limit = 5
            await message.answer('Limit set to default: 5')
        else:
            self.limit = int(arg)
            if self.limit > 30 or self.limit <= 0 or self.limit is float:
                raise ValueError('Invalid limit')
            else:
                await message.answer(f'Limit set to: {self.limit}')
    except (IndexError, ValueError):
        await message.answer('Limit cannot be float or > 30, or < 0')


async def handle_image_command(self, message: types.Message):
    image_data = await self.get_image_from_db(self.image_id)
    if image_data:
        await self.send_image(message, image_data)
    else:
        await message.answer('Image not found')


""" Getting data from DB with commands """


async def get_data_from_db(self, first_value, second_value):
    db = await setup_db()
    str_limit = str(self.limit)
    if first_value == 'driver_name':
        second_value = second_value.title()
        result = await db.fetch(
            f"Select * from grando_ftl_screen_test where {first_value} = '{second_value}'"
            f"ORDER BY {first_value} DESC LIMIT {str_limit}")

    elif first_value == 'date_start':
        result = await db.fetch(
            f"Select * from grando_ftl_screen_test where {first_value} = '{second_value}'"
            f"ORDER BY {first_value} DESC LIMIT {str_limit}"
        )
    else:
        result = await db.fetch(
            f"SELECT * from grando_ftl where {first_value} = '{second_value}' ORDER BY {first_value} "
            f"DESC LIMIT {str_limit}")
    await db.close()
    if result:
        self.image_id = result[0]['id']

    else:
        self.image_id = None

    return result


async def process_data(message, data):
    result = ""

    for item in data:
        result += '\n'
        result += 'Номер ТС: ' + str(item['car_number'])
        result += '\n'
        result += 'Имя водителя: ' + str(item['driver_name'])
        result += '\n'
        result += 'Дата выезда: ' + str(item['date_start'])
        result += '\n'
        result += 'Дата прибытия: ' + str(item['date_end'])
        result += '\n'
        result += 'Перевозчик: ' + str(item['trans_name'])
        result += '\n'

    await message.answer(result)


""" Get image from DB """


async def get_image_from_db(self):
    db = await setup_db()
    result = await db.fetchrow(
        f"SELECT screenshot FROM grando_ftl_screen_test WHERE id = '{self.image_id}'")
    await db.close()
    return result['screenshot'] if result else None


""" Send image """


async def send_image(message, image_data):
    try:
        image_bytes = base64.b64decode(image_data)
        image = Image.open(BytesIO(image_bytes))
        # Convert the image to bytes
        image_byte_array = BytesIO()
        image.save(image_byte_array, format='JPEG')
        image_byte_array.seek(0)
        # Send the image as a photo
        await message.answer_photo(image_byte_array)
    except Exception as e:
        await message.answer(f'Error sending image: {e}')


if __name__ == "__main__":
    bot = Grando_bot()
    asyncio.run(bot.start())
