import requests
import json

# URL вашего сервера Express.js
url = 'http://miroslavbabk.fvds.ru:3000/post'

# JSON данные, которые вы хотите отправить
data = {
    'key1': 'value1',
    'key2': 'value2'
}

# Преобразуем данные в JSON формат
json_data = json.dumps(data)

# Отправляем POST запрос на сервер
response = requests.post(url, json=json_data)

# Печатаем ответ от сервера
print(response.text)
