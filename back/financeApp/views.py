from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import Group
from rest_framework import permissions, viewsets
from rest_framework.request import Request
from django.contrib.auth.hashers import make_password, check_password

from .models import CustomUser, Transport, Accomodation

from .serializers import CustomUserSerializer, TransportSerializer, AccomodationSerializer
from rest_framework.permissions import IsAuthenticated

# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]


# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
#     permission_classes = [permissions.IsAuthenticated]


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, ]

from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from .models import CustomUser

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate

# serilaizer
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
            return Response(response, status=status.HTTP_200_OK)
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