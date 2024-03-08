from django.shortcuts import get_object_or_404, render
from rest_framework import permissions, viewsets
from rest_framework.request import Request
from django.contrib.auth.hashers import make_password, check_password
from .models import CustomUser, Transport, Accomodation
from .serializers import CustomUserSerializer, TransportSerializer, AccomodationSerializer
from rest_framework.permissions import IsAuthenticated


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, ]

from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from .models import CustomUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import UserRegisterSerializer
from .serializers import UserLoginSerializer


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