from rest_framework import generics, viewsets, permissions, status
from .models import Car, Comment
from .serializers import CarSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly

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