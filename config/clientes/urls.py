from django.urls import path
from .views import *

urlpatterns = [
    path("", ClientesListView.as_view(), name="clientelist"),
    path("add/", ClienteCreateView.as_view(), name="clienteadd"),
    path("edit/<int:pk>", ClienteUpdateView.as_view(), name="clientedit"),
    path("delet/<int:pk>", ClienteDeleteView.as_view(), name="clientedelet"),
    path("zonas/list/", ZonasListView.as_view(), name="zonaslist"),
    path("zonas/add/", ZonaCreateView.as_view(), name="zonasadd"),
    path("zonas/edit/<int:pk>", ZonaUpdateView.as_view(), name="zonaedit"),
    path("zonas/delet/<int:pk>", ZonaDeleteView.as_view(), name="zonadelet"),
]