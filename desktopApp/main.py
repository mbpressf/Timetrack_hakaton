from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timedelta

# Указываем область календаря, в котором хотим создать событие
calendar_id = 'primary'

# Устанавливаем область даты и времени события

########
start_time = datetime.now()
end_time = start_time + timedelta(hours=1)
########

# Устанавливаем данные для нового события
event = {
  'summary': 'Название события',
  'description': 'Описание события',
  'start': {
    'dateTime': start_time.strftime('%Y-%m-%dT%H:%M:%S'),  # Формат ISO 8601 для начала события
    'timeZone': 'Europe/Moscow',  # Укажите ваш часовой пояс здесь
  },
  'end': {
    'dateTime': end_time.strftime('%Y-%m-%dT%H:%M:%S'),  # Формат ISO 8601 для окончания события
    'timeZone': 'Europe/Moscow',  # Укажите ваш часовой пояс здесь
  },
}

flow = InstalledAppFlow.from_client_secrets_file('credentials.json', ['https://www.googleapis.com/auth/calendar'])
creds = flow.run_local_server(port=0)

# Создание клиента для работы с Google Календарем
service = build('calendar', 'v3', credentials=creds)

# Создание события
event = service.events().insert(calendarId=calendar_id, body=event).execute()
