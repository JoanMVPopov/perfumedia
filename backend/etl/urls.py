from django.urls import path, include

# from .views import LatestProductsList
# replaced with this

from backend.etl import views


# from . import views

urlpatterns = [
    path("latest-products/", views.LatestProductsList.as_view()),
]