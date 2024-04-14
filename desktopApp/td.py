from time import monotonic
from plyer import notification
from datetime import datetime, timedelta
import json
import paramiko

import pyautogui
import time
import requests

from log import *

from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.reactive import reactive
from textual.widgets import Button, Footer, Header, Static

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timedelta

host = host
port = 22
username = username
password = password

class TimeDisplay(Static):
    """A widget to display elapsed time."""
    start_time = reactive(monotonic)
    time = reactive(0.0)
    total = reactive(0.0)
    

    def on_mount(self) -> None:
        """Event handler called when widget is added to the app."""
        self.update_timer = self.set_interval(1 / 60, self.update_time, pause=True)

    def update_time(self) -> None:
        """Method to update time to current."""
        self.time = self.total + (monotonic() - self.start_time)

    def watch_time(self, time: float) -> None:
        """Called when the time attribute changes."""
        minutes, seconds = divmod(time, 60)
        hours, minutes = divmod(minutes, 60)
        self.update(f"{hours:02,.0f}:{minutes:02.0f}:{seconds:05.2f}")

    def start(self) -> None:
        """Method to start (or resume) time updating."""
        self.start_time = monotonic()
        self.update_timer.resume()
        
        self.start_time_t = datetime.now()
        
        
        notification.notify(
            title='Предупреждение',
            message='Таймер стартовал!',
            app_icon=None,  # Путь к иконке (может быть None)
            timeout=10,  # Время отображения уведомления в секундах
        )


    def stop(self):
        """Method to stop the time display updating."""
        self.update_timer.pause()
        self.total += monotonic() - self.start_time
        self.time = self.total
        
        self.end_time_t = datetime.now()
        
        
        
        data = {
            "Timers": [
                {
                    "timestamp_start": self.start_time_t.isoformat(),
                    "timestamp_end" : self.end_time_t.isoformat(),
                    "title" : "Таймер 1",
                    "description" : "Таймер для работы"
                }
                ]
            }
            


        
        url = 'http://miroslavbabk.fvds.ru:3000/post'
        
        
        with open('post.json', 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=3)
            
        # Отправляем POST запрос на сервер
        response = requests.post(url, json=data)

        # Печатаем ответ от сервера
        print(response.text)
  
            
        # Указываем область календаря, в котором хотим создать событие
        calendar_id = 'primary'


        # Устанавливаем данные для нового события
        event = {
            'summary': 'Таймер 1',
            'description': 'Описание таймера',
            'start': {
                'dateTime': self.start_time_t.strftime('%Y-%m-%dT%H:%M:%S'),  # Формат ISO 8601 для начала события
                'timeZone': 'Europe/Moscow',  # Укажите ваш часовой пояс здесь
            },
            'end': {
                'dateTime': self.end_time_t.strftime('%Y-%m-%dT%H:%M:%S'),  # Формат ISO 8601 для окончания события
                'timeZone': 'Europe/Moscow',  # Укажите ваш часовой пояс здесь
            },
        }
        

        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', ['https://www.googleapis.com/auth/calendar'])
        creds = flow.run_local_server(port=0)

        # Создание клиента для работы с Google Календарем
        service = build('calendar', 'v3', credentials=creds)

        # Создание события
        event = service.events().insert(calendarId=calendar_id, body=event).execute()
        
    
        
        transport = paramiko.Transport((host, port))
        transport.connect(username=username, password=password)

        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put('post.json', '/var/www/html/post.json')
        sftp.close()

        
        
        self.total = 0
        self.time = 0
        

    def reset(self):
        pass


class Stopwatch(Static):
    """A stopwatch widget."""

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        button_id = event.button.id
        time_display = self.query_one(TimeDisplay)
        if button_id == "start":
            time_display.start()
            
            
            self.add_class("started")
        elif button_id == "stop":
            time_display.stop()
            self.remove_class("started")
        elif button_id == "reset":
            time_display.reset()

    def compose(self) -> ComposeResult:
        """Create child widgets of a stopwatch."""
        yield Button("Start", id="start", variant="success")
        yield Button("Stop", id="stop", variant="error")
        yield Button("Reset", id="reset")
        yield TimeDisplay()

class StopwatchApp(App):
    """A Textual app to manage stopwatches."""

    CSS_PATH = "stopwatch.tcss"

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("a", "add_stopwatch", "Add"),
        ("r", "remove_stopwatch", "Remove"),
    ]

    def compose(self) -> ComposeResult:
        """Called to add widgets to the app."""
        yield Header()
        yield Footer()
        yield ScrollableContainer(Stopwatch(), Stopwatch(), Stopwatch(), id="timers")

    def action_add_stopwatch(self) -> None:
        """An action to add a timer."""
        new_stopwatch = Stopwatch()
        self.query_one("#timers").mount(new_stopwatch)
        new_stopwatch.scroll_visible()

    def action_remove_stopwatch(self) -> None:
        """Called to remove a timer."""
        timers = self.query("Stopwatch")
        if timers:
            timers.last().remove()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark



if __name__ == "__main__":
    app = StopwatchApp()
    app.run()
