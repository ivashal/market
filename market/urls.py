"""
URL configuration for market project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from products import urls as urls_products
from users import urls as urls_users
from cart import urls as urls_cart
from orders import urls as urls_orders
from products.views import *
from django.conf.urls.static import static
from market import settings


urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('products/', include(urls_products)),
    path('users/', include(urls_users)),
    path('cart/', include(urls_cart)),
    path('orders/', include(urls_orders)),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
