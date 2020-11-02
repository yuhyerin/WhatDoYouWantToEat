from django.conf import settings
from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager
from stores.models import Store


USERTYPE_CHOICES = [(0, 'BizUser'), (1, 'User')]
GENDER_CHOICES = [(0, 'Male'), (1, 'Female')]


# 장고는 다중 유저 모델을 지원하지 않는다.
# https://tech.serhatteker.com/post/2020-01/email-as-username-django/#2-creating-user-model
class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    usertype = models.IntegerField(choices=USERTYPE_CHOICES, null=True)
    gender = models.IntegerField(choices=GENDER_CHOICES, null=True)
    address = models.CharField(max_length=200, null=True)
    birth_year = models.DecimalField(max_digits=4, decimal_places=0, null=True)

    # 사업자번호,상호명 , 사업 카테고리, 사업등록증 사본, 사업장 주소
    biznumber = models.CharField(max_length=15, null=True)
    bizname = models.CharField(max_length=50, null=True)
    bizcategory = models.CharField(max_length=20, null=True)
    bizimage = models.ImageField(
        default='media/bonobono.png', null=True, blank=True, upload_to='biz')
    bizaddress = models.CharField(max_length=200, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


# 하나씩 추가하게 하고, 주소 목록을 줄 때는 최신순으로 5개를 주면 된다.
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, null=True)
    store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True)
    location = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
