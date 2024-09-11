from django.contrib import admin
from django.urls import path, include
from shop.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('shop.urls')),
    path('', home, name='home'),
]
