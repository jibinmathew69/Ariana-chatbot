from django.shortcuts import render
from .serializers import ChatSerializer
from .models import Chat
from rest_framework import viewsets
from rest_framework.views import APIView
from django.db import transaction
from questionaire.models import Questionaire,Questions,Responses
from rest_framework import status
from rest_framework.response import Response

class ChatView(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer



class ChatTreeView(APIView):

    @transaction.atomic
    def insertions(self, chat_nodes, questionaire_name):
        try:

            with transaction.atomic():
                # Create Questionaire
                questionaire = Questionaire(name=questionaire_name)
                questionaire.save()

                options = []
                for node in chat_nodes:

                    # Create Questions
                    question = Questions(question_text=node["question"], reference_id=node["id"], questionaire=questionaire)
                    question.save()                 #question id required

                    for response, next in node["response"].items():
                        options.append(
                            Responses(options=response, next=next, question=question, questionaire=questionaire))

                # Create Responses
                Responses.objects.bulk_create(options)          #bulk insert all response options


        except:
            return False

        return True


    def post(self,request):

        #data validation
        if 'file' not in request.FILES or 'name' not in request.data:
            return Response("Insufficient Parameters",status=status.HTTP_400_BAD_REQUEST)

        if not request.FILES['file'].name.lower().endswith('.json'):
            return Response("Invalid File",status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)


        import json

        file_obj = request.FILES['file']
        file_obj.seek(0)
        data = file_obj.read()

        try:
            data = json.loads(data)
        except:
            return Response("Invalid Json",status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

        #inserting decoded json
        if self.insertions(data,request.data["name"]):
            return Response("File inserted",status=status.HTTP_201_CREATED)

        return Response("Internal Server Error",status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ChatbotView(APIView):
    pass