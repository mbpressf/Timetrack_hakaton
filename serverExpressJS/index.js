const express = require('express');
const fs = require('fs');
const bodyParser = require('body-parser');
const path = require('path');


const app = express();
const port = 3000;

// Маршрут обработки корневого URL
app.get('/', (req, res) => {
    res.send('работает');
});

// Разбор JSON тела запроса
app.use(bodyParser.json());

// Маршрут для POST запроса
app.post('/post', (req, res) => {
    // Получаем данные из тела запроса
    const jsonData = req.body;

    // Преобразуем данные в JSON строку
    const jsonString = JSON.stringify(jsonData);

    // Путь к файлу, куда нужно сохранить данные
    const filePath = "json/completed.json";

    // Записываем данные в файл
    fs.writeFile(filePath, jsonString, (err) => {
        if (err) {
            console.error('Ошибка при записи в файл:', err);
            res.status(500).send('Произошла ошибка на сервере');
            return;
        }
        console.log('Данные успешно сохранены в файл');
        res.send('Данные успешно сохранены на сервере');
    });
});

app.get('/get/completed', (req, res) => {
    // Читаем файл example.json
    fs.readFile('json/completed.json', 'utf8', (err, data) => {
        if (err) {
        console.error('Ошибка чтения файла:', err);
        res.status(500).send('Произошла ошибка на сервере');
        return;
        }
        // Отправляем содержимое файла как JSON
        res.json(JSON.parse(data));
    });
});

app.get('/get/inprocces', (req, res) => {
    // Читаем файл example.json
    fs.readFile('json/inprocces.json', 'utf8', (err, data) => {
        if (err) {
        console.error('Ошибка чтения файла:', err);
        res.status(500).send('Произошла ошибка на сервере');
        return;
        }
        // Отправляем содержимое файла как JSON
        res.json(JSON.parse(data));
    });
});


// Слушаем указанный порт
app.listen(port, () => {
  console.log(`Сервер запущен на порту ${port}`);
});
