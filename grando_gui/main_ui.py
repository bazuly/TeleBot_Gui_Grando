import asyncio
from datetime import datetime
from gui import driver_name_entry, date_end_entry, \
    date_start_entry, combobox, screenshot_data, create_main_window, window, \
    car_number_entry
from database import insert_data_into_db

create_main_window()


async def add_data_in_db():
    car_number_str = str(car_number_entry.get()).strip()
    driver_name = str(driver_name_entry.get()).strip()
    date_start_str = str(date_start_entry.get()).strip()
    date_end_str = str(date_end_entry.get()).strip()

    # convert datetime
    date_start = datetime.strptime(date_start_str, '%d.%m.%Y').date()
    date_end = datetime.strptime(date_end_str, '%d.%m.%Y').date()

    # remove space bars in car number
    letter_counter = 0
    for i in car_number_str:
        if i.isalpha() or i.isnumeric():
            letter_counter += 1

    if letter_counter <= 9:
        car_number_str = car_number_str.replace(' ', '').upper()
    else:
        car_number_str.strip().upper()

    car_number = car_number_str

    trans_name = combobox.get()
    if trans_name == 'Перевозчик':
        trans_name = None

    screenshot = screenshot_data.get()

    await insert_data_into_db(car_number, driver_name, date_start, date_end,
                              trans_name, screenshot)


def add_button_click():
    asyncio.run(add_data_in_db())


window.mainloop()
