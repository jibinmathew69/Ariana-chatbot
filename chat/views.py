from django.shortcuts import render
from .serializers import ChatSerializer
from .models import Chat
from rest_framework import viewsets

class ChatView(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
