# import http.client
# import json
# from django.views import View
# from django.http import JsonResponse, HttpResponse        # 通过这种方式返回的就是json数据
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
#
# from django.shortcuts import render

# Create your views here.
# 回顾django原生的函数式视图编程接口和类视图编程接口

# course_dict = {
#     'name': '课程名称',
#     'introduction': '课程介绍',
#     'price': 0.11
# }


# 使用django FBV编写API接口
# @csrf_exempt            # 对于post，取消django的csrf限制
# def course_list(request):
#     if request.method == 'GET':
#         return HttpResponse(json.dumps(obj=course_dict), content='application/json')
#         # return JsonResponse(course_dict)      # 这两种实现的效果是相同的，返回的数据都是json类型的数据
#
#     if request.method == 'POST':
#         course = json.loads(request.body.decode('utf-8'))
#         return JsonResponse(course, safe=False)
#         # return HttpResponse(json.dumps(obj=course), content_type='application/json')      # 这两种方法实现的效果也是相同的


# Django DBV编写API接口  类视图接口
# @method_decorator(csrf_exempt, name='dispatch')       # 或者用这种方法取消csrf限制
# class CourseList(View):
#
#     def get(self, request):     # 用不同的方法来处理不同的请求
#         # 返回的方式和FBV一样
#         # return JsonResponse(course_dict)
#         # 或者是这种方式返回:
#         return HttpResponse(json.dumps(obj=course_dict), content_type='application/json')
#
#     @csrf_exempt
#     def post(self, request):
#         course = json.loads(request.body.decode('utf-8'))
#         # return JsonResponse(course_dict)
#         return HttpResponse(json.dumps(obj=course_dict), content_type='application/json')

###############################################################################################

# 呃。。。就是django原生的接口会有一些问题，就是实现一些功能需要自己去造轮子。。。
# 比如分页、排序、认证、权限、限流等等问题，这些都是rest api所必须的功能，但是DRF提供了这些功能.

# DRF视图开发的函数式编程:
# import rest_framework.status as status
#
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .models import Course
# from .serializer import CourseSerializer
# """
# 第一种：函数式编程：Function Based View
# """
# # 后面接的是后面函数的什么方法
#
#
# @api_view(['GET', 'POST'])      # 装饰函数的装饰器
# def course_list(request):
#     """
#     获取所有课程信息或者新增一个课程
#     :param request:
#     :return:
#     """
#     # DRF的FBV处理方法和django处理的方法类似, 都是先判断请求的是什么方法
#     if request.method == 'GET':     # 在这里就需要序列化了, 导入之前写好的模型类和序列化类
#         # 序列化，将数据库中查询的东西 ---> json数据
#         # 别问为什么这时要序列化，因为这是GET请求。。。。
#         ret = CourseSerializer(instance=Course.objects.all(), many=True)      # 因为要序列化多个项: many=True
#         # 在django中，返回的response一般是HttpResponse或者JsonResponse，在DRF中，一般使用封装好的rest_framework中的Response
#         return Response(data=ret.data, status=status.HTTP_200_OK)       # DRF封装好的状态码
#     elif request.method == 'POST':
#         # 这里就要进行反序列化了, 反序列化过程。
#         # 设置部分更新。但是有前提，就是在数据库中设置的必填字段，必须从前段传过来，如果没有，这里不会报错，但是在is_valid()验证那里会报错
#         # partial=True 只适用于非必填字段的可以不填
#         s = CourseSerializer(data=request.data, partial=True)
#         # 反序列化过程需要对数据进行校验, 因为前端数据通常不确定，不能确定数据类型是否符合定义好的属性
#         if s.is_valid():                    # 对数据进行校验, 校验成功返回True，失败返回False
#             s.save(teacher=request.user)    # 教师字段必填项，但是在Model类中又是设置的只读属性，那如果想要添加该怎么办呢？？？这里的解决方法是将添加该课程的用户设置为teacher
#             return Response(data=s.data, status=status.HTTP_201_CREATED)
#         else:                           # 校验失败, 返回错误
#             return Response(data=s.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET', 'POST', 'PUT', 'DELETE'])
# def course_detail(request, id):
#     """
#     对课程信息进行操作，具体操作为添加、删除、更新、查询
#     :param request:
#     :param id:
#     :return:
#     """
#     if request.method == 'GET':
#         try:
#             course = Course.objects.get(pk=id)
#         except Course.DoesNotExist:
#             return Response(data={"msg": "没有此课程"}, status=status.HTTP_404_NOT_FOUND)
#         course = CourseSerializer(instance=course, many=False)
#         return Response(data=course.data, status=status.HTTP_200_OK)
#
#     elif request.method == 'POST':
#         # 新增一个Course
#         course = CourseSerializer(data=request.data, partial=True)
#         if course.is_valid():
#             course.save(teacher=request.user)
#             return Response(data=course.data, status=status.HTTP_201_CREATED)
#         return Response(data=course.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'PUT':       # 这个是怎么更新呢?
#         # 因为要更新数据, 所以要先把数据查询出来
#         try:
#             course = Course.objects.get(pk=id)
#         except Course.DoesNotExist:
#             return Response(data={"msg": "不存在课程信息"}, status=status.HTTP_400_BAD_REQUEST)
#         # instance: 指的是要序列化的示例， 而data指的是数据的来源, 数据哪里来的
#         # 所以这个的作用是，前段传过来的数据序列化后，更新保存到course这个示例中
#         course = CourseSerializer(instance=course, data=request.data, partial=True)
#         if course.is_valid():
#             # 这里和post的区别是，不用设置teacher字段。因为put是更新，这条数据已经创建好了，teacher是有值的。而post是创建数据，teacher在开始时没有
#             course.save()
#             return Response(data=course.data, status=status.HTTP_200_OK)
#         return Response(data=course.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         try:
#             course = Course.objects.get(pk=id)
#         except Course.DoesNotExist:
#             return Response(data={"msg": "不存在课程信息"}, status=status.HTTP_400_BAD_REQUEST)
#         course.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


###############################################################################################

# DRF 类视图接口
# import rest_framework.status as status
#
# from rest_framework.views import APIView
# from .models import Course
# from .serializer import CourseSerializer
# from rest_framework.response import Response
#
#
# """类视图"""
# class CourseList(APIView):
#
#     def get(self, request):
#         course_list = Course.objects.all()
#         serializer = CourseSerializer(instance=course_list, many=True)
#         return Response(data=serializer.data, status=status.HTTP_200_OK)
#
#     def post(self, request):
#         # 这里就由我来写
#         # 创建序列化器。这个request.data 的数据就是在postman中的request的body中的raw格式的json对象
#         # 注意，在类视图编写过程中，最好写成 self.request.XXX, 这里APIView类中封装好了self.request和self.response
#         serializer = CourseSerializer(data=self.request.data, partial=True)
#
#         if serializer.is_valid():
#             serializer.save(teacher=self.request.user)
#             print('request.data format: ' + type(self.request.data))
#             print('serializer.data format: ' + type(serializer.data))
#             return Response(data=serializer.data, status=status.HTTP_201_CREATED)
#         return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 课程详情信息
# class CourseDetail(APIView):
#
#     def get_object(self, id):
#         return Course.objects.get(pk=id)
#
#     def get(self, request, id):
#         try:
#             course_detail = self.get_object(id)
#         except Course.DoesNotExist:
#             return Response(data={'msg': '没有课程信息'}, status=status.HTTP_400_BAD_REQUEST)
#         serializer = CourseSerializer(instance=course_detail, many=False)
#         return Response(data=serializer.data, status=status.HTTP_200_OK)
#
#     def post(self, request, id):
#         try:
#             course_detail = Course.objects.get(pk=id)
#         except Course.DoesNotExist:
#             return Response(data={'msg': '没有此课程信息'}, status=status.HTTP_400_BAD_REQUEST)
#         serializer = CourseSerializer(data=self.request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save(teacher=self.request.user)
#             return Response(data=serializer.data, status=status.HTTP_201_CREATED)
#         return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def put(self, request, id):
#         try:
#             course_detail = self.get_object(id)
#         except Course.DoesNotExist:
#             return Response(data={'msg': '没有此课程信息'}, status=status.HTTP_400_BAD_REQUEST)
#         serializer = CourseSerializer(instance=course_detail, data=self.request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(data=serializer.data, status=status.HTTP_200_OK)
#         return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, id):
#         try:
#             course_detail = self.get_object(id)
#         except Course.DoesNotExist:
#             return Response(data={'msg': '没有此课程信息'}, status=status.HTTP_400_BAD_REQUEST)
#
#         course_detail.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

###############################################################################################
# 上面两种写法的代码重复度还是很高，所以采用通用类视图接口来处理
























