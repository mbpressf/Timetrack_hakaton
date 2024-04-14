<?php

// app/Http/Controllers/TimerController.php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Timer;

class TimerController extends Controller
{
    /**
     * Display a listing of the timers.
     *
     * @return \Illuminate\Http\Response
     */
    public function index()
    {
        $timers = Timer::all();
        return view('timers.index', compact('timers'));
    }

    /**
     * Show the form for creating a new timer.
     *
     * @return \Illuminate\Http\Response
     */
    public function create()
    {
        return view('timers.create');
    }

    /**
     * Store a newly created timer in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        $request->validate([
            'title' => 'required', // Поле title обязательно для заполнения
        ]);
    
        $timer = new Timer();
        $timer->title = $request->input('title');
        $timer->description = $request->input('description');
        $timer->created_at = now(); // Текущая дата и время
        $timer->save();
    
        return redirect('/timers');
    }
    
}


