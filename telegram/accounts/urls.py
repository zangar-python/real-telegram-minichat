from .views import RegisterView,LoginView,UserProfile
from .allUsers import GetAllUsersViews,DeleteUser
from django.urls import path

urlpatterns = [
    path("register/",RegisterView.as_view()),
    path("login/",LoginView.as_view()),
    path("profile/",UserProfile.as_view()),
    path("users/",GetAllUsersViews.as_view()),
    path("del/",DeleteUser.as_view())
]
