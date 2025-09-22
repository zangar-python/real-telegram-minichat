from django.urls import path
from .views import ChatsViews,ChatsDetailView,chat_users_add_delete,MessagesViews

urlpatterns = [
    path("",ChatsViews.as_view()),
    path("<int:id>/",ChatsDetailView.as_view()),
    path("<int:id>/users/",chat_users_add_delete.as_view()),
    path("<int:id>/msg/",MessagesViews.as_view())
]
