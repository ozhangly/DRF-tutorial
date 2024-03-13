import http.client
import json
from django.views import View
from django.http import JsonResponse, HttpResponse        # 通过这种方式返回的就是json数据
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.shortcuts import render

# Create your views here.
# 回顾django原生的函数式视图编程接口和类视图编程接口

course_dict = {
    'name': '课程名称',
    'introduction': '课程介绍',
    'price': 0.11
}


# 使用django FBV编写API接口
@csrf_exempt            # 对于post，取消django的csrf限制
def course_list(request):
    if request.method == 'GET':
        return HttpResponse(json.dumps(obj=course_dict), content='application/json')
        # return JsonResponse(course_dict)      # 这两种实现的效果是相同的，返回的数据都是json类型的数据

    if request.method == 'POST':
        course = json.loads(request.body.decode('utf-8'))
        return JsonResponse(course, safe=False)
        # return HttpResponse(json.dumps(obj=course), content_type='application/json')      # 这两种方法实现的效果也是相同的


# Django DBV编写API接口  类视图接口
# @method_decorator(csrf_exempt, name='dispatch')       # 或者用这种方法取消csrf限制
class CourseList(View):

    def get(self, request):     # 用不同的方法来处理不同的请求
        # 返回的方式和FBV一样
        # return JsonResponse(course_dict)
        # 或者是这种方式返回:
        return HttpResponse(json.dumps(obj=course_dict), content_type='application/json')

    @csrf_exempt
    def post(self, request):
        # return JsonResponse(course_dict)
        return HttpResponse(json.dumps(obj=course_dict), content_type='application/json')

# 呃。。。就是django原生的接口会有一些问题，就是实现一些功能需要自己去造轮子。。。
# 比如分页、排序、认证、权限、限流等等问题，这些都是rest api所必须的功能，但是DRF提供了这些功能.













