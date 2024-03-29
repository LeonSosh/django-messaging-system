from django.urls import path
from .views import SendMessage, GetAllMessages, GetUnreadMessages, ReadMessage, DeleteMessage

urlpatterns = [
    path("send/", SendMessage.as_view(), name="send_message"),
    path("all/", GetAllMessages.as_view(), name="all_messages"),
    path("unread/", GetUnreadMessages.as_view(), name="unread_messages"),
    path("read/<int:message_id>/", ReadMessage.as_view(), name="read_message"),
    path("delete/<int:message_id>/", DeleteMessage.as_view(), name="delete_message"),
]
