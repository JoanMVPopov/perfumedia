from django.urls import path, include

# from .views import LatestProductsList
# replaced with this

from backend.etl import views


# from . import views

urlpatterns = [
    path("latest-products/", views.LatestProductsList.as_view()),
    path("eda-ratings/", views.EDADataRatings.as_view()),
    path("eda-ratings-prog/", views.EDADataRatingsProgression.as_view()),
    path("eda-cat-notes/", views.EDADataCategoriesNotes.as_view()),
    path("eda-correlation/", views.EDADataCorrelation.as_view()),
    path("eda-brands/", views.EDADataBrands.as_view())
]