
import requests
import json

# URL вашего сервера Express.js
url = 'http://miroslavbabk.fvds.ru:3000/post'

# # Путь к вашему JSON файлу
# json_file_path = 'post.json'

# # Открываем JSON файл и читаем его содержимое
# with open(json_file_path, 'r') as file:
#     json_data = file.read()
    
    
data = {
   "Timers": {
      "timestamp_start": "2024-04-13T19:59:41.871086",
      "timestamp_end": "2024-04-13T19:59:44.916983",
      "title": "Заголовок 1",
      "description": "Описание таймера"
   }
}


# Отправляем POST запрос на сервер
response = requests.post(url, json=data)

# Печатаем ответ от сервера
print(response.text)
