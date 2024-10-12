from .views import * 
from django.urls import path, include, re_path

urlpatterns = [    
    # Основные маршруты
    path('', index, name='index'),
    path('home/', home, name='home'),
    
    # Маршруты для аутентификации
    path('login/', login_view, name='login_site'),
    path('logout/', logout_view, name='logout_site'),
    path('register/', register, name='register_site'),
    
    # Маршруты для автомобилей
    path('cars/my/', my_cars, name='my_cars'),
    path('cars/create/', CarCreateView.as_view(), name='create_car'),
    path('cars/update/<int:pk>/', CarUpdateView.as_view(), name='update_car'),
    path('cars/delete/<int:pk>/', CarDeleteView.as_view(), name='delete_car'),

    # Маршруты для комментариев
    path('comments/<int:pk>/', CarDetailView.as_view(), name='car_detail'),
    
    # API маршруты
    path('api/cars/', CarListCreateAPIView.as_view(), name='car-list'), # Для чтения списка записей об автомобилях и добавления новой записи
    path('api/cars/<int:pk>/', CarRetieveUpdateDestroyAPIView.as_view()),  # Для чтения, обновления и удаления конкретного автомобиля
    path('api/cars/<int:pk>/comments/', CommentListCreateAPIView.as_view()),  # Для чтения и добавления комментариев к конкретному автомобилю
    path('api/auth/', include('rest_framework.urls')), # Для авторизации по логину и паролю в аминистративной панели API django
    path('api/auth/', include('djoser.urls')), 
    re_path(r'^api/auth/', include('djoser.urls.authtoken'))   # Стандартные эндпоинты Djoser для аутентификации и авторизации, в том числе и по токенам
] 


