from fastzap.models import Chat
from rest_framework.permissions import BasePermission

class ChatParticipantPermission(BasePermission):

    def has_permission(self, request, view):
        chat = Chat.objects.get(pk=view.kwargs['parent_lookup_message_chat'])
        return request.user in chat.participants.all()

