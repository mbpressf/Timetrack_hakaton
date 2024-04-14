@extends('layouts.app')

@section('content')
    <div class="container mt-5">
        <h1 class="mb-4">Законченные</h1>
    
        @foreach($data['Timers'] as $post)
        <div class="card mb-3">
            <div class="card-body">
                <h5 class="card-title">{{ $post['title'] }}</h5>
                <p class="card-text">{{ $post['description'] }}</p>
                <p class="card-text"><small class="text-muted">Начало: {{ $post['timestamp_start'] }}</small></p>
                <p class="card-text"><small class="text-muted">Конец: {{ $post['timestamp_end'] }}</small></p>
            </div>
        </div>
        @endforeach
    </div>
@endsection