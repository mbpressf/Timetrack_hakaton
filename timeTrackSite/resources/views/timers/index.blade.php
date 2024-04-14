@extends('layouts.app')

@section('content')
<div class="container mt-5 row">
    @foreach ($timers as $timer)
    <div class="col">
        <div class="card text-center">
            <div class="card-body">
              <h5 class="card-title">{{ $timer->title }}</h5>
              <p class="card-text">{{ $timer->description }}</p>
              <a href="#" class="btn btn-primary">Подробнее</a>
            </div>
            <div class="card-footer text-muted">
                {{ $timer->created_at->diffForHumans() }}
            </div>
        </div>
    </div>
    @endforeach
</div>
@endsection


