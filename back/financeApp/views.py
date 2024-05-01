from django.shortcuts import get_object_or_404, render
from rest_framework import permissions, viewsets
from rest_framework.request import Request
from django.contrib.auth.hashers import make_password, check_password
from .models import CustomUser, Transport, Accomodation
from .serializers import CustomUserSerializer, TransportSerializer, AccomodationSerializer
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from celery.result import AsyncResult
import json
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from .models import CustomUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import UserRegisterSerializer
from .serializers import UserLoginSerializer
from django.http import QueryDict
from .tasks import send_email_task, loop_task


def run_long_task(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        l = body['l']
        task = loop.delay(l)
        return JsonResponse({"task_id": task.id}, status=202)


def task_status(request, task_id):
    task = AsyncResult(task_id)
    if task.state == 'FAILURE' or task.state == 'PENDING':
        response = {
            'task_id': task_id,
            'state': task.state,
            'progression': "None",
            'info': str(task.info)
        }
        return JsonResponse(response, status=200)
    current = task.info.get('current', 0)
    total = task.info.get('total', 1)
    progression = (int(current) / int(total)) * 100
    response = {
        'task_id': task_id,
        'state': task.state,
        'progression': progression,
        'info': "None"
    }
    return JsonResponse(response, status=200)


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, ]


class UserLoginAPIView(APIView):
    def post(self, request, *args, **kargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            response = {
                "response": {
                    "detail": "Incorrect credentials!"
                }
            }
            if CustomUser.objects.filter(email=request.data['email']).exists():
                user = CustomUser.objects.get(email=request.data['email'])
                password_status = check_password(request.data['password'], user.password)
                if (password_status):
                    token, created = Token.objects.get_or_create(user=user)
                    response = {
                        'success': True,
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'token': token.key
                    }
                    return Response(response, status=status.HTTP_200_OK)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRegisterAPIView(APIView):
    def post(self, request, *args, **kargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'success': True,
                'user': serializer.data,
                'token': Token.objects.get(user=CustomUser.objects.get(username=serializer.data['username'])).key
            }
            return Response(response, status=status.HTTP_201_CREATED)
        raise ValidationError(
            serializer.errors, code=status.HTTP_406_NOT_ACCEPTABLE)


class UserLogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args):
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({"success": True, "detail": "Logged out!"}, status=status.HTTP_200_OK)


class TransportViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Transport.objects.all()

    def list(self, request:Request):
        queryset = Transport.objects.all()
        serializer=TransportSerializer(instance=queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request:Request, pk=None):
        post=get_object_or_404(Transport, pk=pk)
        serializer=TransportSerializer(instance=post)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class AccomodationViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Accomodation.objects.all()

    def list(self, request:Request):
        queryset = Accomodation.objects.all()
        serializer=AccomodationSerializer(instance=queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request:Request, pk=None):
        post=get_object_or_404(Accomodation, pk=pk)
        serializer=AccomodationSerializer(instance=post)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class DescriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        description = "Додаток для відстеження витрат і управління бюджетом - це зручний інструмент для користувачів, який дозволяє їм керувати своїми фінансами. Основна мета цього додатка полягає в тому, щоб допомогти користувачам відстежувати свої витрати, категоризувати їх і порівнювати зі своїм бюджетом. "
        info = {"description": description}
        print(request.headers)
        return Response(info)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        token = request.headers['Authorization'].split()[1]
        user_id = Token.objects.get(key=token).user_id
        user = CustomUser.objects.get(id=user_id)
        info = { "username": user.username,
                 "email": user.email,
                 "sex": user.sex,
                 "dob": user.birthDate}
        return Response(info)


class ComputeView(APIView):

    def post(self, request):

        income = self.request.query_params.get('income')
        accomodationId = self.request.query_params.get('accomodation')
        accomodation = Accomodation.objects.get(pk=accomodationId).amount
        utilities = self.request.query_params.get('utilities')
        food = self.request.query_params.get('food')
        transportationId = self.request.query_params.get('transportation')
        transportation = Transport.objects.get(pk=transportationId).amount
        entertainment = self.request.query_params.get('entertainment')

        if(int(income)-accomodation-int(utilities)-int(food)-transportation-int(entertainment)>=0):
            info = {"result": "success"}
        else:
            info = {"result": "error"}
        return Response(info)


class SendMessageView(APIView):

    def post(self, request):
        try:
            json_repr = json.loads(request.body)
        except:
            json_repr = QueryDict(request.body)
        to_email = json_repr['email']
        message = json_repr['message']

        if send_email_task.apply_async(args=[to_email, message], queue='firstqueue'):
            info = {"result": 'success'}
            return Response(info, status=status.HTTP_200_OK)
        else:
            info = {"result": 'error'}
            return Response(info, status=status.HTTP_400_BAD_REQUEST)


class LongTaskView(APIView):

    def post(self, request):
        try:
            json_repr = json.loads(request.body)
        except:
            json_repr = QueryDict(request.body)
        longValue = json_repr['l']

        if loop_task.apply_async(args=[longValue], queue='secondqueue'):
            info = {"result": 'success'}
            return Response(info, status=status.HTTP_200_OK)
        else:
            info = {"result": 'error'}
            return Response(info, status=status.HTTP_400_BAD_REQUEST)
