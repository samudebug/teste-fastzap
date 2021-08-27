"""testefastzap URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls.conf import include
from fastzap.views import ChatViewSet, MessageViewSet, UserViewSet
from django.contrib import admin
from django.urls import path
from rest_framework import routers
from rest_framework_extensions.routers import ExtendedSimpleRouter

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = ExtendedSimpleRouter()
router.register(r'users', UserViewSet)
(
    router.register(r'chats', ChatViewSet, basename="chat").register(r'messages', MessageViewSet, basename='chats-messages', parents_query_lookups=['message_chat'])
)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('api/token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
    path('admin/', admin.site.urls),
]
