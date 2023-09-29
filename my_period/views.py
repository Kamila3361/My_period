from django.shortcuts import get_object_or_404, get_list_or_404
from django.utils.decorators import method_decorator

from django.contrib.auth.decorators import login_required

from .models import PeriodCycle, PersonalInfo, ChatInfo
from ..secret_key import API_KEY

from rest_framework.response import Response
from rest_framework import status, generics
from .serializer import PeriodSerializer, UserSerializer, PersonalInfoSerializer, ChatSerializer, MessageSerializer

import openai
openai.api_key = API_KEY

class SignUpView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully.'})
        return Response(serializer.errors, status=400)

@method_decorator(login_required(login_url='/login/'), name='dispatch')
class FormVeiw(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = PersonalInfo.objects.all()
    serializer_class = PersonalInfoSerializer

    def get(self, request, *args, **kwargs):
        info = get_object_or_404(PersonalInfo, owner=request.user)
        info_serializer = self.get_serializer(info)
        return Response(info_serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=400)
    

@method_decorator(login_required(login_url='/login/'), name='dispatch')
class PeriodsView(generics.ListCreateAPIView):
    queryset = PeriodCycle.objects.all()
    serializer_class = PeriodSerializer

    def get(self, request, *args, **kwargs):
        periods = get_list_or_404(PeriodCycle, owner=request.user)
        serializer = PeriodSerializer(periods, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@method_decorator(login_required(login_url='/login/'), name='dispatch')
class PeriodsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PeriodCycle.objects.all()
    serializer_class = PeriodSerializer

    def get(self, request, pk, *args, **kwargs):
        period_detail = get_object_or_404(PeriodCycle, owner=request.user, pk=pk)
        serializer = PeriodSerializer(period_detail)
        return Response(serializer.data, status=status.HTTP_200_OK)

@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ChatAssistantView(generics.ListCreateAPIView, generics.DestroyAPIView):
    queryset = ChatInfo.objects.all()
    serializer_class = ChatSerializer

    def get(self, request, *args, **kwargs):
        messages = get_list_or_404(ChatInfo, owner=request.user)
        serializer = ChatSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):
        messages = ChatInfo.objects.filter(owner=request.user)
        messages.delete()
        return Response({'message': 'New chat'}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        parameters = get_object_or_404(PersonalInfo, owner=request.user)

        initial_message = [{'role': 'system',
            'content': f'''You are gynecologist with 10 years experience. 
            I am {parameters.age} old years girl. 
            My weight: {parameters.weight} kg and my height: {parameters.height} cm.
            I am interested about the menstruation. 
            Answer my question based on these parameters.'''},]

        userSerializer = self.get_serializer(data=request.data)
        if userSerializer.is_valid():
            userSerializer.save(owner=request.user, role='user')
        
        try:
            messages = ChatInfo.objects.filter(owner=request.user).all()
        except ChatInfo.DoesNotExist:
            messages = []  
        
        messageSerializer = MessageSerializer(messages, many=True)
        chat_messages = initial_message + messageSerializer.data
        chat_response = openai.ChatCompletion.create(
                model = "gpt-3.5-turbo",
                messages = chat_messages,
                )
        
        assistant_reply = chat_response['choices'][0]['message']['content']

        chatSerializer = self.get_serializer(data={'content': assistant_reply})

        if chatSerializer.is_valid():
            chatSerializer.save(owner=request.user, role='assistant')

        return Response(chatSerializer.data, status=status.HTTP_200_OK)


# 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