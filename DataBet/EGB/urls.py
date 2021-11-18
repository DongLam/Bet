from django.urls import path
from . import views

urlpatterns = [
    path('', views.Crawl.as_view()),
]

