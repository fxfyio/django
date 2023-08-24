from django.contrib import admin

# Register your models here.
# 向后台管理注册
from .models import Question
admin.site.register(Question)