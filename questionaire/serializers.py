from rest_framework import serializers
from .models import Questionaire,Questions,Responses


class QuestionaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionaire
        fields = '__all__'



class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = '__all__'



class ResponsesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responses
        fields = '__all__'