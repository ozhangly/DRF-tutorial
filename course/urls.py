
from django.urls import path, include
from rest_framework.routers import DefaultRouter

import course.views

# 实例化路由器
# router = DefaultRouter()
# # 将视图集注册到路由器中
# router.register(prefix='courseinfo', viewset=course.views.CourseViewSet)

urlpatterns = [
    # 函数式视图
    path('courselist/', course.views.course_list, name='fbv list'),
    path('course_detail/<int:id>', course.views.course_detail, name='course detail')

    # 类视图 Class Based View
    # 这里因为继承的是APIView，所以要使用as_view方法
    # path('courselist/', course.views.CourseList.as_view(), name='CBV'),
    # path('coursedetail/<int:id>', course.views.CourseDetail.as_view(), name='course detail')

    # 通用类视图接口
    # path('courselist/', course.views.GCourseList.as_view(), name='GBV'),
    # path('coursedetail/<int:id>', course.views.GCourseDetail.as_view(), name='gcourse detail')

    # 视图集的路由写法, 两种写法
    # 一:
    # 要注意一下，上面是三种方法都是不同的url对应不同的View类，但是在视图集方法中，却是不同的url对应同一个视图集类
    # 那么就要给不同的url指定视图集处理的方法，就是在as_view中指定 http请求的方法和视图集处理的方法名
    # 字典的key是http的方法，value是视图集ModelViewSet继承的ListModelMiXin中的list方法
    # path('courseinfo/', course.views.CourseViewSet.as_view(
    #     {
    #         'get': 'list',
    #         'post': 'create'
    #     }
    # ), name='GBVS'),
    # path('courseinfo/<int:id>', course.views.CourseViewSet.as_view(
    #     {
    #         'get': 'retrieve',
    #         'put': 'update',    # put是全部更新, patch是部分更新  --> 后面自己在函数视图和类视图再加一下
    #         'patch': 'partial_update',
    #         'delete': 'destroy'
    #     }
    # ), name='GBVS')

    # 这么写还是太麻烦，有更简单的方法
    # path("", include(router.urls))      # 太牛了。。。
]