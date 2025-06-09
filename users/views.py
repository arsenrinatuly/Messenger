<<<<<<< HEAD
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
=======
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import MethodNotAllowed, PermissionDenied
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from users.serializers import UserSerializer, UserModelSerializer
from drf_yasg.utils import swagger_auto_schema

class RegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={405: "Method not allowed"}
    )
    def get(self, request):
        raise MethodNotAllowed("GET")

    @swagger_auto_schema(
        request_body=UserModelSerializer,
        responses={
            201: "User successfully registered",
            400: "error",
            409: "conflict error"
        }
    )
    def post(self, request):
        serializer = UserModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            User.objects.create_user(**serializer.validated_data)
            return Response(
                {"message": "User successfully registered"},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_409_CONFLICT
            )


class UserListAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={200: UserSerializer(many=True)}
    )
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=None,
        responses={405: "Method not allowed"}
    )
    def post(self, request):
        raise MethodNotAllowed("POST")


class UserDetailAPIView(APIView):
    permission_classes = [AllowAny]

    def get_user(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if request.user.pk != user.pk:
            raise PermissionDenied("you have no power here")
        return user

    @swagger_auto_schema(
        responses={200: UserSerializer}
    )
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=UserModelSerializer,
        responses={
            200: "user updated",
            400: "serializer not valid",
            403: "forbidden",
            404: "user not found"
        }
    )
    def put(self, request, pk):
        user = self.get_user(request, pk)
        serializer = UserModelSerializer(instance=user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "user updated"})

    @swagger_auto_schema(
        request_body=UserModelSerializer,
        responses={
            200: "user partial updated",
            400: "serializer not valid",
            403: "forbidden",
            404: "user not found"
        }
    )
    def patch(self, request, pk):
        user = self.get_user(request, pk)
        serializer = UserModelSerializer(instance=user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "user partial updated"})

    @swagger_auto_schema(
        responses={
            200: "user has been deleted",
            403: "forbidden",
            404: "user not found"
        }
    )
    def delete(self, request, pk):
        user = self.get_user(request, pk)
        user.delete()
        return Response({"message": "user has been deleted"})
>>>>>>> d211408 (hz)
