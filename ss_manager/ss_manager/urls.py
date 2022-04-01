from rest_framework.authtoken import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('image/', include('image.urls'), name="image"),
    path('screenshot/', include('screenshot.urls'), name="screenshot"),
    path('auth/', include('otp_auth.urls'), name='auth')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('api-token-auth/', views.obtain_auth_token)
]
