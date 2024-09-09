from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CarForm, CommentForm
from .api import *
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'cars_app/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm(request)
    
    return render(request, 'cars_app/login.html', {'form': form})



@login_required
def logout_view(request):
    logout(request)
    return redirect('index')


def index(request):
    cars = Car.objects.all()
    return render(request, 'cars_app/index.html', {'cars': cars})


def home(request):
    return render(request, 'cars_app/home.html')


@login_required
def my_cars(request):
    user = request.user
    cars = Car.objects.filter(owner=user)
    return render(request, 'cars_app/my_cars.html', {'cars': cars})



# Создание записи об автомобиле
def create_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            car = form.save(commit=False)
            # Текущий пользователь становится автором записи
            car.owner = request.user
            car.save()
            return redirect('my_cars')
    else:
        form = CarForm()
    return render(request, 'cars_app/create_car.html', {'form': form})


# Обновление записи об автомобиле
def update_car(request, pk):
    car = Car.objects.get(pk=pk)
    if request.method == 'POST':
        # Проверка на владельца записи об автомобиле
        if car.owner != request.user:
            return render(request, 'cars_app/access_denied.html', {'error': 'У вас нет прав на редактирование этого автомобиля.'})
        form = CarForm(request.POST, instance=car)
        if form.is_valid():
            form.save()
            return redirect('my_cars')
    else:
        form = CarForm(instance=car)
    return render(request, 'cars_app/update_car.html', {'form': form, 'pk': pk})


# Удаление записи об автомобиле
def delete_car(request, pk):
    car = Car.objects.get(pk=pk)
    # Проверка на владельца записи об автомобиле
    if car.owner != request.user:
        return render(request, 'cars_app/access_denied.html', {'error': 'У вас нет прав на удаление этого автомобиля.'})
    if request.method == 'POST':
        car.delete()
        return redirect('my_cars')
    return render(request, 'cars_app/confirm_delete.html', {'car': car})


def car_detail(request, pk):
    car = Car.objects.get(pk=pk)
    car_form = CarForm()
    comments = car.comments.all()
    comment_form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.car = car
            comment.author = request.user
            comment.save()
            return redirect(f'/comments/{pk}/')  # Перенаправляем обратно на детальную страницу автомобиля

    return render(request, 'cars_app/car_detail.html', {
        'car': car,
        'comments': comments,
        'comment_form': comment_form,
    })