# urls.py
from django.contrib import admin  # Import the admin module
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Make sure the admin route is registered
    path('', include('face_app.urls')),  # Include the app URLs for the face recognition app
]
