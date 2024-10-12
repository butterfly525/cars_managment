from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CarForm, CommentForm
from .api import *
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_site')
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

def page_not_found(request, exception):
    return render(request, 'cars_app/404.html', status=404)

# Создание записи об автомобиле
class CarCreateView(LoginRequiredMixin, CreateView):
    model = Car
    form_class = CarForm
    template_name = 'cars_app/create_car.html'
    success_url = reverse_lazy('my_cars')
    extra_context = {
        'title': 'Добавление автомобиля'
    }
    def form_valid(self, form):
        car = form.save(commit=False)
        car.owner = self.request.user
        return super().form_valid(form)


# Обновление записи об автомобиле
class CarUpdateView(LoginRequiredMixin, UpdateView):
    model = Car
    form_class = CarForm
    template_name = 'cars_app/create_car.html'
    success_url = reverse_lazy('my_cars')
    extra_context = {
        'title': 'Редактирование автомобиля'
    }
    def dispatch(self, request, *args, **kwargs):
        self.car = self.get_object()
        if self.car.owner != request.user:
            return render(request, 'cars_app/access_denied.html', {'error': 'У вас нет прав на редактирование этого автомобиля.'})
        return super().dispatch(request, *args, **kwargs)


class CarDeleteView(LoginRequiredMixin, DeleteView):
    model = Car
    template_name = 'cars_app/delete_car.html'
    success_url = reverse_lazy('my_cars')
    extra_context = {
        'title': 'Подтвердите удаление автомобиля'
    }
    def get(self, request, *args, **kwargs):
        car = self.get_object()
        if car.owner != request.user:
            return render(request, 'cars_app/access_denied.html', {'error': 'У вас нет прав на удаление этого автомобиля.'})
        return super().get(request, *args, **kwargs)

# Удаление записи об автомобиле
# def delete_car(request, pk):
#     car = Car.objects.get(pk=pk)
#     # Проверка на владельца записи об автомобиле
#     if car.owner != request.user:
#         return render(request, 'cars_app/access_denied.html', {'error': 'У вас нет прав на удаление этого автомобиля.'})
#     if request.method == 'POST':
#         car.delete()
#         return redirect('my_cars')
#     return render(request, 'cars_app/confirm_delete.html', {'car': car})


class CarDetailView(View):
    template_name = 'cars_app/car_detail.html'

    def get(self, request, pk):
        car = Car.objects.get(pk=pk)
        comments = car.comments.all()
        comment_form = CommentForm()
        return render(request, self.template_name, {
            'car': car,
            'comments': comments,
            'comment_form': comment_form,
        })
    
    def post(self, request, pk):
        car = Car.objects.get(pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.car = car
            comment.author = request.user
            comment.save()
            # Перенаправляем обратно на детальную страницу автомобиля
            return redirect(f'/comments/{pk}/')
        return render(request, self.template_name, {
            'car': car,
            'comments': car.comments.all(),
            'comment_form': form,
        })

def car_detail(request, pk):
    car = Car.objects.get(pk=pk)
    comments = car.comments.all()
    comment_form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.car = car
            comment.author = request.user
            comment.save()
            # Перенаправляем обратно на детальную страницу автомобиля
            return redirect(f'/comments/{pk}/')

    return render(request, 'cars_app/car_detail.html', {
        'car': car,
        'comments': comments,
        'comment_form': comment_form,
    })
