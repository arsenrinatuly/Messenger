<<<<<<< HEAD
from django.shortcuts import render

# Create your views here.
=======
# apps/images/views.py

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound
from .models import Images
from .serializators import ImagesSerializer

class ImagesViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        user = request.user
        try:
            image = user.user_images
            serializer = ImagesSerializer(image)
            return Response(serializer.data)
        except Images.DoesNotExist:
            return Response({"detail": "Изображение не найдено."}, status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, pk=None):
        user = request.user
        try:
            image = user.user_images
            if str(image.pk) != pk:
                return Response({"detail": "Доступ запрещён."}, status=status.HTTP_403_FORBIDDEN)
            serializer = ImagesSerializer(image)
            return Response(serializer.data)
        except Images.DoesNotExist:
            return Response({"detail": "Изображение не найдено."}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        user = request.user
        if hasattr(user, 'user_images'):
            raise ValidationError("У пользователя уже есть изображение.")
        serializer = ImagesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        user = request.user
        try:
            image = user.user_images
            if str(image.pk) != pk:
                return Response({"detail": "Доступ запрещён."}, status=status.HTTP_403_FORBIDDEN)
        except Images.DoesNotExist:
            return Response({"detail": "Изображение не найдено."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ImagesSerializer(image, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        user = request.user
        try:
            image = user.user_images
            if str(image.pk) != pk:
                return Response({"detail": "Доступ запрещён."}, status=status.HTTP_403_FORBIDDEN)
            image.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Images.DoesNotExist:
            return Response({"detail": "Изображение не найдено."}, status=status.HTTP_404_NOT_FOUND)
>>>>>>> 010e858 (images)
