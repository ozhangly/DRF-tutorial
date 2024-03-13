from django.db import models
from django.conf import settings

# Create your models here.


class Course(models.Model):
    name = models.CharField(max_length=255, unique=True, help_text='课程名称', verbose_name='课程名称')
    introduction = models.TextField(help_text='课程介绍', verbose_name='课程介绍')
    price = models.DecimalField(max_digits=6, decimal_places=2, help_text='课程价格', verbose_name='价格')
    # 外键怎么定义？
    # 还有就是注册的话是不是就自动加到django的用户组里了？
    # 回答一：这里的外键指向的是验证的用户组。然后如果用户组中的用户删除了，那么该讲师也删除。
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text='讲师', verbose_name='讲师')
    create_at = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    update_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    # 元信息
    class Meta:
        verbose_name = '课程信息'
        verbose_name_plural = verbose_name
        ordering = ['price', ]

    def __str__(self):
        return self.name
