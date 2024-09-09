from . import views
# from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include, re_path

urlpatterns = [    
    # Основные маршруты
    path('cars/', views.index, name='index'),
    path('home/', views.home, name='home'),
    
    # Маршруты для аутентификации
    path('login/', views.login_view, name='login_site'),
    path('logout/', views.logout_view, name='logout_site'),
    path('register/', views.register, name='register_site'),
    
    # Маршруты для автомобилей
    path('cars/my/', views.my_cars, name='my_cars'),
    path('cars/create/', views.create_car, name='create_car'),
    path('cars/update/<int:pk>/', views.update_car, name='update_car'),
    path('cars/delete/<int:pk>/', views.delete_car, name='delete_car'),

    # Маршруты для комментариев
    path('comments/<int:pk>/', views.car_detail, name='car_detail'),
    
    # API маршруты
    path('api/cars/', views.CarListCreateAPIView.as_view(), name='car-list'), # Для чтения списка записей об автомобилях и добавления новой записи
    path('api/cars/<int:pk>/', views.CarRetieveUpdateDestroyAPIView.as_view()),  # Для чтения, обновления и удаления конкретного автомобиля
    path('api/cars/<int:pk>/comments/', views.CommentListCreateAPIView.as_view()),  # Для чтения и добавления комментариев к конкретному автомобилю
    path('api/auth/', include('rest_framework.urls')), # Для авторизации по логину и паролю в аминистративной панели API django
    path('api/auth/', include('djoser.urls')), # Стандартные эндпоинты Djoser для аутентификации и авторизации
    re_path(r'^api/auth/', include('djoser.urls.authtoken'))   # Для поддержки токенов аутентификации
    
] 