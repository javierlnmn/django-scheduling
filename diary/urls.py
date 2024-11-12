from django.urls import path
from . import views

app_name="diary"

urlpatterns = [
    path('', views.DiaryView.as_view(), name="diary"),
]
