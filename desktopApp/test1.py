import telebot
import json
from datetime import datetime
import matplotlib.pyplot as plt
import threading
import time

# Токен вашего бота в Telegram
TOKEN = '5393474663:AAE1MxXDUQLme_oyBKB5UbnlOcy_gcLyRzA'

# Создание объекта бота
bot = telebot.TeleBot(TOKEN)

# Путь к вашему JSON файлу с дополнительными таймерами
ADDITIONAL_JSON_FILE_PATH = 'post.json'

# Путь к вашему JSON файлу с общими таймерами
COMMON_JSON_FILE_PATH = 'common_data.json'

# Функция для построения диаграммы
def plot_timers(timers):
    titles = []
    times = []
    for timer in timers:
        start_time = datetime.fromisoformat(timer.get('timestamp_start'))
        end_time = datetime.fromisoformat(timer.get('timestamp_end'))
        time_diff_minutes = (end_time - start_time).total_seconds() / 60  # переводим секунды в минуты
        times.append(time_diff_minutes)
        titles.append(timer.get('title'))

    plt.figure(figsize=(10, 6))
    plt.barh(titles, times, color='skyblue')
    plt.xlabel('Потраченное время (минуты)')
    plt.ylabel('Заголовок таймера')
    plt.title('Потраченное время на каждый таймер')
    plt.gca().invert_yaxis()
    plt.savefig('timers_plot.png')

# Функция для загрузки таймеров из файла JSON
def load_timers_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            timers = json.load(file).get('timers', [])
    except FileNotFoundError:
        timers = []
    return timers

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

        time.sleep(5)  # Пауза на 15 секунд

# Запуск потока обновления таймеров
update_thread = threading.Thread(target=update_common_timers)
update_thread.start()

# Функция для обработки команды /summary
@bot.message_handler(commands=['summary'])
def send_summary(message):
    # Загрузка таймеров из общего JSON файла
    common_timers = load_timers_from_file(COMMON_JSON_FILE_PATH)

    # Отправка сводки
    summary_text = ""
    for timer in common_timers:
        start_time = datetime.fromisoformat(timer.get('timestamp_start'))
        end_time = datetime.fromisoformat(timer.get('timestamp_end'))
        time_diff = end_time - start_time
        spent_time = f"{time_diff.seconds // 3600} часов, {(time_diff.seconds // 60) % 60} минут и {time_diff.seconds % 60} секунд"
        timer_summary = f"Заголовок: {timer.get('title')}\nОписание: {timer.get('description')}\nПотраченное время: {spent_time}\n\n"
        summary_text += timer_summary

    bot.reply_to(message, summary_text)

    # Построение и отправка диаграммы
    plot_timers(common_timers)
    with open('timers_plot.png', 'rb') as plot:
        bot.send_photo(message.chat.id, plot)

# Функция для запуска бота
def run_bot():
    bot.polling()

if __name__ == "__main__":
    run_bot()