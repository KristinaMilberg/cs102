import json
import re
from datetime import datetime, timedelta
from urllib.parse import urlparse

import gspread  # type: ignore
import pandas as pd  # type: ignore
import requests  # type: ignore
import telebot  # type: ignore

bot = telebot.TeleBot("6099153394:AAFJyP18BbGf0FMTPUZt3I1isr5wQt51JTE")
USEFUL_ARG = []
TABLE_CONNECTED = False  # переменная-флаг для проверки подключения таблицы


def is_valid_date(date: str = "01/01/00", divider: str = "/") -> bool:
    """Проверяем, что дата дедлайна валидна:
    - дата не может быть до текущей
    - не может быть позже, чем через год
    - не может быть такой, которой нет в календаре
    - может быть сегодняшним числом
    - пользователь не должен быть обязан вводить конкретный формат даты
    (например, только через точку или только через слеш)"""
    if divider not in date:
        return False
    dmy = date.split(divider)
    if len(dmy) < 3:
        return False
    day, month, year = list(map(int, dmy))
    today = list(map(int, datetime.today().date().strftime("20%year/%month/%day").split(sep="/")))
    today = datetime(today[0], today[1], today[2])  # type: ignore
    try:
        date = datetime(2000 + year, month, day)  # type: ignore
    except ValueError:
        return False
    period = date - today  # type: ignore
    return period.days < 365 and date >= today  # type: ignore


def is_valid_url(url: str = "") -> bool:
    """Проверяем, что ссылка рабочая"""
    try:
        parsed_url = urlparse(url)
        if not parsed_url.scheme:
            url = "http://" + url
        response = requests.get(url)
        if response.status_code == 200:
            return True
    except requests.exceptions.ConnectionError:
        return False
    return False


def convert_date(date: str = "01/01/00"):
    """Конвертируем дату из строки в datetime"""
    divider = date[2]
    dates = date.split(divider)
    if len(dates[-1]) == 4:
        return datetime.strptime(date, "%d" + divider + "%m" + divider + "%Y")
    elif len(dates[-1]) == 2:
        return datetime.strptime(date, "%d" + divider + "%m" + divider + "%y")


def connect_table(message):
    """Подключаемся к Google-таблице"""
    global TABLE_CONNECTED
    url = message.text
    sheet_id = url.split("/")[5]  # Нужно извлечь id страницы из ссылки на Google-таблицу
    try:
        with open("tables.json", encoding="utf-8") as json_file:
            tables = json.load(json_file)
        title = len(tables) + 1
        tables[title] = {"url": url, "id": sheet_id}
    except FileNotFoundError:
        tables = {0: {"url": url, "id": sheet_id}}
    with open("tables.json", "w", encoding="utf-8") as json_file:
        json.dump(tables, json_file)
    TABLE_CONNECTED = True
    text = bot.send_message(message.chat.id, "Таблица подключена!")
    bot.register_next_step_handler(text, start)


def access_current_sheet():
    """Обращаемся к Google-таблице"""
    with open("tables.json", encoding="utf-8") as json_file:
        tables = json.load(json_file)
    sheet_id = tables[max(tables)]["id"]
    gc = gspread.service_account(filename="credentials.json")
    sh = gc.open_by_key(sheet_id)
    worksheet = sh.sheet1
    # Преобразуем Google-таблицу в таблицу pandas
    worksheet_values = worksheet.get_all_values()
    header = worksheet_values[0]
    data = worksheet_values[1:]
    dataframe = pd.DataFrame(data, columns=header)
    return worksheet, tables[max(tables)]["url"], dataframe


def choose_action(message):
    """Обрабатываем действия верхнего уровня"""
    if message.text == "Подключить Google-таблицу":
        bot.send_message(message.chat.id, "Пришли ссылку на Google-таблицу")
        bot.register_next_step_handler(message, connect_table)
    elif message.text == "Редактировать предметы":
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        start_markup.row("Добавить предмет 🆕")
        start_markup.row("Редактировать предмет")
        start_markup.row("Удалить предмет 🚮")
        start_markup.row("Удалить все предметы 🗑")
        info = bot.send_message(message.chat.id, "Что именно ты хочешь сделать?", reply_markup=start_markup)
        bot.register_next_step_handler(info, choose_subject_action)
    elif message.text == "Редактировать дедлайны":
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        start_markup.row("Добавить дедлайн 🆕")
        start_markup.row("Редактировать дедлайн")
        info = bot.send_message(message.chat.id, "Что именно ты хочешь сделать?", reply_markup=start_markup)
        bot.register_next_step_handler(info, choose_deadline_action)
    elif message.text == "Посмотреть дедлайны на этой неделе":
        deadlines_this_week(message)
    elif message.text == "Удалить всё":
        clear_all(message)


def choose_subject_action(message):
    """Выбираем действие в разделе Редактировать предметы"""
    if message.text == "Добавить предмет 🆕":
        message = bot.send_message(message.chat.id, "Введи название и ссылку через пробел ")
        bot.register_next_step_handler(message, add_subject)
    elif message.text == "Редактировать предмет":
        worksheet, sheet, dataframe = access_current_sheet()
        mrkp = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for element in worksheet.col_values(1)[1:]:
            mrkp.row(f"{element}")
        info = bot.send_message(message.chat.id, "Выберите предмет", reply_markup=mrkp)
        bot.register_next_step_handler(info, update_subject)
    elif message.text == "Удалить предмет 🚮":
        worksheet, sheet, dataframe = access_current_sheet()
        mrkp = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for element in worksheet.col_values(1)[1:]:
            mrkp.row(f"{element}")
        info = bot.send_message(message.chat.id, "Выберите предмет", reply_markup=mrkp)
        bot.register_next_step_handler(info, delete_subject)
    elif message.text == "Удалить все предметы 🗑":
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        start_markup.row("Да")
        start_markup.row("Нет")
        info = bot.send_message(
            message.chat.id,
            "Вы уверены, что хотите удалить все?",
            reply_markup=start_markup,
        )
        bot.register_next_step_handler(info, choose_removal_option)


def choose_deadline_action(message):
    """Выбираем действие в разделе Редактировать дедлайн"""
    if message.text == "Добавить дедлайн 🆕":
        worksheet, _, dataframe = access_current_sheet()
        mark_up = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for el in worksheet.col_values(1)[1:]:
            mark_up.row(f"{el}")
        info = bot.send_message(message.chat.id, "Выберите предмет", reply_markup=mark_up)
        bot.register_next_step_handler(info, add_deadline)
    elif message.text == "Редактировать дедлайн":
        worksheet, b, dataframe = access_current_sheet()
        mark_up = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for el in worksheet.col_values(1)[1:]:
            mark_up.row(f"{el}")
        info = bot.send_message(message.chat.id, "Выбери предмет", reply_markup=mark_up)
        bot.register_next_step_handler(info, update_deadline)


def add_subject(message):
    """Вносим новый предмет в Google-таблицу"""
    try:
        name = message.text.split()[0]
        url = message.text.split()[1]
        worksheet, _, dataframe = access_current_sheet()
        in_worksheet = False
        for i in range(2, len(worksheet.col_values(1)) + 1):
            if worksheet.cell(i, 1).value == name:
                in_worksheet = True
        if not in_worksheet:
            worksheet.append_row([name, url])
            bot.send_message(message.chat.id, "Готово")
        else:
            bot.send_message(message.chat.id, "Предмет уже находится в таблице")
        start(message)
    except IndexError:
        info = bot.send_message(
            message.chat.id,
            "Пожалуйста, введите название и ссылку в одном сообщении через пробел",
        )
        bot.register_next_step_handler(info, add_subject)


def add_subject_url(message):
    """Вносим новую ссылку на таблицу предмета в Google-таблицу"""
    worksheet, sheet, dataframe = access_current_sheet()
    # Получаем последнюю строку таблицы
    last_row = len(sheet.get_all_values()) + 1
    # Записываем новую ссылку в таблицу
    sheet.update_cell(last_row, 1, message)
    return f"Ссылка {message} добавлена в таблицу"


def update_subject(message):
    """Обновляем информацию о предмете в Google-таблице"""
    global USEFUL_ARG
    USEFUL_ARG = []
    USEFUL_ARG.append(message.text)
    inf = bot.send_message(message.chat.id, "Введите название и ссылку в одном сообщении через пробел")
    bot.register_next_step_handler(inf, update_subject2)


def update_subject2(message):
    global USEFUL_ARG
    try:
        name = message.text.split()[0]
        url = message.text.split()[1]
        worksheet, _, dataframe = access_current_sheet()
        ind = worksheet.find(f"{USEFUL_ARG[0]}").row
        cell_list = worksheet.range(f"A{ind}:B{ind}")
        cell_list[0].value = name
        cell_list[1].value = url
        worksheet.update_cells(cell_list)
        bot.send_message(message.chat.id, "Готово")
    except IndexError:
        inf = bot.send_message(
            message.chat.id,
            "Пожалуйста, введите название и ссылку в одном сообщении через пробел",
        )
        bot.register_next_step_handler(inf, update_subject2)
    start(message)


def delete_subject(message):
    """Удаляем предмет в Google-таблице"""
    global USEFUL_ARG
    worksheet, _, dataframe = access_current_sheet()
    ind = worksheet.find(f"{message.text}").row
    worksheet.delete_rows(int(ind), int(ind))
    bot.send_message(message.chat.id, "Готово")
    start(message)


def delete_all_subjects(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    if message.text == "Удалить все предметы 🗑":
        sheet, _, _ = access_current_sheet()
        subjects = sheet.range("A2:A" + str(sheet.row_count))
        for cell in subjects:
            cell.clear()
        bot.send_message(message.chat_id, "Все предметы удалены", reply_markup=markup)


def add_deadline(message):
    global USEFUL_ARG
    USEFUL_ARG = []
    USEFUL_ARG.append(message.text)
    inf = bot.send_message(
        message.chat.id, "Введи дату в формате 'dd/mm/yy' или 'dd.mm.yyyy' или с любым другим разделителем"
    )
    bot.register_next_step_handler(inf, add_deadline2)


def add_deadline2(message):
    global USEFUL_ARG
    date = message.text
    divider = ""
    for i in range(len(date)):
        if not date[i].isdigit():
            divider = date[i]
    dates = date.split(divider)
    if not re.match(r"\d\d" + divider + r"\d\d" + divider + r"\d\d", message.text) and not re.match(
        r"\d\d" + divider + r"\d\d" + divider + r"\d\d\d\d", message.text
    ):
        info = bot.send_message(
            message.chat.id,
            "Неправильный формат!\nВведите время в формате 'dd/mm/yy' или 'dd/mm/yyyy' или с любым другим разделителем",
        )
        bot.register_next_step_handler(info, add_deadline2)
    else:
        try:
            if convert_date(message.text) < datetime.today():
                bot.send_message(message.chat.id, "Дедлайн сгорел 😰")
            else:
                worksheet, _, dataframe = access_current_sheet()
                row = worksheet.find(f"{USEFUL_ARG[0]}").row
                number = len(worksheet.row_values(row))
                dateline = ""
                if len(dates[-1]) == 4:
                    dateline = dates[0] + "/" + dates[1] + "/" + dates[2][2:]
                else:
                    dateline = dates[0] + "/" + dates[1] + "/" + dates[2]
                worksheet.update_cell(row, number + 1, dateline)
                if not worksheet.cell(1, number + 1).value:
                    num = int(worksheet.cell(1, number).value)
                    worksheet.update_cell(1, number + 1, num + 1)
                bot.send_message(message.chat.id, "Готово")
                start(message)
        except:
            ins = bot.send_message(message.chat.id, "Такая дата не существует")
            bot.register_next_step_handler(ins, add_deadline2)


def update_deadline(message):
    """Обновляем дедлайн"""
    global USEFUL_ARG
    USEFUL_ARG = [message.text]
    worksheet, _, dataframe = access_current_sheet()
    mark_up = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for element in worksheet.row_values(1)[2:]:
        mark_up.row(f"{element}")
    inf = bot.send_message(message.chat.id, "Выбери номер работы", reply_markup=mark_up)
    bot.register_next_step_handler(inf, update_deadline2)


def update_deadline2(message):
    global USEFUL_ARG
    USEFUL_ARG.append(message.text)
    inf = bot.send_message(
        message.chat.id, "Введите время в формате 'dd/mm/yy' или 'dd/mm/yyyy' или с любым другим разделителем"
    )
    bot.register_next_step_handler(inf, update_deadline3)


def update_deadline3(message):
    global USEFUL_ARG
    date = message.text
    divider = ""
    for i in range(len(date)):
        if not date[i].isdigit():
            divider = date[i]
    dates = date.split(divider)
    if not re.match(r"\d\d" + divider + r"\d\d" + divider + r"\d\d", message.text) and not re.match(
        r"\d\d" + divider + r"\d\d" + divider + r"\d\d\d\d", message.text
    ):
        info = bot.send_message(message.chat.id, "Неправильный формат!\nВведите дату в формате 'dd/mm/yy'")
        bot.register_next_step_handler(info, update_deadline3)
    else:
        try:
            if convert_date(message.text) < datetime.today():
                bot.send_message(message.chat.id, "Дедлайн сгорел 😰")
            else:
                worksheet, _, dataframe = access_current_sheet()
                row = worksheet.find(f"{USEFUL_ARG[0]}").row
                col = worksheet.find(f"{USEFUL_ARG[1]}").col
                dateline = ""
                if len(dates[-1]) == 4:
                    dateline = dates[0] + "/" + dates[1] + "/" + dates[2][2:]
                else:
                    dateline = dates[0] + "/" + dates[1] + "/" + dates[2]
                worksheet.update_cell(row, col, dateline)
                bot.send_message(message.chat.id, "Готово")
                start(message)
        except:
            info = bot.send_message(
                message.chat.id,
                "Пожалуйста, введи дату в правильном формате 'dd/mm/yyyy'",
            )
            bot.register_next_step_handler(info, update_deadline3)


def choose_subject(message):
    """Выбираем предмет, у которого надо отредактировать дедлайн"""
    global USEFUL_ARG
    USEFUL_ARG = [message.text]
    info = bot.send_message(
        message.chat.id, "Введи дату в формате 'dd/mm/yy' или 'dd/mm/yyyy' или с любым другим разделителем"
    )
    bot.register_next_step_handler(info, add_deadline2)


def deadlines_this_week(message):
    today = datetime.today()
    week = today + timedelta(days=7)
    worksheet, _, dataframe = access_current_sheet()
    msg = ""
    for i in range(2, len(worksheet.col_values(1)) + 1):
        for deadline in worksheet.row_values(i)[2:]:
            if week >= convert_date(deadline) >= today:
                msg += f"{worksheet.cell(i, 1).value}: {deadline}\n"
    if msg == "":
        msg += "Планов на эту неделю нет"
    bot.send_message(message.chat.id, msg)
    start(message)


def choose_removal_option(message):
    """Уточняем, точно ли надо удалить все"""
    if message.text == "Да":
        clear_all(message)
    elif message.text == "Нет":
        start(message)


def clear_all(message):
    """Удаляем все из Google-таблицы"""
    worksheet, sheet, dataframe = access_current_sheet()
    sheet.del_worksheet(worksheet)
    start(message)


@bot.message_handler(commands=["start"])
def start(message):
    global TABLE_CONNECTED
    if TABLE_CONNECTED is True:
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        start_markup.row("Посмотреть дедлайны на этой неделе")
        start_markup.row("Редактировать дедлайны")
        start_markup.row("Редактировать предметы")
        start_markup.row("Показать дисциплины")
        info = bot.send_message(message.chat.id, "Что хочешь сделать?", reply_markup=start_markup)
        bot.register_next_step_handler(info, choose_action)
    else:
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        start_markup.row("Подключить Google-таблицу")
        info = bot.send_message(message.chat.id, "Что хочешь сделать?", reply_markup=start_markup)
        bot.register_next_step_handler(info, choose_action)


if __name__ == "__main__":
    bot.infinity_polling()
