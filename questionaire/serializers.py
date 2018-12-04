from rest_framework import serializers
from .models import Questionaire,Questions,Responses


class QuestionaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionaire
        field = '__all__'



class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionaire
        field = '__all__'



class ResponsesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionaire
        field = '__all__'