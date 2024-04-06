from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password, check_password


class CustomUser(AbstractUser):
    SEX = (
        ('M', 'Чоловіча'),
        ('F', 'Жіноча'),
        ('A', 'Інша')
    )

    sex = models.CharField("sex", max_length=1, choices=SEX, default='A')
    email = models.EmailField(unique=True)
    birthDate = models.DateField("birthDate", default=date.today)
    is_online = models.BooleanField(blank=False, default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']


    def str(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2')):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

class Accomodation(models.Model):
    type = models.CharField(max_length=128, null=False)
    amount = models.IntegerField()

    def __str__(self):
        return f'Type "{self.type}"'


class Transport(models.Model):
    kind = models.CharField(max_length=128, null=False)
    amount = models.IntegerField()

    def __str__(self):
        return f'Type "{self.kind}"'


