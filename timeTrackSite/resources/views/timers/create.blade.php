@extends('layouts.app')

@section('content')
<div class="container mt-5">
    <h1 class="text-center mb-4">Создание таймера</h1>
    
    <form action="{{ route('timers.store') }}" method="post">
      @csrf
      <div class="mb-3">
        <label for="postTitle" class="form-label">Название</label>
        <input type="text" name="title" class="form-control" id="postTitle" placeholder="Введите название">
      </div>
      <div class="mb-3">
        <label for="postDescription" class="form-label">Описание</label>
        <textarea class="form-control" id="Description" name="description" rows="3" placeholder="Введите описание"></textarea>
      </div>
      <button type="submit" class="btn btn-primary">Создать</button>
    </form>
</div>
@endsection
