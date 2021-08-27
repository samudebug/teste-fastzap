import datetime
from fastzap.permissions import ChatParticipantPermission
from fastzap.serializers import ChatSerializer, MessageSerializer, UserSerializer
from fastzap.models import Chat, Message, User
from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework_extensions.mixins import NestedViewSetMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return super(UserViewSet, self).get_permissions()


class ChatViewSet(NestedViewSetMixin,viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class MessageViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    model = Message
    http_method_names = ['get', 'post', 'put', 'patch', 'head', 'options', 'trace']
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, ChatParticipantPermission]

    def create(self, request, *args, **kwargs):
        request.data['sender'] = request.user.id
        request.data['timestamp'] = datetime.datetime.now()
        result = super().create(request, *args, **kwargs)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            kwargs['parent_lookup_message_chat'],
            {
                    'type': 'add_message',
                    'text_content': request.data['text_content'],
                    'sender': result.data['sender']
                }
        )
        return result

    def get_queryset(self):
        return Message.objects.filter(chat=self.kwargs['parent_lookup_message_chat'])