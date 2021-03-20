from django.urls import path

from . import views
from .apps import CoreConfig as CurrentApp

app_name = CurrentApp.name

urlpatterns = [
    path("overview/", views.overview_view),
    path("", views.ProductsView.as_view())
]
