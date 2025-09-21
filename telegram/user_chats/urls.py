from django.urls import path
from .views import ChatsViews,ChatsDetailView

urlpatterns = [
    path("",ChatsViews.as_view()),
    path("<int:id>/",ChatsDetailView.as_view())
]
