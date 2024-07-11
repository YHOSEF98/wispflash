from django.urls import path
from .views import *

urlpatterns = [
    path("list/", MikrotikListView.as_view(), name="mikrolist"),
    path('segmentos-ip', SegmentosIPView.as_view(), name='segmentos-ip'),
    path("add/", MikrotikCreateView.as_view(), name="mikroadd"),
    path("edit/<int:pk>", MikrotikUpdateView.as_view(), name="mikroedit"),
    path("delet/<int:pk>", MikrotikDeleteView.as_view(), name="mikrodelet"),
    path("detail/<int:pk>", MikrotikDetailView.as_view(), name="mikrodetail"),
    path("reglascorte/<int:pk>", MikrotikreglasView.as_view(), name="relgascorte"),
    path("reincio/<int:pk>", MikrotikreinicioView.as_view(), name="reiniciomikro"),
    path("grupocorte/list/", GrupoCorteListView.as_view(), name="grupocortelist"),
    path("grupocorte/add/", GrupoCorteCreateView.as_view(), name="grupocorteadd"),
    path("grupocorte/edit/<int:pk>", GrupoCUpdateView.as_view(), name="grupocortedit"),
    path("grupocorte/delet/<int:pk>", GrupoCorteDeleteView.as_view(), name="grupocortedelet"),
    path("planes/list/", PlanesListView.as_view(), name="planeslist"),
    path("planes/add/", PlanesCreateView.as_view(), name="planesadd"),
    path("planes/edit/<int:pk>", PlanesUpdateView.as_view(), name="planesedit"),
    path("servicios/list/", ServiciosListView.as_view(), name="serivcioslist"),
    path("servicios/add/", ServicioCreateView.as_view(), name="serivcioadd"),
    path("servicios/edit/<int:pk>", ServicioUpdateView.as_view(), name="serivcioedit"),
    path("servicios/delet/<int:pk>", ServicioDeleteView.as_view(), name="serivciodelet"),
    path("servicio/desh/<int:pk>", DeshabilitarServicioView.as_view(), name="serivciodesh"),
    path("servicioselec/add/", ServicioCreateSelecView.as_view(), name="serivcioaddselec"),
    #path("test", test.as_view(), name="test"),
]

