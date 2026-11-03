from django.urls import path
from . import views

app_name = "leaderboard"
urlpatterns = [
    path("", views.home, name="home"),
    path("t/<int:pk>/", views.detail, name="detail"),
    path("t/<int:pk>/add/", views.add_entry, name="add"),
]
