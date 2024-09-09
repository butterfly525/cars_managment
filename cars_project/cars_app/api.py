from rest_framework import generics, viewsets, permissions, status
from .models import Car, Comment
from .serializers import CarSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly


# Представление для создания и просмотра записей об автомобилях
class CarListCreateAPIView(generics.ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    # Позволяет добавлять записи в список об автомобилях пользователям с аутентификацией, просматривать можно всем
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# Представление для просмотра, обновления, удаления записи об автомобиле
class CarRetieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    # Позволяет обновлять и удалять информацию об автомобиле только владельцу, просматривать можно всем
    permission_classes = [IsOwnerOrReadOnly]


# Представление для создания и просмотра комментариев
class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # Позволяет добавлять комментарии пользователям с аутентификацией, просматривать можно всем
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Фильтрует набор данных по конкретному автомобилю, о котором пользователь запросил информацию
    def get_queryset(self):
        car_id = self.kwargs['pk']
        return Comment.objects.filter(car_id=car_id)

    # Задает автомобиль, к которому добавляется комментарий
    def perform_create(self, serializer):
        car_id = self.kwargs['pk']
        car = Car.objects.get(id=car_id)
        serializer.save(car=car)