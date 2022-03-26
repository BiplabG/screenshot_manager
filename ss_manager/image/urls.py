from django.urls import path, include
from image import views

urlpatterns = [
    path("", views.ImageList.as_view(), name='image-list'),
    path("<str:slug>/", views.ImageDetail.as_view(), name='image-detail'),
]
