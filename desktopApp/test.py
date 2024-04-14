from datetime import datetime

# Исходные строки времени
start = "2024-04-13T16:04:28.343116"
end = "2024-04-13T16:04:35.263881"

# Преобразуем строки в объекты datetime
start_dt = datetime.fromisoformat(start)
end_dt = datetime.fromisoformat(end)

# Вычисляем разницу времени
time_diff = end_dt - start_dt

# Выводим разницу времени в секундах
print("Разница времени (в минутах):", time_diff.total_seconds()/60)
