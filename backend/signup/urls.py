"""signup URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from django.conf.urls import include as include2

urlpatterns = [
    path('api/chat/', include2('chat.urls')),
    path('api/chatroom/', include('chatroom.urls')),
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),

    # path('account/signin/', include('rest_auth.urls')),
    path('api/account/', include('rest_auth.urls')),
    # path('account/bizsignin/', include('rest_auth.urls')),

    path('api/account/signup/', include('rest_auth.registration.urls')),
    # path('account/bizsignup/', include('rest_auth.registration.urls')),

    path('api/reviews/', include('reviews.urls')),
    path('api/stores/', include('stores.urls')),
    path('api/deliveries/', include('deliveries.urls')),
    path('api/main/', include('main.urls')),
    path('api/calc/', include('calcembedding.urls')),
    path('api/advertisements/', include('advertisements.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
