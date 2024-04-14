from plyer import notification

notification.notify(
    title='Предупреждение',
    message='...',
    app_icon=None,  # Путь к иконке (может быть None)
    timeout=10,  # Время отображения уведомления в секундах
)
