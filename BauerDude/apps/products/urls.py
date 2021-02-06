from django.urls import path
from rest_framework import routers
from . import views
from .apps import CoreConfig as CurrentApp
app_name = CurrentApp.name
router = routers.SimpleRouter()
router.register(r"", views.ProductsViewSet, basename="products")

urlpatterns = [
    path("overview/", views.overview_view)
]
urlpatterns += router.urls
