from rest_framework import permissions
from rest_framework.views import APIView

class IsOwnerReadOnly(permissions.BasePermission):
    """
    自定义权限，只允许对象拥有者可以编辑
    """
    def has_object_permission(self, request, view, obj):
        """
        实现所有的request都有读权限, 因此一律允许GET，HEAD，OPTIONS方法
        :param request:
        :param view:
        :param obj:
        :return: bool
        """
        if request.method in permissions.SAFE_METHODS:      # SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
            return True
        # 这个对象obj指的就是要访问的对象示例，要看这个对象的拥有者是谁，如果当前的访问者和对象的拥有者不一致，那么就禁止访问该接口
        return request.user == obj.teacher
