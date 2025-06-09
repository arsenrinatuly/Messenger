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