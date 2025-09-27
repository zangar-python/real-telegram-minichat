from django.urls import path
from .views import ChanelViews,chanel_detail_view,register_to_chanel_views,user_channel_views

urlpatterns = [
    path("",ChanelViews.as_view()),
    path("<int:id>/",chanel_detail_view.as_view()),
    path("<int:id>/register/",register_to_chanel_views.as_view()),
    path("<int:id>/users/",user_channel_views.as_view())
]
