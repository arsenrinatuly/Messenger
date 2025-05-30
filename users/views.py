from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.exceptions import APIException
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
)
from django.db.models.query import QuerySet
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from users.serializators import UserModelSerializer, PasswordChangeSerializer


class RegistrationViewSet(ViewSet):
    permission_classes = [AllowAny]

    def list(self, request: Request) -> Response:
        raise APIException(
            code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="Not implemented",
        )

    def create(self, request: Request) -> Response:
        s = UserModelSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        try:
            User.objects.create(
                username=s.validated_data.get("username"),
                first_name=s.validated_data.get("first_name"),
                last_name=s.validated_data.get("last_name"),
                email=s.validated_data.get("email"),
                password=make_password(s.validated_data.get("password")),
            )

            return Response(
                data={"message": "success"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class UserViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request: Request) -> Response:
        queryset = User.objects.all()
        serializer = UserModelSerializer(queryset, many=True)
        if not serializer.data:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"error": "users not found"},
            )
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def create(self, request: Request) -> Response:
        raise APIException(
            code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="Not implemented"
        )

    def retrieve(self, request: Request, pk=None) -> Response:
        try:
            user = User.objects.get(pk=pk)
            serializer = UserModelSerializer(user)
            return Response(data=serializer.data)
        except Exception as e:
            return Response(
                data={"error": str(e)}, 
                status=status.HTTP_404_NOT_FOUND
            )

    def update(self, request: Request, pk=None) -> Response:
        user = request.user
        serializer = UserModelSerializer(
            instance = request.user, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(**serializer.validated_data)
        return Response(data={"message": "user updated"})

    def partial_update(self, request: Request, pk=None) -> Response:
        user = request.user
        serializer = UserModelSerializer(
            instance = request.user, data=request.data, partial = True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(**serializer.validated_data)
        return Response(data={"message": "user partial updated"})

    def destroy(self, request: Request, pk=None) -> Response:
        user: User | None = User.objects.filter(pk=pk).first()
        if not user:
            return Response(
                data={"error": "user not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        if request.user.pk is not user.pk:
            return Response(
                data={"message": "you have no power"},
                status=status.HTTP_400_BAD_REQUEST
            )
        user.delete()
        return Response(
            data={"message": "user has been deleted"}
        )
    
    @action(
        detail=False, 
        methods=['post'],
        permission_classes=[IsAuthenticated],
        url_path='change-password'
    )
    def change_password(self, request: Request) -> Response:
        """
        Изменение пароля пользователя.
        Требует передачи старого пароля и нового пароля с подтверждением.
        """
        try:
            serializer = PasswordChangeSerializer(
                data=request.data,
                context={'request': request}
            )

            if not serializer.is_valid():
                return Response(
                    data={'errors': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user = request.user
            new_password = serializer.validated_data['new_password']


            user.password = make_password(new_password)
            user.save(update_fields=['password'])

            return Response({
                'status': 'success',
                'message': 'Пароль успешно изменен'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'Ошибка при смене пароля: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)