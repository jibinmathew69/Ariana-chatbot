from django.urls import path,include
from .views import QuestionaireView,QuestionsView,ResponsesView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register('questionaire',QuestionaireView)
router.register('questions',QuestionsView)
router.register('responses',ResponsesView)


urlpatterns = [
    path('',include(router.urls))
]
