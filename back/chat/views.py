from .models import Message
from rest_framework.exceptions import PermissionDenied
from financeApp.models import CustomUser
from rest_framework import viewsets, authentication
from .serializers import MessageSerializer, OnlineUsersSerializer


class OnlineUsersViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = OnlineUsersSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = self.queryset.filter(is_online=True)
            return queryset
        else:
            raise PermissionDenied("Access denied")


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer

    def get_queryset(self):
        room = self.request.query_params.get('room')
        if room is None:
            queryset = Message.objects.all()
        else:
            queryset = Message.objects.all().filter(room=room)
        return queryset
