from django.urls import path,include
from .views import ChatView,ChatTreeView,ChatbotView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register('chat',ChatView)

urlpatterns = [
    path('',include(router.urls)),
    path('chattree',ChatTreeView.as_view(),name="chattree"),
    path('chatbot',ChatbotView.as_view(),name="chatbot")
]
