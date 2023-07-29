import customtkinter as ctk
from PIL import Image, ImageTk
from PIL.ImageTk import PhotoImage
from tkinter import StringVar
from tkcalendar import Calendar
from datetime import datetime
import asyncio
from database import insert_data_into_db
import PyPDF2
import base64
from tkinter import filedialog
from tkinter import messagebox

""" Calendar """


def pick_date_start():
    cal = Calendar(window,
                   selectmode="day",
                   year=datetime.now().year,
                   month=datetime.now().month)
    cal.pack()

    def set_date_start():
        date_str = cal.get_date()
        date = datetime.strptime(date_str, '%d.%m.%Y')
        date_start_var.set(date.strftime('%d.%m.%Y'))
        cal.pack_forget()
        cal.destroy()
        choose_button.pack_forget()
        choose_button.destroy()

    choose_button = ctk.CTkButton(window, text="Выбрать", command=set_date_start)
    choose_button.pack()


def pick_date_end():
    cal = Calendar(window,
                   selectmode="day",
                   year=datetime.now().year,
                   month=datetime.now().month)
    cal.pack()

    def set_date_end():
        date_str = cal.get_date()
        date = datetime.strptime(date_str, '%d.%m.%Y')
        date_end_var.set(date.strftime('%d.%m.%Y'))
        cal.pack_forget()
        cal.destroy()
        choose_button.pack_forget()
        choose_button.destroy()

    choose_button = ctk.CTkButton(window, text="Выбрать", command=set_date_end)
    choose_button.pack()


""" ADD DATA INTO DB """


async def add_data_in_db():
    car_number_str = str(car_number_entry.get()).strip()
    driver_name = str(driver_name_entry.get()).strip()
    date_start_str = str(date_start_entry.get()).strip()
    date_end_str = str(date_end_entry.get()).strip()

    # convert datetime
    date_start = datetime.strptime(date_start_str, '%d.%m.%Y').date()
    date_end = datetime.strptime(date_end_str, '%d.%m.%Y').date()

    # datetime error case
    if date_start > date_end:
        messagebox.showerror('Error',
                             'Дата отправления не может быть поздее даты прибытия')
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


"""  ADD SCREENSHOT OR PDF FILE """


# schema screen upload
def upload_screenshot():
    filepath = filedialog.askopenfilename()
    if filepath:
        with open(filepath, "rb") as file:
            screenshot_data.set(base64.b64encode(file.read()).decode("utf-8"))
            upload_button.configure(fg_color='green', bg_color='green')


# converter from pdf to photo
def convert_pdf_to_jpeg(pdf_file_path):
    images = []
    with open(pdf_file_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        num_pages = pdf_reader.numPages
        for page_num in range(num_pages):
            page = pdf_reader.getPage(page_num)
            image = page.to_image()
            images.append(image)

    return images


def add_pdf_button_click():
    filepath = filedialog.askopenfilename()
    if filepath:
        jpeg_images = convert_pdf_to_jpeg(filepath)
        if jpeg_images:
            for image in jpeg_images:
                screenshot_data.set(
                    base64.b64encode(image.tostring()).decode("utf-8"))
                asyncio.run(add_data_in_db())


def add_button_click():
    asyncio.run(add_data_in_db())


""" UI CORE """

window = ctk.CTk()
window.title('GrandoPro')
window.geometry('900x600')
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

#  load image
image = Image.open('grando.jpg')
image = image.resize((900, 600))
photo: PhotoImage = ImageTk.PhotoImage(image)

# set image as background label
background_label = ctk.CTkLabel(window, image=photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# inserting data strings
car_number_label = ctk.CTkLabel(window,
                                text='Номер машины',
                                font=('Arial', 18))
car_number_label.place(x=10, y=120)

car_number_entry = ctk.CTkEntry(window, width=250)
car_number_entry.place(x=150, y=120)

driver_name_label = ctk.CTkLabel(window, text='Водитель', font=('Arial', 18))
driver_name_label.place(x=10, y=170)

driver_name_entry = ctk.CTkEntry(window, width=250)
driver_name_entry.place(x=150, y=170)

date_start_label = ctk.CTkLabel(window, text='Дата выезда', font=('Arial', 18))
date_start_label.place(x=10, y=220)

date_start_var = StringVar()
date_start_entry = ctk.CTkEntry(window,
                                width=250,
                                textvariable=date_start_var,
                                font=('Arial', 18))
date_start_entry.place(x=150, y=220)

date_end_var = StringVar()
date_end_entry = ctk.CTkEntry(window,
                              width=250,
                              textvariable=date_end_var,
                              font=('Arial', 18))
date_end_entry.place(x=150, y=270)

date_end_label = ctk.CTkLabel(window, text='Дата прибытия', font=('Arial', 18))
date_end_label.place(x=10, y=270)

""" Buttons """

# Выбор перевозчика
combobox = ctk.CTkOptionMenu(
    master=window,
    values=["ООО Компромисс", "ТК Вега", "ООО Грандо Логистик"],
    width=250,
    button_color='black',
    bg_color='blue',
    button_hover_color='white',
    anchor='center')
combobox.place(x=150, y=80)
combobox.set("Перевозчик")

# Calendar date selection
date_start_button = ctk.CTkButton(window,
                                  text='Дата выезда',
                                  command=pick_date_start,
                                  fg_color='black')
date_start_button.place(x=410, y=220)

date_end_button = ctk.CTkButton(window,
                                text='Дата прибытия',
                                command=pick_date_end,
                                fg_color='black')
date_end_button.place(x=410, y=270)

# Загрузка данных в ДБ
add_button = ctk.CTkButton(window,
                           text='Добавить данные',
                           command=add_button_click,
                           fg_color='black')
add_button.place(x=140, y=320)

screenshot_data = StringVar()
upload_button = ctk.CTkButton(window,
                              text='Загрузить скриншот фактической отгрузки',
                              command=upload_screenshot,
                              fg_color='black',
                              bg_color='black')
upload_button.place(x=590, y=550)

add_pdf_button = ctk.CTkButton(window,
                               text='Загрузить pdf файл',
                               command=add_pdf_button_click,
                               fg_color='black',
                               bg_color='black')
add_pdf_button.place(x=590, y=500)


def create_main_window():
    window.mainloop()
