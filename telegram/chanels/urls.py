from django.urls import path
from .views import ChanelViews,chanel_detail_view,register_to_chanel_views

urlpatterns = [
    path("",ChanelViews.as_view()),
    path("<int:id>/",chanel_detail_view.as_view()),
    path("<int:id>/register/",register_to_chanel_views.as_view())
]
