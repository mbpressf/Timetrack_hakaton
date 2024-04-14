<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Facades\File;
use GuzzleHttp\Client;


class PostController extends Controller
{
    public function inproccesTimers()
    {
        $client = new Client();
        $response = $client->request('GET', 'http://miroslavbabk.fvds.ru:3000/get/inprocces');
        
        // Проверяем статус ответа
        if ($response->getStatusCode() == 200) {
            $jsonData = $response->getBody()->getContents();
            $data = json_decode($jsonData, true);
            return view('apiTimers.inprocces', ['data' => $data]);
        } else {
            // Если не удалось получить данные, обработка ошибки
            abort(500, 'Failed to fetch data from remote server.');
        }
    }

    public function completedTimers()
    {
        // Создание клиента Guzzle
        $client = new Client();
    
        try {
            // Выполнение GET запроса к удаленному серверу
            $response = $client->get('http://miroslavbabk.fvds.ru:3000/get/completed');
    
            // Получение содержимого ответа
            $jsonData = $response->getBody()->getContents();
            
            // Декодирование JSON в массив
            $data = json_decode($jsonData, true);
    
            // Передача данных в представление
            return view('apiTimers.completed', ['data' => $data]);
        } catch (\Exception $e) {
            // Обработка ошибок, например, логирование или вывод сообщения об ошибке
            return response()->json(['error' => $e->getMessage()], 500);
        }
    }
}

