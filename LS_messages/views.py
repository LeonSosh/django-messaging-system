from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


from .models import Message
from .serializers import MessageSerializer


def home_view(request):
    """
    A view that returns a simple HttpResponse with a welcome message.

    Parameters:
    - request: the HTTP request object

    Returns:
    - HttpResponse object with the welcome message
    """
    return HttpResponse("Welcome! not much here at the moment")


class SendMessage(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Handles the HTTP POST request for creating a new message.

        Parameters:
            request (Request): The HTTP request object containing the message data.

        Returns:
            Response: The HTTP response object with the serialized message data if the message is valid,
                      or the serialized error messages if the message is invalid.
        """
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(sender=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class GetAllMessages(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieves a list of messages for the authenticated user.

        Parameters:
            request (Request): The HTTP request object.

        Returns:
            Response: The serialized data of the retrieved messages.
        """
        messages = Message.objects.filter(receiver=request.user)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class GetUnreadMessages(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieves unread messages for the specified user and returns them serialized as Response data.
        :param request: the request object containing user information
        :return: Response data containing serialized unread messages
        """
        messages = Message.objects.filter(receiver=request.user, is_read=False)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class ReadMessage(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, message_id):
        """
        Retrieve a message by its ID and mark it as read for the current user.

        Args:
            self: The instance of the class.
            request: The request object.
            message_id: The ID of the message to retrieve.

        Returns:
            Response: The response containing the serialized message data.
        """
        message = get_object_or_404(Message, id=message_id, receiver=request.user)
        message.is_read = True
        message.save()
        serializer = MessageSerializer(message)
        return Response(serializer.data)


class DeleteMessage(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, message_id):
        """
        Deletes a message.

        Args:
            request (Request): The HTTP request object.
            message_id (int): The ID of the message to be deleted.

        Returns:
            Response: The HTTP response object indicating the success or failure of the deletion.
        """
        message = get_object_or_404(Message, id=message_id)
        if request.user == message.sender or request.user == message.receiver:
            message.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
