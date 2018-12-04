from django.urls import path,include
from .views import ChatView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register('chat',ChatView)

urlpatterns = [
    path('',include(router.urls))
]
