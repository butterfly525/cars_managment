from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, CarForm, CommentForm
from .models import Car, Comment
from .serializers import CarSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.views import APIView
from rest_framework import generics, viewsets, permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
import requests


class CarListCreateAPIView(generics.ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CarRetieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsOwnerOrReadOnly]


class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        car_id = self.kwargs['pk']
        return Comment.objects.filter(car_id=car_id)
        
    def perform_create(self, serializer):
        car_id = self.kwargs['pk']
        car = Car.objects.get(id=car_id)
        serializer.save(car=car)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'cars_app/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
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


def create_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            car = form.save(commit=False)
            car.owner = request.user
            car.save()
            return redirect('my_cars')
    else:
        form = CarForm()
    return render(request, 'cars_app/create_car.html', {'form': form})



def update_car(request, pk):
    car = Car.objects.get(pk=pk)
    # Проверяем, является ли пользователь владельцем автомобиля
    if car.owner != request.user:
        return render(request, 'cars_app/access_denied.html', {'error': 'У вас нет прав на редактирование этого автомобиля.'})
    if request.method == 'POST':
        form = CarForm(request.POST, instance=car)
        if form.is_valid():
            car = form.save(commit=False)
            car.owner = request.user
            car.save()
            return redirect('my_cars')
    else:
        form = CarForm(instance=car)
    return render(request, 'cars_app/update_car.html', {'form': form, 'pk': pk})



def delete_car(request, pk):
    car = Car.objects.get(pk=pk)
    # Проверяем, является ли пользователь владельцем автомобиля
    if car.owner != request.user:
        return render(request, 'cars_app/access_denied.html', {'error': 'У вас нет прав на удаление этого автомобиля.'})
    if request.method == 'POST':
        car.delete()
        return redirect('my_cars')
    return render(request, 'cars_app/confirm_delete.html', {'car': car})


def car_detail(request, pk):
    car = Car.objects.get(pk=pk)
    car_form = CarForm()
    comments = car.comments.order_by('-created_at')
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