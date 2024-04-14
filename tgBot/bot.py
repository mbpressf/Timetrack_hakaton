import telebot
import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import threading
import time
import calendar
import os
import numpy as np

        # Сюда токен от @BotFather 
        #  |
        #  |
        # \/
TOKEN = '7079335167:AAFfk0JnUBDnE2AXXlngrERfrxWeYZI6dyw'

# Создание объекта бота
bot = telebot.TeleBot(TOKEN)

# Путь к вашему JSON файлу с дополнительными таймерами
ADDITIONAL_JSON_FILE_PATH = 'to.json'

# Путь к вашему JSON файлу с общими таймерами
COMMON_JSON_FILE_PATH = 'common_data.json'



# Текст описания бота
start_message = """
Привет! 👋 Я - бот для контроля за проектом. Моя задача - помочь вам отслеживать, сколько времени вы тратите на различные задачи и проекты. 🕒

Чтобы начать использовать меня, просто добавьте информацию о ваших таймерах, а я буду следить за временем за вас! 🚀

Используйте команду /summary, чтобы получить сводку о потраченном времени 💼.
"""

# Обработка команды /start
@bot.message_handler(commands=['start'])
def send_start(message):
    bot.reply_to(message, start_message)



"""
Эта часть кода подгружает данные новых таймеров, получаемых с приложения.
"""



# Функция для загрузки таймеров из файла JSON
def load_timers_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            timer_data = json.load(file)
            if 'Timer' in timer_data:
                return [timer_data['Timer']]  # Если файл содержит только один таймер, то возвращаем его в списке
            else:
                return timer_data.get('timers', [])
    except FileNotFoundError:
        return []

# Функция для записи уникальных таймеров в файл JSON
def write_unique_timers_to_file(unique_timers, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump({'timers': unique_timers}, file, ensure_ascii=False, indent=4)

# Функция для обновления общего файла с таймерами
def update_common_timers():
    while True:
        # Загрузка таймеров из дополнительного JSON файла
        additional_timers = load_timers_from_file(ADDITIONAL_JSON_FILE_PATH)
        
        # Загрузка таймеров из общего JSON файла
        common_timers = load_timers_from_file(COMMON_JSON_FILE_PATH)

        # Добавление уникальных таймеров из дополнительного файла в общий файл
        for timer in additional_timers:
            if timer not in common_timers:
                common_timers.append(timer)

        # Запись уникальных таймеров в общий файл
        write_unique_timers_to_file(common_timers, COMMON_JSON_FILE_PATH)

        time.sleep(3)  # Пауза на 3 секунды

# Запуск потока обновления таймеров
update_thread = threading.Thread(target=update_common_timers)
update_thread.start()



# Функция для отправки сообщения с диаграммой
def send_message_with_chart(message, text, image_path):
    try:
        with open(image_path, 'rb') as image:
            bot.send_photo(message.chat.id, image, caption=text)
    except Exception as e:
        send_message_with_html(message, text)

# Функция для отправки HTML-файла с подробной сводкой
def send_message_with_html(message, text):
    with open('summary.html', 'w', encoding='utf-8') as file:
        file.write(text)

    with open('summary.html', 'rb') as file:
        bot.send_document(message.chat.id, file)





"""
Эта часть формирует диаграмму и html файл для общей статистике получаемой по команде /summary
"""



import matplotlib.pyplot as plt
import numpy as np

# Функция для построения столбовой диаграммы
def plot_timers_bar(timers):
    titles = [timer.get('title') for timer in timers]
    times = [int((datetime.fromisoformat(timer.get('timestamp_end')) - datetime.fromisoformat(timer.get('timestamp_start'))).total_seconds() // 60) for timer in timers]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(titles, times, color='#00ffff')  # Цвет столбцов
    plt.xlabel('Заголовок таймера', color='#00ffff')  # Цвет текста
    plt.ylabel('Потраченное время (минуты)', color='#00ffff')  # Цвет текста
    plt.title('Потраченное время на каждый таймер', color='#00ffff')  # Цвет текста
    plt.xticks(rotation=45, ha='right', color='#00ffff')  # Цвет текста
    plt.gca().set_facecolor('#162938')  # Цвет фона

    # Цвет границ
    plt.gca().spines['top'].set_color('#00ffff')
    plt.gca().spines['bottom'].set_color('#00ffff')
    plt.gca().spines['left'].set_color('#00ffff')
    plt.gca().spines['right'].set_color('#00ffff')

    # Цвет черточек (тиков) на осях X и Y
    plt.tick_params(axis='x', colors='#00ffff')
    plt.tick_params(axis='y', colors='#00ffff')

    plt.yticks(color='#00ffff')  # Цвет текста по оси Y
    plt.tight_layout()
    plt.savefig('timers_plot_bar.png', facecolor='#162938')  # Цвет фона

# Функция для обработки команды /summary
@bot.message_handler(commands=['summary'])
def send_summary(message):
    # Загрузка таймеров из общего JSON файла
    common_timers = load_timers_from_file(COMMON_JSON_FILE_PATH)

    # Подготовка сводки в виде HTML-таблицы
    summary_text = "<style>body {background-color: #162938; color: #00ffff;} \
    table {font-family: Arial, sans-serif; border-collapse: collapse; width: 80%; background-color: #162938; color: #00ffff;} \
    th {background-color: #162938; color: #00ffff; font-weight: bold;} \
    td, th {border: 1px solid #00ffff; padding: 8px;} \
    tr:nth-child(even) {background-color:#162938;} \
    tr:nth-child(odd) {background-color: #162938;} </style>"
    summary_text += "<br><br><table border='1'><tr><th>Заголовок таймера</th><th>Описание</th><th>Потраченное время</th></tr>"
    
    for timer in common_timers:
        start_time = datetime.fromisoformat(timer.get('timestamp_start'))
        end_time = datetime.fromisoformat(timer.get('timestamp_end'))
        time_diff = end_time - start_time
        spent_time = f"{time_diff.seconds // 60} минут"  # выводим время в минутах
        timer_summary = f"<tr><td>{timer.get('title')}</td><td>{timer.get('description')}</td><td>{spent_time}</td></tr>"
        summary_text += timer_summary
    summary_text += "</table>"

    try:
        # Попытка отправить текстовую сводку
        bot.reply_to(message, summary_text)

        # Построение и отправка столбовой диаграммы
        plot_timers_bar(common_timers)
        with open('timers_plot_bar.png', 'rb') as plot:
            bot.send_photo(message.chat.id, plot)
    except telebot.apihelper.ApiTelegramException as e:
        # Если текстовое сообщение слишком длинное, отправляем HTML файл
        html_content = f"<b>Сводка:</b><br>{summary_text}"
        bot.send_message(message.chat.id, "Сводка слишком длинная. Отправляю в виде HTML файла.")
        with open('summary.html', 'w', encoding='utf-8') as html_file:
            html_file.write(html_content)
        # Отправка HTML файла
        with open('summary.html', 'rb') as html_file:
            bot.send_document(message.chat.id, html_file, caption='Сводка в формате HTML')


        # Построение и отправка столбовой диаграммы в виде отдельного изображения
        plot_timers_bar(common_timers)
        with open('timers_plot_bar.png', 'rb') as plot:
            bot.send_photo(message.chat.id, plot)
        


"""
Эта часть формирует диаграмму и сводку получаемой по команде /weekly_stats
"""



# Функция для построения столбовой диаграммы за последние 7 дней
def plot_weekly_stats(timers):
    # Словарь для хранения данных за каждый день
    daily_stats = {}

    # Находим понедельник текущей недели
    today = datetime.now().date()
    monday = today - timedelta(days=today.weekday())

    # Заполнение словаря начальными значениями
    for i in range(7):
        date = monday + timedelta(days=i)
        daily_stats[date] = 0

    # Подсчет времени для каждого дня
    for timer in timers:
        end_time = datetime.fromisoformat(timer.get('timestamp_end')).date()
        if monday <= end_time <= today:
            daily_stats[end_time] += (datetime.fromisoformat(timer.get('timestamp_end')) - datetime.fromisoformat(timer.get('timestamp_start'))).total_seconds() / 60

    # Сортировка данных по дате
    sorted_daily_stats = sorted(daily_stats.items())

    # Разделение данных на даты и значения времени
    dates, times = zip(*sorted_daily_stats)

    # Получение дней недели для каждой даты
    weekdays = [calendar.day_name[date.weekday()] for date in dates]

    # Построение столбовой диаграммы
    plt.figure(figsize=(10, 6))
    bars = plt.bar(weekdays, times, color='#00ffff')  # Цвет столбцов
    plt.xlabel('День недели', color='#00ffff')  # Цвет текста
    plt.ylabel('Потраченное время (минуты)', color='#00ffff')  # Цвет текста
    plt.title('Потраченное время за последние 7 дней', color='#00ffff')  # Цвет текста
    plt.xticks(rotation=45, color='#00ffff')  # Поворот подписей по оси X для лучшей читаемости, цвет текста
    plt.tight_layout()  # Улучшение расположения подписей

    # Цвет черточек (тиков) на осях X и Y
    plt.tick_params(axis='x', colors='#00ffff')
    plt.tick_params(axis='y', colors='#00ffff')

    # Цвет фона графика
    plt.gca().set_facecolor('#162938')

    # Изменение цвета границ
    for spine in plt.gca().spines.values():
        spine.set_color('#00ffff')

    # Сохранение диаграммы в файл
    plt.savefig('weekly_stats_plot.png', facecolor='#162938')  # Цвет фона

# Функция для обработки команды /weekly_stats
@bot.message_handler(commands=['weekly_stats'])
def weekly_stats(message):
    # Загрузка таймеров из общего JSON файла
    common_timers = load_timers_from_file(COMMON_JSON_FILE_PATH)

    # Фильтрация таймеров за последнюю неделю
    last_week_timers = []
    for timer in common_timers:
        end_time = datetime.fromisoformat(timer.get('timestamp_end')).date()
        if datetime.now().date() - timedelta(days=7) <= end_time <= datetime.now().date():
            last_week_timers.append(timer)

    # Если таймеров за последнюю неделю нет
    if not last_week_timers:
        bot.reply_to(message, "За последнюю неделю не было активировано ни одного таймера.")
        return

    # Построение статистики за последнюю неделю
    total_time_minutes = sum([(datetime.fromisoformat(timer.get('timestamp_end')) - datetime.fromisoformat(timer.get('timestamp_start'))).total_seconds() / 60 for timer in last_week_timers])
    average_time_minutes = total_time_minutes / len(last_week_timers)

    # Отправка статистики
    bot.reply_to(message, f"За последнюю неделю было активировано {len(last_week_timers)} таймеров.\nОбщее потраченное время: {total_time_minutes:.2f} минут.\nСреднее время активации таймера: {average_time_minutes:.2f} минут.")

    # Построение столбовой диаграммы
    plot_weekly_stats(last_week_timers)

    # Отправка столбовой диаграммы
    with open('weekly_stats_plot.png', 'rb') as plot:
        bot.send_photo(message.chat.id, plot)



"""
Эта часть формирует диаграмму и сводку получаемой по команде /monthly_stats
"""



# Функция для построения столбовой диаграммы за последний месяц
def plot_monthly_stats(timers):
    # Словарь для хранения данных за каждый день
    daily_stats = {}

    # Находим первый день текущего месяца
    today = datetime.now().date()
    first_day_of_month = today.replace(day=1)

    # Определяем последний день месяца
    _, last_day_of_month = calendar.monthrange(today.year, today.month)

    # Заполнение словаря начальными значениями
    for i in range(1, last_day_of_month + 1):
        date = first_day_of_month + timedelta(days=i - 1)
        daily_stats[date] = 0

    # Подсчет времени для каждого дня
    for timer in timers:
        end_time = datetime.fromisoformat(timer.get('timestamp_end')).date()
        if first_day_of_month <= end_time <= today:
            daily_stats[end_time] += (datetime.fromisoformat(timer.get('timestamp_end')) - datetime.fromisoformat(timer.get('timestamp_start'))).total_seconds() / 60

    # Сортировка данных по дате
    sorted_daily_stats = sorted(daily_stats.items())

    # Разделение данных на даты и значения времени
    dates, times = zip(*sorted_daily_stats)

    # Получение дней месяца для каждой даты
    month_days = [date.day for date in dates]

        # Построение столбовой диаграммы
    plt.figure(figsize=(10, 6))
    bars = plt.bar(month_days, times, color='#00ffff')  # Цвет столбцов
    plt.xlabel('День месяца', color='#00ffff')  # Цвет текста
    plt.ylabel('Потраченное время (минуты)', color='#00ffff')  # Цвет текста
    plt.title('Потраченное время за текущий месяц', color='#00ffff')  # Цвет текста
    plt.xticks(month_days, color='#00ffff')  # Устанавливаем дни месяца на оси X, цвет текста
    plt.tight_layout()  # Улучшение расположения подписей

    # Цвет черточек (тиков) на осях X и Y
    plt.tick_params(axis='x', colors='#00ffff')
    plt.tick_params(axis='y', colors='#00ffff')

    # Цвет фона графика
    plt.gca().set_facecolor('#162938')

    # Изменение цвета границ
    for spine in plt.gca().spines.values():
        spine.set_color('#00ffff')

    # Сохранение диаграммы в файл
    plt.savefig('monthly_stats_plot.png', facecolor='#162938')  # Цвет фона


# Функция для обработки команды /monthly_stats
@bot.message_handler(commands=['monthly_stats'])
def monthly_stats(message):
    # Загрузка таймеров из общего JSON файла
    common_timers = load_timers_from_file(COMMON_JSON_FILE_PATH)

    # Фильтрация таймеров за последний месяц
    last_month_timers = []
    for timer in common_timers:
        end_time = datetime.fromisoformat(timer.get('timestamp_end')).date()
        if datetime.now().date().replace(day=1) <= end_time <= datetime.now().date():
            last_month_timers.append(timer)

    # Если таймеров за последний месяц нет
    if not last_month_timers:
        bot.reply_to(message, "За последний месяц не было активировано ни одного таймера.")
        return

    # Построение статистики за последний месяц
    total_time_minutes = sum([(datetime.fromisoformat(timer.get('timestamp_end')) - datetime.fromisoformat(timer.get('timestamp_start'))).total_seconds() / 60 for timer in last_month_timers])
    average_time_minutes = total_time_minutes / len(last_month_timers)

    # Отправка статистики
    bot.reply_to(message, f"За последний месяц было активировано {len(last_month_timers)} таймеров.\nОбщее потраченное время: {total_time_minutes:.2f} минут.\nСреднее время активации таймера: {average_time_minutes:.2f} минут.")

    # Построение столбовой диаграммы
    plot_monthly_stats(last_month_timers)

    # Отправка столбовой диаграммы
    with open('monthly_stats_plot.png', 'rb') as plot:
        bot.send_photo(message.chat.id, plot)


# Функция для построения столбовой диаграммы за указанный месяц
def plot_monthly_stats_for_period(timers, start_date, end_date):
    # Словарь для хранения данных за каждый день
    daily_stats = {}

    # Заполнение словаря начальными значениями
    current_date = start_date
    while current_date <= end_date:
        daily_stats[current_date] = 0
        current_date += timedelta(days=1)

    # Подсчет времени для каждого дня
    for timer in timers:
        end_time = datetime.fromisoformat(timer.get('timestamp_end')).date()
        if start_date <= end_time <= end_date:
            daily_stats[end_time] += (datetime.fromisoformat(timer.get('timestamp_end')) - datetime.fromisoformat(timer.get('timestamp_start'))).total_seconds() / 60

    # Сортировка данных по дате
    sorted_daily_stats = sorted(daily_stats.items())

    # Разделение данных на даты и значения времени
    dates, times = zip(*sorted_daily_stats)

    # Получение дней месяца для каждой даты
    month_days = [date.day for date in dates]

    import matplotlib.pyplot as plt

    # Построение столбовой диаграммы
    plt.figure(figsize=(10, 6))
    bars = plt.bar(month_days, times, color='#00ffff')  # Цвет столбцов
    plt.xlabel('День месяца', color='#00ffff')  # Цвет текста
    plt.ylabel('Потраченное время (минуты)', color='#00ffff')  # Цвет текста
    plt.title(f'Потраченное время за {start_date.strftime("%B %Y")}', color='#00ffff')  # Цвет текста
    plt.xticks(month_days, color='#00ffff')  # Устанавливаем дни месяца на оси X, цвет текста
    plt.tight_layout()  # Улучшение расположения подписей

    # Цвет черточек (тиков) на осях X и Y
    plt.tick_params(axis='x', colors='#00ffff')
    plt.tick_params(axis='y', colors='#00ffff')

    # Цвет фона графика
    plt.gca().set_facecolor('#162938')

    # Изменение цвета границ
    for spine in plt.gca().spines.values():
        spine.set_color('#00ffff')

    # Сохранение диаграммы в файл
    plt.savefig('monthly_stats_plot.png', facecolor='#162938')  # Цвет фона




"""
Эта часть формирует диаграмму и сводку получаемой по команде /last_month_stats
"""



# Функция для обработки команды /last_month_stats
@bot.message_handler(commands=['last_month_stats'])
def last_month_stats(message):
    # Загрузка таймеров из общего JSON файла
    common_timers = load_timers_from_file(COMMON_JSON_FILE_PATH)

    # Определение первого и последнего дня прошлого месяца
    today = datetime.now().date()
    last_day_of_last_month = today.replace(day=1) - timedelta(days=1)
    first_day_of_last_month = last_day_of_last_month.replace(day=1)

    # Фильтрация таймеров за прошлый месяц
    last_month_timers = []
    for timer in common_timers:
        end_time = datetime.fromisoformat(timer.get('timestamp_end')).date()
        if first_day_of_last_month <= end_time <= last_day_of_last_month:
            last_month_timers.append(timer)

    # Если таймеров за прошлый месяц нет
    if not last_month_timers:
        bot.reply_to(message, "За прошлый месяц не было активировано ни одного таймера.")
        return

    # Построение статистики за прошлый месяц
    total_time_minutes = sum([(datetime.fromisoformat(timer.get('timestamp_end')) - datetime.fromisoformat(timer.get('timestamp_start'))).total_seconds() / 60 for timer in last_month_timers])
    average_time_minutes = total_time_minutes / len(last_month_timers)

    # Отправка статистики
    bot.reply_to(message, f"За прошлый месяц было активировано {len(last_month_timers)} таймеров.\nОбщее потраченное время: {total_time_minutes:.2f} минут.\nСреднее время активации таймера: {average_time_minutes:.2f} минут.")

    # Построение столбовой диаграммы
    plot_monthly_stats_for_period(last_month_timers, first_day_of_last_month, last_day_of_last_month)

    # Отправка столбовой диаграммы
    with open('monthly_stats_plot.png', 'rb') as plot:
        bot.send_photo(message.chat.id, plot)



# Обработка неизвестных команд
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Я пока не знаю, что делать с этой командой.")

# Функция для запуска бота
def run_bot():
    bot.polling()

if __name__ == "__main__":
    run_bot()
