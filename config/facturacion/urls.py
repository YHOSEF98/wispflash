from django.urls import path
from .views import *
from .views import *

urlpatterns = [
    path("facturas/add", SaleCreateView.as_view(), name="sale_create"),
    path("facturas/list", SaleListView.as_view(), name="sale_list"),
    path("facturas/detail/<int:pk>", SaledetailView.as_view(), name="sale_detail"),
    path("facturas/delete/<int:pk>", SaleDeleteView.as_view(), name="sale_delete"),
]