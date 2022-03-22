from django.urls import path, include
from image import views

urlpatterns = [
    path("", views.ImageList.as_view()),
    path("<int:pk>/", views.ImageDetail.as_view()),
]
