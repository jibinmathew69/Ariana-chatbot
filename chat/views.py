from django.shortcuts import render
from .serializers import ChatSerializer
from .models import Chat
from rest_framework import viewsets
from rest_framework.views import APIView
from django.db import transaction
from questionaire.models import Questionaire,Questions,Responses
from rest_framework import status
from rest_framework.response import Response
from django.db.models.functions import Concat
from django.db.models import Value



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
    def post(self,request):

        if 'questionaire' not in request.data:
            return Response("Insufficient Parameters",status=status.HTTP_400_BAD_REQUEST)

        try:
            questionaire = Questionaire.objects.get(id=request.data["questionaire"])
        except Questionaire.DoesNotExist:
            return Response("Invalid Questionaire", status=status.HTTP_400_BAD_REQUEST)


        #If the status for last conversation is Null indicate the conversation was conpleted, else active conversation for questionaire

        try:
            chat = Chat.objects.get(questionaire=questionaire,status__isnull= False)
        except Chat.DoesNotExist:
            chat = None


        #A new chat
        if not chat:
            question = Questions.objects.get(reference_id=1,questionaire=questionaire)

            try:
                Chat.objects.create(questionaire=questionaire,log=question.question_text)
            except:
                return Response("Internal Server Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        else:
            question = Questions.objects.get(reference_id=chat.status,questionaire=questionaire)

            count = Responses.objects.filter(question=question.id, questionaire=questionaire)[:1] #check if there more stages in Conversation

            if not count:
                Chat.objects.filter(id=chat.id).update(status=None)     #ending conversation by setting status to null
                return Response("Restarting Conversation: "+chat.log, status=status.HTTP_200_OK)

            if "message" not in request.data:
                return Response("Invalid input", status=status.HTTP_400_BAD_REQUEST)

            valid_response = Responses.objects.filter(question=question.id,questionaire=questionaire,options__iexact=request.data["message"])[:1] #check if the user chose a valid option
            if not valid_response:
                return Response("Invalid Option", status=status.HTTP_400_BAD_REQUEST)

            try:
                question = Questions.objects.get(reference_id=valid_response[0].next,questionaire=questionaire) #fetch next question for user
            except Questions.DoesNotExist:
                return Response("Internal Server Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


            Chat.objects.filter(id=chat.id).update(status=question.reference_id,log=Concat('log', Value("->"+request.data["message"]))) #update chat state

        options = Responses.objects.values_list('options',flat=True).filter(question=question.id) #fetch option for current question

        result = {
            "question" : question.question_text,
            "response" : options
        }


        return Response(result,status=status.HTTP_200_OK)