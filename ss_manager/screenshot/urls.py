from django.urls import path
from screenshot import views

urlpatterns = [
    path("", views.ScreenshotList.as_view(), name='screenshot-list'),
    path("<int:pk>/", views.ScreenshotDetail.as_view(), name='screenshot-detail'),
]
