from django.contrib.auth.models import Group
from rest_framework import serializers
from .models import CustomUser, Transport, Accomodation
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token


# class GroupSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ['url', 'name']

class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        # fields = 'all'
        exclude = ('password', 'groups', 'is_staff', 'is_superuser', 'last_login', 'user_permissions', 'is_active', 'date_joined')
        extra_kwargs = {"course": {"required": False, "allow_null": True}}


class UserLoginSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    email = serializers.CharField(read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["id", "email", "password"]


class UserRegisterSerializer(serializers.ModelSerializer):
    SEX = (
        ('M', 'Чоловіча'),
        ('F', 'Жіноча'),
        ('A', 'Інша')
    )

    id = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField()
    #first_name = serializers.CharField()
    #last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    #password2 = serializers.CharField(write_only=True)
    sex = serializers.ChoiceField(choices=SEX)
    birthDate = serializers.DateField()

    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "password", "sex", "birthDate"]
        extra_kwargs = {
            'password': {"write_only": True}
        }

    def validate_email(self, email):
        if CustomUser.objects.filter(email=email).exists():
            detail = {
                "detail": "User Already exist!"
            }
            raise ValidationError(detail=detail)
        return email

    def validate(self, instance):
        # if instance['password'] != instance['password2']:
        #     raise ValidationError({"message": "Both password must match"})

        if CustomUser.objects.filter(email=instance['email']).exists():
            raise ValidationError({"message": "Email already taken!"})

        return instance

    def create(self, validated_data):
        passowrd = validated_data.pop('password')
        #passowrd2 = validated_data.pop('password2')
        user = CustomUser.objects.create(**validated_data)
        user.set_password(passowrd)
        user.save()
        Token.objects.create(user=user)
        return user

class TransportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transport
        fields = '__all__'

class AccomodationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Accomodation
        fields = '__all__'