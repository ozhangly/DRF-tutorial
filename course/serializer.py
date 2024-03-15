import rest_framework.serializers

from django import forms

from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer
from .models import Course
from django.contrib.auth.models import User


# Serializer的设计理念和Django中的Form很像，然后回去的话可能得再看一遍Form的相关内容
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('name', 'introduction', 'price', 'teacher')


class UserSerializer(ModelSerializer):
    # 因为在Course中teacher是外键，但是使用django的序列化方案中，只会显示外键值，而不能直接显示外键的名字
    # 所以Serializer可以解决django中的序列化的问题
    class Meta:
        model = User
        fields = '__all__'


class CourseSerializer(ModelSerializer):
    # 老师在这里说的是，Course中的teacher参照的是User表，并不是在插入数据时新建的用户
    # 所以会有一个问题
    # 可以把这个字段设置为只读。。。。
    # ？？？？？？这是什么逻辑？？？？设置成只读就可以了吗？？？？
    # teacher = rest_framework.serializers.CharField(source='teacher.username')
    teacher = rest_framework.serializers.ReadOnlyField(source='teacher.username')      # 外键: 只读

    class Meta:
        model = Course          # 写法上和CourseForm一致
        # exclude = ('id', )
        fields = ('name', 'introduction', 'price', 'teacher')
        # 或者也可以这么写
        # fields = '__all__'      # 这样的话就是所有字段都序列化
        # 这个depth指的是外键关联的深度，比如teacher关联的是User表，那么如果user表中的属性也关联了其他表，那么那个表也能关联出来
        # 这里有一个问题，那在第二个关联的外键中的参考字段是不是也要写出来呢？像这个的teacher一样
        # depth = 2


# 如果响应数据中带有url的数据，应该怎么反序列化呢？
# 这时就可以继承DRF提供的HyperLinkedModelSerializer来实现
class HyperLinkCourseSerializer(HyperlinkedModelSerializer):
    teacher = rest_framework.serializers.ReadOnlyField(source='teacher.username')

    class Meta:
        model = Course
        # url是默认值，可在setting.py中设置URL_FIELD_NAME全局生效
        fields = ('id', 'name', 'url', 'introduction')


























