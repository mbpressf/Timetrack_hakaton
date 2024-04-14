import requests
import json
import schedule
import time
import os

def fetch_and_save_data():
    url_completed = 'http://miroslavbabk.fvds.ru:3000/get/completed'

    try:
        response_completed = requests.get(url_completed)
        if response_completed.status_code == 200:
            # Получаем данные
            data_completed = response_completed.content.decode('unicode-escape')
            print("Полученные данные:", data_completed)  # Добавляем вывод данных
            # Сохраняем данные в файл completed.json с кодировкой UTF-8
            with open('completed.json', 'w', encoding='utf-8') as f:
                json.dump(json.loads(data_completed), f, ensure_ascii=False)

            print("Данные сохранены в файл completed.json")
        else:
            print('Ошибка при запросе:', response_completed.status_code)
    except requests.exceptions.RequestException as e:
        print('Произошла ошибка при запросе:', e)

def check_for_changes():
    # Проверяем, изменился ли файл completed.json
    if os.path.exists('completed.json'):
        with open('completed.json', 'r', encoding='utf-8') as f:
            previous_data = json.load(f)

        fetch_and_save_data()  # Получаем новые данные

        with open('completed.json', 'r', encoding='utf-8') as f:
            current_data = json.load(f)

        if current_data != previous_data:
            os.remove('completed.json')
            print("Данные обновлены и сохранены в новом файле.")
        else:
            print("Данные не изменились.")
    else:
        fetch_and_save_data()  # Если файл отсутствует, получаем новые данные

# Запускаем функцию проверки каждые 10 секунд
schedule.every(10).seconds.do(check_for_changes)

while True:
    schedule.run_pending()
    time.sleep(1)
