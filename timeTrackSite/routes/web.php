<?php

use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider and all of them will
| be assigned to the "web" middleware group. Make something great!
|
*/

use App\Http\Controllers\PostController;
use App\Http\Controllers\TimerController;

Route::get('/timers', [TimerController::class, 'index'])->name('timers.index');
Route::get('/timers/create', [TimerController::class, 'create'])->name('timers.create');
Route::post('/timers', [TimerController::class, 'store'])->name('timers.store');

Route::get('/completed', [PostController::class, 'completedTimers'])->name('timers.completed');
Route::get('/inprocces', [PostController::class, 'inproccesTimers'])->name('timers.inprocces');





