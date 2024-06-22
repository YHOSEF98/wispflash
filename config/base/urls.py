from django.urls import path
from .views import *

urlpatterns = [
    path("", vista, name="vistaBase"),
]