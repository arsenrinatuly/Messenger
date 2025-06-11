from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import QuerySet
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.authentication import JWTAuthentication

from chats.models import Chat, Message
from chats.serializers import ChatSerializer, ChatQuerySerializer


class ChatsViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(responses={
        200: ChatSerializer(many=True)
    })
    def list(self, request: Request) -> Response:
        chats: QuerySet[Chat] = request.user.users_chats.all()
        serializer = ChatSerializer(instance=chats, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def create(self, request: Request) -> Response:
        pass

    @swagger_auto_schema(
        query_serializer=ChatQuerySerializer,
        responses={
            200: ChatSerializer
        }
    )
    def retrieve(self, request: Request, pk: int) -> Response:
        try:
            chat: Chat = request.user.users_chats.get(pk=pk)
        except Chat.DoesNotExist:
            return Response(
                data="chat not exist",
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ChatSerializer(instance=chat)
        return Response(data=serializer.data)

    def update(self, request: Request, pk: int) -> Response:
        pass

    def partial_update(self, request: Request, pk: int) -> Response:
        pass

    def destroy(self, request: Request, pk: int) -> Response:
        pass


class MessagesViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def list(self, request: Request) -> Response:
        pass

    def create(self, request: Request) -> Response:
        pass

    def retrieve(self, request: Request, pk: int) -> Response:
        pass

    def update(self, request: Request, pk: int) -> Response:
        pass

    def partial_update(self, request: Request, pk: int) -> Response:
        pass

    def destroy(self, request: Request, pk: int) -> Response:
        pass
