from django.contrib import admin

# Register your models here.

# 将这些字段注册到后台，能够方便从后台直接添加数据
from .models import Course


# 这是注册了什么？注册了一个课程管理员吗
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'introduction', 'teacher', 'price')
    search_fields = ('name', 'introduction', 'teacher', 'price')
    list_filter = ('name', 'introduction', 'teacher', 'price')
