# members/urls.py
from django.urls import path
from . import views

app_name = 'members'

urlpatterns = [
    path('my-page/', views.my_page, name='my_page'),
]
