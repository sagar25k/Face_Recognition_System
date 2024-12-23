# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_person, name='create_person'),
    path('display/', views.display_data, name='display_data'),
]
