from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Message
from .serializers import MessageSerializer
from django.http import HttpResponse


def home_view(request):
    return HttpResponse("Welcome! not much here at the moment")


class SendMessage(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(sender=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class GetAllMessages(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        messages = Message.objects.filter(receiver=request.user)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class GetUnreadMessages(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        messages = Message.objects.filter(receiver=request.user, is_read=False)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class ReadMessage(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, message_id):
        message = get_object_or_404(Message, id=message_id, receiver=request.user)
        message.is_read = True
        message.save()
        serializer = MessageSerializer(message)
        return Response(serializer.data)


class DeleteMessage(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, message_id):
        message = get_object_or_404(Message, id=message_id)
        if request.user == message.sender or request.user == message.receiver:
            message.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
